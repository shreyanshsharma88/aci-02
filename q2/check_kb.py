#!/usr/bin/env python3
"""Check a Q2 answer.md: section completeness, rubric counts, undefined symbols,
and a forward-chaining run of the knowledge base that verifies each query.

Usage:
    python q2/check_kb.py q2/<BITS_ID>/answer.md
    python q2/check_kb.py q2/EXAMPLE.md --profile example
Exit code 0 = PASS, 1 = FAIL.
"""
import argparse
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent

PROFILES = {
    # minimums from the assignment docx (Section A.3 / B.3)
    "full": {"rules": 10, "facts": 20, "inference_rules": 10, "queries": 5, "word_counts": True},
    # only for q2/EXAMPLE.md (a short illustration)
    "example": {"rules": 4, "facts": 6, "inference_rules": 4, "queries": 2, "word_counts": False},
}
WORD_RANGES = {"B.2": (150, 250), "B.4": (200, 300), "B.5": (200, 300)}
SECTION_TITLES = {"B.1": "Submission Form", "B.2": "Anchor", "B.3": "Apply", "B.4": "Analyse",
                  "B.5": "Reflect"}
B1_FIELDS = ["Name", "ID No", "Industry / Domain", "Organisation Type", "Instructor prompt"]
BUILTINS = {"ge": lambda a, b: a >= b, "gt": lambda a, b: a > b, "le": lambda a, b: a <= b,
            "lt": lambda a, b: a < b, "eq": lambda a, b: a == b, "neq": lambda a, b: a != b}


# ============================================================ report
@dataclass
class Report:
    items: list = field(default_factory=list)      # (status, message)
    traces: list = field(default_factory=list)     # text blocks
    meta: dict = field(default_factory=dict)
    doc: object = None

    def add(self, status, msg):
        self.items.append((status, msg))

    @property
    def passed(self):
        return not any(s == "FAIL" for s, _ in self.items)

    def failures(self):
        return [m for s, m in self.items if s == "FAIL"]

    def render(self):
        out = []
        for s, m in self.items:
            out.append(f"[{s}] {m}")
        if self.traces:
            out.append("\n--- Forward-chaining derivations for your queries ---")
            out += self.traces
        n = len(self.failures())
        out.append("\nRESULT: " + ("PASS" if self.passed else f"FAIL ({n} item(s) to fix)"))
        return "\n".join(out)


# ============================================================ markdown parsing
def strip_comments(text):
    return re.sub(r"<!--.*?-->", "", text, flags=re.S)


def is_unfilled(text):
    t = text.strip()
    return not t or "TODO" in t


def split_sections(text):
    """'## B.n ...' headings -> {'B.n': body}"""
    secs, cur = {}, None
    for line in text.splitlines():
        m = re.match(r"^##\s+(B\.\d)\b", line)
        if m:
            cur = m.group(1)
            secs[cur] = []
            continue
        if re.match(r"^#{1,2}\s", line):
            cur = None
        if cur:
            secs[cur].append(line)
    return {k: "\n".join(v) for k, v in secs.items()}


def fenced_blocks(text, lang):
    return re.findall(rf"^```{lang}[ \t]*\n(.*?)^```", text, flags=re.S | re.M)


def without_fences(text):
    return re.sub(r"^```.*?^```", "", text, flags=re.S | re.M)


def prose(text):
    """Text of a section without headings, tables, code and guidance."""
    t = without_fences(text)
    lines = [l for l in t.splitlines() if not l.lstrip().startswith(("#", "|"))]
    return "\n".join(lines).strip()


def word_count(text):
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'’-]*", prose(text)))


def tables(text):
    """All markdown tables -> list of (header_cells, rows)."""
    out, cur = [], []
    for line in without_fences(text).splitlines() + [""]:
        if line.strip().startswith("|"):
            cur.append([c.strip() for c in line.strip().strip("|").split("|")])
        elif cur:
            body = [r for r in cur[1:] if not all(re.fullmatch(r":?-{2,}:?", c) for c in r if c)]
            out.append((cur[0], body))
            cur = []
    return out


def clean_cell(c):
    return c.replace("`", "").replace("*", "").strip()


def labelled_items(text, label):
    """Bullets like '- **BR3:** text' -> {3: text}"""
    out = {}
    for line in without_fences(text).splitlines():
        m = re.match(rf"^\s*[-*]\s*\**\s*{label}\s*(\d+)\s*\**\s*[:.)]?\s*\**\s*(.*)$", line)
        if m:
            out[int(m.group(1))] = m.group(2).strip()
    return out


def parse_b1(body):
    fields = {}
    for header, rows in tables(body):
        for r in rows:
            if len(r) >= 2:
                fields[clean_cell(r[0]).rstrip(":")] = clean_cell(r[1])
    return fields


def query_sections(b3):
    """'#### Query n' -> body text"""
    out, cur = {}, None
    for line in b3.splitlines():
        m = re.match(r"^#{3,4}\s+Query\s+(\d+)", line)
        if m:
            cur = int(m.group(1))
            out[cur] = []
            continue
        if re.match(r"^#{1,4}\s", line):
            cur = None
        if cur is not None:
            out[cur].append(line)
    return {k: "\n".join(v) for k, v in out.items()}


def labelled_field(body, label):
    """Text after '- **Label:**' up to the next '- **X:**' label or fence."""
    m = re.search(rf"^\s*[-*]?\s*\**{label}[^:\n]*:\**(.*?)(?=^\s*[-*]?\s*\*\*[A-Z][^*\n]*:\*\*|^```|\Z)",
                  body, flags=re.S | re.M)
    return m.group(1).strip() if m else None


# ============================================================ propositional logic
PL_TOKENS = [("NOT", r"¬|~|!"), ("AND", r"∧|&|/\\"), ("OR", r"∨|\||\\/"),
             ("IFF", r"↔|<->|<=>|⇔"), ("IMP", r"→|->|=>|⇒"), ("LP", r"\("), ("RP", r"\)"),
             ("CONST", r"⊤|⊥"), ("SYM", r"[A-Za-z][A-Za-z0-9_]*"), ("WS", r"\s+")]
PL_RE = re.compile("|".join(f"(?P<{n}>{p})" for n, p in PL_TOKENS))


def pl_parse(text):
    """Parse a propositional formula. Returns the set of symbols; raises ValueError."""
    toks, pos = [], 0
    text = text.strip().rstrip(".")
    while pos < len(text):
        m = PL_RE.match(text, pos)
        if not m:
            raise ValueError(f"unexpected character '{text[pos]}'")
        if m.lastgroup != "WS":
            toks.append((m.lastgroup, m.group()))
        pos = m.end()
    syms, i = set(), 0

    def peek():
        return toks[i][0] if i < len(toks) else None

    def eat(kind):
        nonlocal i
        if peek() != kind:
            raise ValueError(f"expected {kind} at token {i + 1}")
        i += 1

    def iff():
        imp()
        while peek() == "IFF":
            eat("IFF"); imp()

    def imp():
        disj()
        if peek() == "IMP":
            eat("IMP"); imp()

    def disj():
        conj()
        while peek() == "OR":
            eat("OR"); conj()

    def conj():
        unary()
        while peek() == "AND":
            eat("AND"); unary()

    def unary():
        nonlocal i
        k = peek()
        if k == "NOT":
            eat("NOT"); unary()
        elif k == "LP":
            eat("LP"); iff(); eat("RP")
        elif k == "SYM":
            syms.add(toks[i][1]); i += 1
        elif k == "CONST":
            i += 1
        else:
            raise ValueError("incomplete formula" if k is None else f"unexpected '{toks[i][1]}'")

    if not toks:
        raise ValueError("empty formula")
    iff()
    if i != len(toks):
        raise ValueError(f"unexpected '{toks[i][1]}' after a complete formula")
    return syms


# ============================================================ predicate logic (lenient)
QUANT_RE = re.compile(r"∀|∃|\bforall\b|\bexists\b", re.I)


def fol_predicates(text):
    """Names and arities of every Name(args) in a formula.
    '∀x (' and '∃y (' are quantifiers, not predicates."""
    out = []
    for m in re.finditer(r"([A-Za-z_][A-Za-z0-9_]*)(\s*)\(", text):
        before = text[:m.start()].rstrip()
        if m.group(2) and (before.endswith(("∀", "∃", ",")) or
                           re.search(r"(forall|exists)$", before, re.I)):
            continue
        if re.search(r"(∀|∃)$", before) or m.group(1).lower() in ("forall", "exists"):
            continue
        depth, j, args = 1, m.end(), 1
        while j < len(text) and depth:
            ch = text[j]
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
            elif ch == "," and depth == 1:
                args += 1
            j += 1
        if depth:
            raise ValueError(f"unbalanced parentheses after {m.group(1)}")
        out.append((m.group(1), args))
    return out


def norm(name):
    return name.lower().replace("_", "")


def parse_signature(cell):
    """'Employee(x, y)' or 'Employee/2' -> ('Employee', 2)"""
    c = clean_cell(cell)
    m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\s*\((.*)\)\s*$", c)
    if m:
        return m.group(1), len([a for a in m.group(2).split(",") if a.strip()])
    m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\s*/\s*(\d+)$", c)
    if m:
        return m.group(1), int(m.group(2))
    return None


# ============================================================ knowledge base (Datalog)
@dataclass(frozen=True)
class Atom:
    pred: str
    args: tuple
    neg: bool = False

    def __str__(self):
        a = f"{self.pred}({', '.join(map(fmt_term, self.args))})" if self.args else self.pred
        return ("not " + a) if self.neg else a


@dataclass
class Rule:
    head: Atom          # pred 'false' = integrity constraint
    body: list
    line: int
    text: str
    number: int = 0     # inference rule number (1-based), 0 for constraints


class Var(str):
    pass


def fmt_term(t):
    if isinstance(t, Var):
        return str(t)
    if isinstance(t, str) and not re.fullmatch(r"[a-z][A-Za-z0-9_]*", t):
        return f"'{t}'"
    return str(t)


TERM_RE = re.compile(r"\s*('(?:[^']*)'|\"(?:[^\"]*)\"|-?\d+(?:\.\d+)?|[A-Za-z_][A-Za-z0-9_]*)\s*")


def parse_term(s):
    s = s.strip()
    if s[:1] in "'\"":
        return s[1:-1]
    if re.fullmatch(r"-?\d+", s):
        return int(s)
    if re.fullmatch(r"-?\d+\.\d+", s):
        return float(s)
    if s[0].isupper() or s[0] == "_":
        return Var(s)
    return s


def split_top(s, sep=","):
    parts, depth, cur, quote = [], 0, "", None
    for ch in s:
        if quote:
            cur += ch
            if ch == quote:
                quote = None
            continue
        if ch in "'\"":
            quote = ch
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == sep and depth == 0:
            parts.append(cur)
            cur = ""
        else:
            cur += ch
    parts.append(cur)
    return [p.strip() for p in parts if p.strip()]


def parse_atom(s):
    s = s.strip()
    neg = False
    m = re.match(r"^(not\s+|\\\+\s*)", s)
    if m:
        neg, s = True, s[m.end():]
    m = re.fullmatch(r"([a-z][A-Za-z0-9_]*)\s*(?:\((.*)\))?", s, flags=re.S)
    if not m:
        raise ValueError(f"cannot read '{s}' (predicate names start lowercase: name(arg, ...))")
    args = tuple(parse_term(a) for a in split_top(m.group(2))) if m.group(2) is not None else ()
    for a in split_top(m.group(2) or ""):
        if not TERM_RE.fullmatch(a):
            raise ValueError(f"bad argument '{a}' in '{s}'")
    return Atom(m.group(1), args, neg)


def strip_kb_comment(line):
    out, quote = "", None
    for ch in line:
        if quote:
            if ch == quote:
                quote = None
        elif ch in "'\"":
            quote = ch
        elif ch == "%":
            break
        out += ch
    return out


def split_clauses(src):
    """Yield (line_number, clause_text_without_final_dot). Several clauses may share a line."""
    buf, start, quote = "", None, None
    lines = [strip_kb_comment(l) for l in src.splitlines()]
    for n, line in enumerate(lines, 1):
        for i, ch in enumerate(line):
            if start is None and not ch.isspace():
                start = n
            if quote:
                buf += ch
                if ch == quote:
                    quote = None
                continue
            if ch in "'\"":
                quote = ch
            nxt = line[i + 1] if i + 1 < len(line) else " "
            prev = buf[-1:] or " "
            if ch == "." and not (prev.isdigit() and nxt.isdigit()) and (nxt.isspace() or nxt == "%"):
                yield start, buf.strip()
                buf, start = "", None
                continue
            buf += ch
        buf += " "
    if buf.strip():
        yield start, buf.strip() + "\x00"          # marker: missing final '.'


def parse_kb(src):
    """Returns (facts list[(Atom, line)], rules list[Rule], errors list[str])"""
    facts, rules, errors = [], [], []
    for start, clause in split_clauses(src):
        if clause.endswith("\x00"):
            errors.append(f"KB line {start}: clause not terminated with '.'  ->  {clause[:-1]}")
            continue
        try:
            if ":-" in clause:
                head_s, body_s = clause.split(":-", 1)
                head = parse_atom(head_s)
                body = [parse_atom(b) for b in split_top(body_s)]
                if head.neg:
                    raise ValueError("a rule head cannot be negated")
                if not body:
                    raise ValueError("empty rule body")
                pos_vars = {a for b in body if not b.neg and b.pred not in BUILTINS
                            for a in b.args if isinstance(a, Var)}
                for lit in [head] + body:
                    if lit is head or lit.neg or lit.pred in BUILTINS:
                        free = [a for a in lit.args if isinstance(a, Var) and a not in pos_vars]
                        if free:
                            raise ValueError(f"variable {free[0]} in '{lit}' must also appear in a "
                                             "positive (non-negated, non-comparison) body condition")
                rules.append(Rule(head, body, start, clause))
            else:
                a = parse_atom(clause)
                if a.neg or any(isinstance(x, Var) for x in a.args):
                    raise ValueError("a fact must be ground (no variables, no 'not')")
                if a.pred in BUILTINS or a.pred == "false":
                    raise ValueError(f"'{a.pred}' is reserved")
                facts.append((a, start))
        except ValueError as e:
            errors.append(f"KB line {start}: {e}  ->  {clause}.")
    k = 0
    for r in rules:
        if r.head.pred != "false":
            k += 1
            r.number = k
    return facts, rules, errors


def unify(args, fact_args, subst):
    s = dict(subst)
    for a, f in zip(args, fact_args):
        if isinstance(a, Var):
            if a == "_":
                continue
            if a in s:
                if s[a] != f:
                    return None
            else:
                s[a] = f
        elif a != f:
            return None
    return s


def ground(atom, s):
    return Atom(atom.pred, tuple(s.get(a, a) if isinstance(a, Var) else a for a in atom.args))


class KB:
    def __init__(self, facts, rules):
        self.facts = {a for a, _ in facts}
        self.rules = rules
        self.model = defaultdict(set)          # pred -> set of arg tuples
        self.why = {}                          # Atom -> (rule, premises) ; facts -> None
        self.used = set()                      # atoms used as premises
        self.fired = defaultdict(int)          # rule number -> successful instantiations
        self.violations = []                   # (constraint rule, premises)
        for a in self.facts:
            self.model[a.pred].add(a.args)
            self.why[a] = None

    def strata(self):
        preds = {r.head.pred for r in self.rules} | {a.pred for a in self.facts}
        level = {p: 0 for p in preds}
        for _ in range(len(preds) + 2):
            changed = False
            for r in self.rules:
                for b in r.body:
                    if b.pred in BUILTINS:
                        continue
                    need = level.get(b.pred, 0) + (1 if b.neg else 0)
                    if level[r.head.pred] < need:
                        level[r.head.pred] = need
                        changed = True
            if not changed:
                return level
        raise ValueError("the rules use 'not' inside a cycle (p depends on not p); "
                         "this cannot be evaluated")

    def solve(self, body, s=None, prem=()):
        """Yield (substitution, premises) for a conjunction of literals."""
        s = s or {}
        if not body:
            yield s, prem
            return
        lit, rest = body[0], body[1:]
        if lit.pred in BUILTINS:
            vals = [s.get(a, a) if isinstance(a, Var) else a for a in lit.args]
            if len(vals) != 2:
                raise ValueError(f"{lit.pred} takes 2 arguments")
            try:
                ok = BUILTINS[lit.pred](*vals)
            except TypeError:
                ok = False
            if ok != lit.neg:
                g = ground(lit, s)
                yield from self.solve(rest, s, prem + (Atom(g.pred, g.args, lit.neg),))
            return
        if lit.neg:
            g = ground(lit, s)
            if g.args not in self.model[g.pred]:
                yield from self.solve(rest, s, prem + (Atom(g.pred, g.args, True),))
            return
        for fargs in list(self.model[lit.pred]):
            if len(fargs) != len(lit.args):
                continue
            s2 = unify(lit.args, fargs, s)
            if s2 is not None:
                yield from self.solve(rest, s2, prem + (Atom(lit.pred, fargs),))

    def run(self):
        level = self.strata()
        for k in sorted(set(level.values())):
            layer = [r for r in self.rules if level[r.head.pred] == k and r.head.pred != "false"]
            changed = True
            while changed:
                changed = False
                for r in layer:
                    for s, prem in list(self.solve(r.body)):
                        self.fired[r.number] += 1
                        self.used.update(prem)
                        h = ground(r.head, s)
                        if h.args not in self.model[h.pred]:
                            self.model[h.pred].add(h.args)
                            self.why[h] = (r, prem)
                            changed = True
        for r in self.rules:
            if r.head.pred == "false":
                for s, prem in self.solve(r.body):
                    self.violations.append((r, prem))
                    self.used.update(prem)
        return self

    def trace(self, atom, indent="  ", seen=None):
        seen = seen or set()
        if atom.pred in BUILTINS:
            return [f"{indent}{atom}   [comparison holds]"]
        if atom.neg:
            return [f"{indent}{atom}   [closed world: cannot be derived]"]
        why = self.why.get(atom)
        if why is None:
            return [f"{indent}{atom}   [fact]"]
        r, prem = why
        lines = [f"{indent}{atom}   [inference rule {r.number}: {r.text}.]"]
        if atom in seen:
            return lines
        for p in prem:
            lines += self.trace(p, indent + "    ", seen | {atom})
        return lines


def parse_query(block):
    q, expect = None, None
    for line in block.splitlines():
        line = line.strip()
        if line.startswith("?-"):
            q = line[2:].strip().rstrip(".")
        elif line.lower().startswith("expect:"):
            expect = line.split(":", 1)[1].strip()
    return q, expect


def parse_expect(expect, qvars):
    """'yes' / 'no' / 'X = a; X = b' / 'X = a, Y = b; ...' / 'none'"""
    e = expect.strip().lower()
    if e in ("yes", "true"):
        return True
    if e in ("no", "false", "none"):
        return False if not qvars else set()
    answers = set()
    for alt in expect.split(";"):
        b = {}
        for part in split_top(alt):
            if "=" not in part:
                raise ValueError(f"cannot read expected answer '{alt.strip()}'")
            k, v = part.split("=", 1)
            b[k.strip()] = parse_term(v.strip())
        if set(b) != set(qvars):
            raise ValueError(f"expected answer must bind exactly {', '.join(qvars)}")
        answers.add(tuple(b[v] for v in qvars))
    return answers


# ============================================================ the check
def load_members():
    p = HERE / "members.json"
    return {m["id"]: m for m in json.loads(p.read_text())} if p.exists() else {}


def check(path, profile="full"):
    prof = PROFILES[profile]
    rep = Report()
    path = Path(path)
    raw = path.read_text(encoding="utf-8")
    text = strip_comments(raw)
    secs = split_sections(text)
    rep.doc = {"raw": raw, "text": text, "sections": secs}

    # ---- sections present and filled
    for key, title in SECTION_TITLES.items():
        body = secs.get(key)
        if body is None:
            rep.add("FAIL", f"Section {key} {title}: heading '## {key} {title}' not found")
        elif key == "B.3":
            pass   # checked in detail below
        elif key == "B.1":
            pass
        elif is_unfilled(prose(body)):
            rep.add("FAIL", f"Section {key} {title}: still empty or contains TODO")
        else:
            rep.add("PASS", f"Section {key} {title}: filled ({word_count(body)} words)")
            if prof["word_counts"] and key in WORD_RANGES:
                lo, hi = WORD_RANGES[key]
                wc = word_count(body)
                if not lo <= wc <= hi:
                    rep.add("WARN", f"Section {key}: {wc} words (guide: about {lo}-{hi})")

    # ---- B.1
    b1 = parse_b1(secs.get("B.1", ""))
    rep.meta = {f: b1.get(f, "") for f in B1_FIELDS}
    missing = [f for f in B1_FIELDS if is_unfilled(b1.get(f, ""))]
    if "B.1" in secs:
        if missing:
            rep.add("FAIL", "Section B.1 Submission Form: fill in " + ", ".join(missing)
                    + ("  (write 'None given' if there was no instructor prompt)"
                       if "Instructor prompt" in missing else ""))
        else:
            rep.add("PASS", "Section B.1 Submission Form: all fields filled")
    members = load_members()
    sid = b1.get("ID No", "")
    if sid in members:
        if members[sid]["name"].lower() != b1.get("Name", "").strip().lower():
            rep.add("FAIL", f"B.1 Name '{b1.get('Name')}' does not match members.json for {sid} "
                            f"('{members[sid]['name']}')")
        if path.parent.name in members and path.parent.name != sid:
            rep.add("FAIL", f"B.1 ID {sid} does not match the folder {path.parent.name}")

    b3 = secs.get("B.3", "")
    if "B.3" not in secs:
        return finish(rep)

    # ---- business rules / PL / FOL counts and 1:1 mapping
    br = labelled_items(b3, "BR")
    pl = labelled_items(b3, "PL")
    fol = labelled_items(b3, "FOL")
    need = prof["rules"]
    for label, items, what in (("BR", br, "business rules (plain English)"),
                               ("PL", pl, "rules in propositional logic"),
                               ("FOL", fol, "rules in predicate logic")):
        filled = {k: v for k, v in items.items() if not is_unfilled(v)}
        todo = sorted(k for k, v in items.items() if is_unfilled(v))
        status = "PASS" if len(filled) >= need else "FAIL"
        msg = f"{what}: {len(filled)}/{need}"
        if todo:
            msg += f"  (still empty: {', '.join(f'{label}{k}' for k in todo)})"
        rep.add(status, msg)
    filled_br = {k for k, v in br.items() if not is_unfilled(v)}
    for label, items in (("PL", pl), ("FOL", fol)):
        miss = sorted(k for k in filled_br if is_unfilled(items.get(k, "")))
        if miss and len(filled_br) >= need:
            rep.add("FAIL", f"the same rules must appear in both logics: no {label} for "
                    + ", ".join(f"BR{k}" for k in miss))

    # ---- propositions
    props, preds, variables, consts = {}, {}, set(), set()
    for header, rows in tables(b3):
        h = clean_cell(header[0]).lower() if header else ""
        for r in rows:
            if not r or is_unfilled(" ".join(r[:2])):
                continue
            first = clean_cell(r[0])
            if h.startswith(("symbol", "proposition")):
                props[first] = r[1] if len(r) > 1 else ""
            elif h.startswith("predicate"):
                sig = parse_signature(first)
                if sig:
                    preds[norm(sig[0])] = sig
                else:
                    rep.add("FAIL", f"predicate table: cannot read '{first}' (write Name(x, y))")
            elif h.startswith("variable"):
                variables.update(v.strip() for v in first.split(","))
            elif h.startswith("constant"):
                consts.update(v.strip() for v in first.split(","))
    rep.add("PASS" if props else "FAIL", f"propositions defined: {len(props)}")
    undefined_p = defaultdict(list)
    for k, f in sorted(pl.items()):
        if is_unfilled(f):
            continue
        try:
            for s in pl_parse(f):
                if s not in props:
                    undefined_p[s].append(f"PL{k}")
        except ValueError as e:
            rep.add("FAIL", f"PL{k} is not a well-formed formula: {e}  ->  {f}")
    for s, where in sorted(undefined_p.items()):
        rep.add("FAIL", f"proposition '{s}' used in {', '.join(where)} but not defined in the "
                        "propositions table")
    if props and not undefined_p:
        unused = [p for p in props if not any(p in pl_safe_syms(f) for f in pl.values())]
        if unused:
            rep.add("WARN", f"propositions defined but never used: {', '.join(unused)}")

    # ---- predicates (FOL)
    rep.add("PASS" if preds else "FAIL", f"predicates defined: {len(preds)}")
    rep.add("PASS" if variables else "FAIL", f"variables listed: {len(variables)}")
    rep.add("PASS" if consts else "FAIL", f"constants listed: {len(consts)}")
    undefined_f = defaultdict(list)
    quantified = 0
    for k, f in sorted(fol.items()):
        if is_unfilled(f):
            continue
        try:
            for name, arity in fol_predicates(f):
                d = preds.get(norm(name))
                if d is None:
                    undefined_f[name].append(f"FOL{k}")
                elif d[1] != arity:
                    rep.add("WARN", f"FOL{k}: {name} used with {arity} argument(s), "
                                    f"defined with {d[1]}")
        except ValueError as e:
            rep.add("FAIL", f"FOL{k}: {e}")
        if QUANT_RE.search(f):
            quantified += 1
        elif variables and any(re.search(rf"\b{re.escape(v)}\b", f) for v in variables if v):
            rep.add("WARN", f"FOL{k} uses a variable but has no quantifier (∀ / ∃)")
    for name, where in sorted(undefined_f.items()):
        rep.add("FAIL", f"predicate '{name}' used in {', '.join(where)} but not defined in the "
                        "predicates table")
    if fol and quantified == 0 and any(not is_unfilled(v) for v in fol.values()):
        rep.add("FAIL", "no predicate-logic rule uses a quantifier (∀ or ∃)")

    # ---- knowledge base
    kb_src = "\n".join(fenced_blocks(b3, "kb"))
    facts, rules, errors = parse_kb(kb_src)
    for e in errors:
        rep.add("FAIL", e)
    inf_rules = [r for r in rules if r.head.pred != "false"]
    rep.add("PASS" if len(facts) >= prof["facts"] else "FAIL",
            f"KB facts: {len(facts)}/{prof['facts']}")
    rep.add("PASS" if len(inf_rules) >= prof["inference_rules"] else "FAIL",
            f"KB inference rules: {len(inf_rules)}/{prof['inference_rules']}")
    dup = len(facts) - len({a for a, _ in facts})
    if dup:
        rep.add("WARN", f"{dup} duplicate fact(s) in the KB (duplicates are not counted twice "
                        "by a marker)")

    kb_preds = {a.pred: len(a.args) for a, _ in facts}
    for r in rules:
        if r.head.pred != "false":
            kb_preds.setdefault(r.head.pred, len(r.head.args))
    used_preds = {(b.pred, len(b.args)) for r in rules for b in r.body if b.pred not in BUILTINS}
    for p, n in sorted(used_preds):
        if p not in kb_preds:
            rep.add("FAIL", f"KB predicate '{p}' is used in a rule body but is never a fact or a "
                            "rule head, so it can never be true")
    for p, n in sorted(set(kb_preds.items()) | used_preds):
        if preds and norm(p) not in preds and p not in BUILTINS:
            rep.add("FAIL", f"KB predicate '{p}/{n}' is not defined in the predicates table "
                            "(names match ignoring case and underscores)")
        elif preds and norm(p) in preds and preds[norm(p)][1] != n:
            rep.add("WARN", f"KB predicate '{p}' has {n} argument(s) but the table says "
                            f"{preds[norm(p)][1]}")

    kb = None
    if not errors and (facts or rules):
        try:
            kb = KB(facts, rules).run()
        except ValueError as e:
            rep.add("FAIL", f"KB cannot be evaluated: {e}")
    if kb:
        derived = sum(1 for a, w in kb.why.items() if w is not None)
        rep.add("PASS", f"forward chaining finished: {derived} new fact(s) derived")
        for r in inf_rules:
            if not kb.fired[r.number]:
                rep.add("WARN", f"inference rule {r.number} never fires (no facts satisfy its "
                                f"body): {r.text}.")
        contradictions = []
        for r, prem in kb.violations:
            contradictions.append(f"constraint '{r.text}.' is violated by "
                                  + ", ".join(map(str, prem)))
        for pred, rows in list(kb.model.items()):
            if pred.startswith("neg_"):
                for args in rows & kb.model.get(pred[4:], set()):
                    contradictions.append(f"both {Atom(pred[4:], args)} and {Atom(pred, args)} "
                                          "hold")
        for c in contradictions:
            rep.add("FAIL", "contradiction: " + c)
        if not contradictions:
            rep.add("PASS", "no contradictions")

    # ---- queries
    qs = query_sections(b3)
    filled_qs, query_preds = 0, set()
    for n in sorted(qs):
        body = qs[n]
        problems = []
        for label in ("Question", "Answer", "Reasoning"):
            v = labelled_field(body, label)
            if v is None or is_unfilled(v):
                problems.append(label.lower())
        blocks = fenced_blocks(body, "query")
        q, expect = parse_query(blocks[0]) if blocks else (None, None)
        if not q or "TODO" in q:
            problems.append("formal query '?- ...' in the query block")
        if not expect or "TODO" in expect:
            problems.append("'expect:' line")
        if problems:
            rep.add("FAIL", f"Query {n}: fill in " + ", ".join(problems))
            continue
        filled_qs += 1
        if kb is None:
            rep.add("FAIL", f"Query {n}: cannot be checked until the KB parses")
            continue
        try:
            body_atoms = [parse_atom(x) for x in split_top(q)]
            query_preds.update(a.pred for a in body_atoms)
            qvars = []
            for a in body_atoms:
                for t in a.args:
                    if isinstance(t, Var) and t != "_" and t not in qvars:
                        qvars.append(t)
            want = parse_expect(expect, qvars)
            sols = list(kb.solve(body_atoms))
        except ValueError as e:
            rep.add("FAIL", f"Query {n}: {e}")
            continue
        lines = [f"Query {n}: ?- {q}."]
        if qvars:
            got = {tuple(s[v] for v in qvars) for s, _ in sols}
            ok = got == want
            shown = "; ".join(", ".join(f"{v} = {fmt_term(x)}" for v, x in zip(qvars, t))
                              for t in sorted(got, key=str)) or "no answers"
            lines.append(f"  KB answer: {shown}")
            detail = f"KB gives {shown}; you expect {expect}"
        else:
            got = bool(sols)
            ok = got == want
            lines.append(f"  KB answer: {'yes' if got else 'no'}")
            detail = f"KB says {'yes' if got else 'no'}; you expect {expect}"
        for s, prem in sols[:3]:
            for p in prem:
                lines += kb.trace(p)
        if not sols:
            lines.append("  (no derivation: the query does not follow from the facts and rules)")
        rep.traces.append("\n".join(lines))
        rep.add("PASS" if ok else "FAIL",
                f"Query {n}: " + ("answer follows from the KB" if ok else
                                  f"answer does NOT follow from the KB ({detail})"))
    if kb:
        read_preds = {p for p, _ in used_preds} | query_preds
        unused = [a for a, _ in facts if a.pred not in read_preds]
        if unused:
            rep.add("WARN", f"{len(unused)} fact(s) never used by any rule or query: "
                    + ", ".join(map(str, unused[:8])) + (" ..." if len(unused) > 8 else ""))
    nq = prof["queries"]
    rep.add("PASS" if filled_qs == nq and len(qs) == nq else "FAIL",
            f"queries: {filled_qs} complete, {nq} required (found {len(qs)} query heading(s))")
    return finish(rep)


def pl_safe_syms(f):
    try:
        return pl_parse(f)
    except ValueError:
        return set()


def finish(rep):
    order = {"FAIL": 0, "WARN": 1, "PASS": 2}
    rep.items.sort(key=lambda x: order[x[0]])
    return rep


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("answer", help="path to answer.md")
    ap.add_argument("--profile", choices=PROFILES, default="full",
                    help="'full' = assignment minimums (default); 'example' = only for EXAMPLE.md")
    args = ap.parse_args(argv)
    rep = check(args.answer, args.profile)
    print(f"Checking {args.answer} (profile: {args.profile})\n")
    print(rep.render())
    return 0 if rep.passed else 1


if __name__ == "__main__":
    sys.exit(main())

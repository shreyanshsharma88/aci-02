#!/usr/bin/env bash
# Build dist/<GROUP>_ACI_Assignment2.zip with exactly 6 top-level files, then verify it.
# Usage:  GROUP=Group12 bash make_zip.sh
# Refuses to build if the notebook or any member's PDF is missing.
set -euo pipefail
cd "$(dirname "$0")"

GROUP="${GROUP:-GroupXX}"
if [ -x .venv/bin/python ]; then PY=.venv/bin/python
elif [ -x .venv/Scripts/python.exe ]; then PY=.venv/Scripts/python.exe
else PY=python3; fi

missing=()
[ -f Question1_Group.ipynb ] || missing+=("Question1_Group.ipynb (group notebook)")
while IFS='|' read -r id name; do
  [ -f "q2/$id/$id.pdf" ] || missing+=("q2/$id/$id.pdf  ($name)")
done < <("$PY" -c 'import json;[print(m["id"]+"|"+m["name"]) for m in json.load(open("q2/members.json"))]')

if [ ${#missing[@]} -gt 0 ]; then
  echo "REFUSING to build the zip. Missing:"
  for m in "${missing[@]}"; do echo "  - $m"; done
  echo
  echo "Each member builds their PDF with: python q2/build_pdf.py q2/<BITS_ID>/answer.md"
  exit 1
fi

[ "$GROUP" = "GroupXX" ] && echo "Note: GROUP not set; using '$GROUP'. Example: GROUP=Group12 bash make_zip.sh"

mkdir -p dist
OUT="dist/${GROUP}_ACI_Assignment2.zip"
rm -f "$OUT"
"$PY" - "$OUT" <<'EOF'
import json, sys, zipfile
out = sys.argv[1]
files = [("Question1_Group.ipynb", "Question1_Group.ipynb")]
files += [(f"q2/{m['id']}/{m['id']}.pdf", f"{m['id']}.pdf") for m in json.load(open("q2/members.json"))]
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for src, name in files:
        z.write(src, arcname=name)          # flat: no folders inside the zip
print(f"Built {out} with {len(files)} files")
EOF

"$PY" check_submission.py "$OUT"

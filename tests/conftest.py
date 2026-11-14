import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "q1"), str(ROOT / "q2"), str(ROOT)]

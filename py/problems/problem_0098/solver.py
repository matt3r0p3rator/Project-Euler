from __future__ import annotations

import os
import sys
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from py.euler.problem import run_problem


def solve() -> int:
    return 0


if __name__ == "__main__":
    os.chdir(Path(__file__).resolve().parent)
    raise SystemExit(run_problem("Problem 0098", solve))

from __future__ import annotations

import argparse
import importlib
import os
import sys
from pathlib import Path


def resolve_python_module_path(workspace_root: Path, problem_number: int) -> tuple[str, Path]:
    problem_name = f"problem_{problem_number:04d}"
    folder_solver = workspace_root / "py" / "problems" / problem_name / "solver.py"
    legacy_solver = workspace_root / "py" / "problems" / f"{problem_name}.py"

    if folder_solver.exists():
        return f"py.problems.{problem_name}.solver", folder_solver.parent

    if legacy_solver.exists():
        return f"py.problems.{problem_name}", workspace_root

    raise FileNotFoundError(problem_name)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a Project Euler Python solver by problem number.")
    parser.add_argument("problem_number", type=int, help="Problem number to run")
    args = parser.parse_args()

    if args.problem_number < 0:
        parser.error("problem_number must be non-negative")

    workspace_root = Path(__file__).resolve().parent.parent
    if str(workspace_root) not in sys.path:
        sys.path.insert(0, str(workspace_root))

    try:
        module_name, run_dir = resolve_python_module_path(workspace_root, args.problem_number)
    except FileNotFoundError:
        parser.error(f"No Python solver exists for problem {args.problem_number:04d}")

    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError as exc:
        if exc.name == module_name:
            parser.error(f"No Python solver exists for problem {args.problem_number:04d}")
        raise

    solve = getattr(module, "solve", None)
    if solve is None:
        parser.error(f"{module_name} does not define solve()")

    from py.euler.problem import run_problem

    os.chdir(run_dir)
    return run_problem(f"Problem {args.problem_number:04d}", solve)


if __name__ == "__main__":
    raise SystemExit(main())
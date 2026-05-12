from __future__ import annotations

import argparse
from pathlib import Path


def build_cpp_problem_source(problem_number: int) -> str:
    padded_number = f"{problem_number:04d}"
    return f'''#include <cstdint>

#include "euler/problem.hpp"

namespace {{

std::uint64_t solve() {{
    return 0;
}}

}}  // namespace

int main() {{
    return euler::run_problem("Problem {padded_number}", solve);
}}
'''


def build_python_problem_source(problem_number: int) -> str:
    padded_number = f"{problem_number:04d}"
    return f'''from __future__ import annotations

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
    raise SystemExit(run_problem("Problem {padded_number}", solve))
'''


def main() -> int:
    parser = argparse.ArgumentParser(description="Create new Project Euler solver files.")
    parser.add_argument("problem_number", type=int, help="Problem number to scaffold")
    parser.add_argument("--cpp-only", action="store_true", help="Create only the C++ solver file")
    parser.add_argument("--python-only", action="store_true", help="Create only the Python solver file")
    args = parser.parse_args()

    if args.problem_number < 0:
        parser.error("problem_number must be non-negative")

    if args.cpp_only and args.python_only:
        parser.error("--cpp-only and --python-only cannot be combined")

    workspace_root = Path(__file__).resolve().parent.parent
    created_files: list[Path] = []
    problem_name = f"problem_{args.problem_number:04d}"

    if not args.python_only:
        cpp_problem_dir = workspace_root / "cpp" / "problems" / problem_name
        cpp_problem_file = cpp_problem_dir / "main.cpp"
        legacy_cpp_problem_file = workspace_root / "cpp" / "problems" / f"{problem_name}.cpp"

        if cpp_problem_dir.exists() or legacy_cpp_problem_file.exists():
            parser.error(f"{problem_name} already exists for C++")

        cpp_problem_dir.mkdir(parents=True)
        cpp_problem_file.write_text(build_cpp_problem_source(args.problem_number), encoding="utf-8")
        created_files.append(cpp_problem_file)

    if not args.cpp_only:
        python_problem_dir = workspace_root / "py" / "problems" / problem_name
        python_problem_file = python_problem_dir / "solver.py"
        python_init_file = python_problem_dir / "__init__.py"
        legacy_python_problem_file = workspace_root / "py" / "problems" / f"{problem_name}.py"

        if python_problem_dir.exists() or legacy_python_problem_file.exists():
            parser.error(f"{problem_name} already exists for Python")

        python_problem_dir.mkdir(parents=True)
        python_init_file.write_text("", encoding="utf-8")
        python_problem_file.write_text(build_python_problem_source(args.problem_number), encoding="utf-8")
        created_files.append(python_init_file)
        created_files.append(python_problem_file)

    for path in created_files:
        print(f"created {path.relative_to(workspace_root)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

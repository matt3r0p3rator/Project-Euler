from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def resolve_cpp_problem_paths(workspace_root: Path, problem_number: int) -> tuple[Path, Path, str]:
    target_name = f"problem_{problem_number:04d}"
    folder_source_file = workspace_root / "cpp" / "problems" / target_name / "main.cpp"
    legacy_source_file = workspace_root / "cpp" / "problems" / f"{target_name}.cpp"

    if folder_source_file.exists():
        return folder_source_file, folder_source_file.parent, target_name

    if legacy_source_file.exists():
        return legacy_source_file, workspace_root, target_name

    raise FileNotFoundError(target_name)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build and run a Project Euler C++ solver by problem number.")
    parser.add_argument("problem_number", type=int, help="Problem number to build and run")
    args = parser.parse_args()

    if args.problem_number < 0:
        parser.error("problem_number must be non-negative")

    workspace_root = Path(__file__).resolve().parent.parent
    source_dir = workspace_root / "cpp"
    build_dir = source_dir / "build"
    executable_path: Path

    try:
        source_file, run_dir, target_name = resolve_cpp_problem_paths(workspace_root, args.problem_number)
    except FileNotFoundError:
        parser.error(f"No C++ solver exists for problem {args.problem_number:04d}")

    executable_path = build_dir / target_name

    subprocess.run(
        ["cmake", "-S", str(source_dir), "-B", str(build_dir)],
        check=True,
        cwd=workspace_root,
    )
    subprocess.run(
        ["cmake", "--build", str(build_dir), "--target", target_name],
        check=True,
        cwd=workspace_root,
    )
    completed = subprocess.run([str(executable_path)], cwd=run_dir)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
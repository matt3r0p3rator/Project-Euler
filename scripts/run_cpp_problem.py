from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def _build_env() -> dict[str, str]:
    """Return an environment that includes cmake/ninja from pip packages if not already on PATH."""
    env = os.environ.copy()
    extra_paths: list[str] = []

    if not shutil.which("cmake"):
        try:
            import cmake as _cmake  # type: ignore[import]
            extra_paths.append(_cmake.CMAKE_BIN_DIR)
        except ImportError:
            pass

    if not shutil.which("ninja"):
        try:
            import ninja as _ninja  # type: ignore[import]
            extra_paths.append(_ninja.BIN_DIR)
        except ImportError:
            pass

    if extra_paths:
        sep = os.pathsep
        env["PATH"] = sep.join(extra_paths) + sep + env.get("PATH", "")
    return env


def _resolve_tool(name: str, env: dict[str, str]) -> str:
    """Return the full path to a tool, searching env['PATH']."""
    found = shutil.which(name, path=env.get("PATH"))
    if found is None:
        raise FileNotFoundError(f"Could not find '{name}' on PATH. Install it or run: pip install {name}")
    return found


def _find_vsdevcmd() -> Path | None:
    """Return the path to VsDevCmd.bat for any VS or BuildTools installation, or None."""
    search_roots = [
        Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")) / "Microsoft Visual Studio",
        Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "Microsoft Visual Studio",
    ]
    for root in search_roots:
        if not root.exists():
            continue
        for vsdevcmd in sorted(root.rglob("VsDevCmd.bat"), reverse=True):
            return vsdevcmd
    return None


def _vs_env(env: dict[str, str]) -> dict[str, str]:
    """Return env augmented with VS build tools variables via VsDevCmd.bat."""
    vsdevcmd = _find_vsdevcmd()
    if vsdevcmd is None:
        return env
    result = subprocess.run(
        f'call "{vsdevcmd}" -no_logo -arch=x64 && set',
        shell=True,
        capture_output=True, text=True, errors="replace", env=env,
    )
    vs_env = dict(env)
    for line in result.stdout.splitlines():
        if "=" in line:
            k, _, v = line.partition("=")
            vs_env[k] = v
    return vs_env


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

    is_windows = sys.platform == "win32"
    exe_suffix = ".exe" if is_windows else ""
    exe_name = target_name + exe_suffix

    # Multi-config generators (e.g. Visual Studio on Windows) place executables
    # in a config subdirectory; single-config generators (Ninja, Make) put them
    # directly in the build dir.
    exe_candidates = [
        build_dir / exe_name,
        build_dir / "Debug" / exe_name,
        build_dir / "Release" / exe_name,
    ]

    cmake_build_cmd = ["cmake", "--build", str(build_dir), "--target", target_name]
    if is_windows:
        cmake_build_cmd += ["--config", "Debug"]

    env = _build_env()
    if is_windows:
        env = _vs_env(env)
    cmake_exe = _resolve_tool("cmake", env)
    cmake_build_cmd[0] = cmake_exe

    cmake_configure_cmd = [cmake_exe, "-S", str(source_dir), "-B", str(build_dir)]

    subprocess.run(
        cmake_configure_cmd,
        check=True,
        cwd=workspace_root,
        env=env,
    )
    subprocess.run(
        cmake_build_cmd,
        check=True,
        cwd=workspace_root,
        env=env,
    )

    executable_path = next((p for p in exe_candidates if p.exists()), build_dir / exe_name)
    completed = subprocess.run([str(executable_path)], cwd=run_dir)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
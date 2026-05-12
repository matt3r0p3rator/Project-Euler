from __future__ import annotations

from time import perf_counter
from typing import Callable


def run_problem(problem_name: str, solver: Callable[[], int]) -> int:
    start = perf_counter()
    answer = solver()
    elapsed_ms = (perf_counter() - start) * 1000

    print(problem_name)
    print(f"answer: {answer}")
    print(f"time:   {elapsed_ms:.3f} ms")
    return 0

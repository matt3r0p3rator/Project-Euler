# Project Euler Workspace

This workspace is set up with:

- a Python virtual environment in `.venv`
- a C++ solver scaffold in `cpp/`
- a Python solver scaffold in `py/`
- a helper script to create per-problem folders in `scripts/`

## Python

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Run the sample Python solver:

```bash
python scripts/run_python_problem.py 0
```

## C++

Configure and build all problems:

```bash
cmake -S cpp -B cpp/build
cmake --build cpp/build
```

Build and run one C++ solver by problem number:

```bash
python scripts/run_cpp_problem.py 0
```

Run the sample solver:

```bash
./cpp/build/problem_0000
```

Create a new problem scaffold:

```bash
source .venv/bin/activate
python scripts/new_problem.py 17
```

Then rebuild:

```bash
cmake --build cpp/build
```

That command creates both:

- `cpp/problems/problem_0017/main.cpp`
- `py/problems/problem_0017/solver.py`

You can place any problem-specific data files in those folders and the runners will execute from that problem directory.

Run a Python solver directly:

```bash
python scripts/run_python_problem.py 17
```

Run a C++ solver directly through the helper:

```bash
python scripts/run_cpp_problem.py 17
```

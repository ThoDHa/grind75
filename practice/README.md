# Grind75 Practice Harness

A `pytest` workspace for practicing the
[Grind75](https://www.techinterviewhandbook.org/grind75) problems. Each problem
gets a directory you solve in, debug through, and test. The canonical worked
solutions are **not** kept here — they live in the matching
[`../docs/problems/<slug>.md`](../docs/problems) write-up, which each `solution.py`
links to (and which links back), so you can go back and forth.

## Layout

```
practice/
├── harness.py            # shared helpers (ListNode/TreeNode/graph builders, case loader, pick_case)
├── pyproject.toml        # uv project (pytest dependency)
├── pytest.ini            # makes `import harness` work from any test
└── <problem_slug>/
    ├── solution.py       # YOUR attempt — solve here; run it directly to debug a case
    ├── cases.json        # simple cases: the LeetCode examples ("Run")
    ├── cases_full.json   # full cases: the edge-case gauntlet ("Submit")
    └── test_<slug>.py    # runs your solution against both case sets
```

## Setup (uv)

```bash
cd practice
uv sync           # creates .venv and installs pytest
```

## The practice loop

1. Open `<problem_slug>/solution.py`. The header links to the write-up at
   `../../docs/problems/<slug>.md` — read the problem there.
2. Implement the method.
3. **Debug it inside the file.** Each `solution.py` has a `__main__` block that
   runs one case and prints input / expected / actual. Set a breakpoint in your
   method, pick the case (edit the `CASE` id near the bottom), and run/de­bug the
   file directly:

   ```bash
   uv run python two_sum/solution.py
   ```

4. **Test it.** Two case sets, mirroring LeetCode's two buttons:

   ```bash
   uv run pytest two_sum/             # both sets
   uv run pytest two_sum/ -m simple   # "Run": just the examples
   uv run pytest two_sum/ -m full     # "Submit": the full gauntlet
   uv run pytest                      # everything
   ```

   An unsolved `solution.py` raises `NotSolved`, so its tests **skip** rather than
   fail. Once you implement it, they run for real (red → green).

5. To study the approaches, open `../docs/problems/<slug>.md` (linked from the top
   of `solution.py`).

## Two test sets: Run vs Submit

| File | Marker | Role |
|------|--------|------|
| `cases.json` | `simple` | The example cases. Fast feedback while you iterate. |
| `cases_full.json` | `full` | Examples **plus** a comprehensive edge-case gauntlet (empties, single elements, negatives, duplicates, boundary values, large inputs). |

`cases_full.json` is a thorough edge-case suite built to each problem's
constraints. LeetCode's literal hidden tests are not public, but this set targets
the same failure modes.

## Case format

Both `cases.json` and `cases_full.json` are lists of cases. For most problems a
case is `{"id": ..., "args": [...], "expected": ...}` where `args` is the
positional argument list and `expected` the return value. Problems with linked
lists, trees, graphs, or design-operation sequences store plain JSON in the case
files and the test module marshals it via the `harness` helpers.

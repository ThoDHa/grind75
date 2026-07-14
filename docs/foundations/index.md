# Foundations: Start Here

New to algorithms, data structures, or coding interviews? Read this section
first. The problem pages and pattern guides assume you already know how to read
`O(n)`, what recursion is, and what a hash map does. These foundations teach
exactly those prerequisites in plain language, with no prior computer science
background assumed.

If you already read complexity notation comfortably and know your core data
structures, skip ahead to the [pattern guides](../patterns/index.md) and the
[problems](../index.md).

## Who this is for

You can write a basic loop and an `if` statement in some language (Python is
used throughout, but the ideas carry over). You have little or no formal
training in algorithms, and terms like "Big-O", "recursion", "hash map", or
"dynamic programming" are unfamiliar or shaky. That is exactly the right
starting point.

## The four foundations

Read these in order. Each one is short and stands on its own.

| Guide | What it gives you | Why you need it first |
|-------|-------------------|------------------------|
| [Big-O Notation](big_o.md) | A feel for what `O(n)`, `O(n²)`, `O(log n)` mean and when each is "too slow" | Every solution is judged by its Big-O; without it the analysis sections are unreadable |
| [Recursion and the Call Stack](recursion.md) | What it means for a function to call itself, and how to trust it | Trees, graphs, backtracking, and divide-and-conquer all lean on recursion |
| [Data Structures in Pictures](data_structures.md) | Arrays, hash maps, sets, stacks, queues, linked lists, trees, graphs, and heaps, in plain terms | Choosing the right structure is half of solving a problem |
| [How to Approach a Problem](how_to_approach.md) | A repeatable method to go from a problem statement to a working solution | Stops the blank-page panic and turns "I have no idea" into a process |

A [glossary](glossary.md) defines the recurring jargon (memoization,
in-degree, amortized, and the rest) in one place for quick lookup.

## A suggested study path

1. Read the four foundations above (about an hour total).
2. Start with the easy problems in [Grind75 order](../index.md), problems 1
   through 10. Focus on understanding, not speed.
3. For each problem, follow this loop:
   - Read the problem page: the statement, examples, and constraints.
   - Open the linked **Pattern** guide. This is where the *why* lives.
   - Try to solve it yourself in the [`practice/`](https://github.com/ThoDHa/grind75/tree/main/practice)
     workspace before reading the solutions.
   - Read the solutions, starting with the first one listed. It is always the
     most direct baseline you could have reached yourself, usually a brute
     force, even when the page names it something more specific (Linear Scan,
     Simulation, Stack). Then work down the ladder to the faster approaches.
4. By the time you have seen 25 to 30 problems, most patterns will start to
   repeat. That repetition is the goal: patterns, not memorized solutions, are
   what let you solve problems you have never seen.

## Practicing in this repo

The [`practice/`](https://github.com/ThoDHa/grind75/tree/main/practice)
workspace is a ready-made pytest harness. One-time setup: `cd practice`, then
`uv sync`. After that, for any problem:

- `uv run pytest <slug>/ -m simple` is the equivalent of LeetCode's **Run**:
  just the example cases, for quick feedback while you iterate.
- `uv run pytest <slug>/ -m full` is the equivalent of **Submit**: the
  examples plus a comprehensive edge-case gauntlet.

An unsolved stub raises `NotSolved`, so its tests **skip** rather than fail. A
fresh checkout shows everything skipped, which is expected. Each `solution.py`
also has a `__main__` debug playground: set `CASE` to a case id near the
bottom of the file, then run the file directly
(`uv run python <slug>/solution.py`) to print the input, expected, and actual
values. The [practice README](https://github.com/ThoDHa/grind75/blob/main/practice/README.md)
walks through the full workflow.

The workspace also includes a small progress tracker, `progress.py`: `scan`
records which problems your tests currently pass, `rate` captures how each
solve felt, and `due` gives you a spaced-repetition review queue so earlier
problems come back before they fade. The
[practice README](https://github.com/ThoDHa/grind75/blob/main/practice/README.md)
documents the commands and intervals.

The point is not to finish fast. It is to build the mental models that make the
next problem easier than the last.

# Recursion and the Call Stack

Recursion is a function that solves a problem by calling itself on a smaller
version of the same problem. It feels like magic at first and like an old
friend later. This guide is about getting from the first feeling to the second.

## The shape of every recursive function

Every correct recursion has two parts:

- A **base case**: the smallest input, where the answer is known directly with
  no further calls. This is what stops the recursion.
- A **recursive case**: the function calls itself on a smaller input, then uses
  that result to build the answer for the current input.

Miss the base case and the function calls itself forever. Miss the recursive
case and it never makes progress. You need both.

## A first example: factorial

The factorial of `n` (written `n!`) is `n × (n-1) × (n-2) × ... × 1`. Notice
that `n!` is just `n × (n-1)!`. That self-reference is the recursive case.

```python
def factorial(n: int) -> int:
    if n == 0:          # base case: 0! is defined as 1
        return 1
    return n * factorial(n - 1)   # recursive case
```

## The leap of faith

The hardest mental step is trusting the recursive call. When you write
`factorial(n - 1)`, you must *assume it already returns the correct answer* for
`n - 1`, even though you are still writing the function that computes it. This
is not circular reasoning. It works because every call moves toward the base
case, where the answer is known for certain. The base case anchors the trust,
and each step inherits it.

A useful habit: write the base case first, then write the recursive case as if
the function you are calling were already finished and correct.

## The call stack: where the values actually live

When a function calls another function, the computer remembers where it was so
it can come back. It stacks these paused calls on top of each other, the **call
stack**, and unwinds them in reverse order. Recursion piles up calls of the
*same* function.

Here is `factorial(3)` traced step by step. Each indent is a deeper call that
has paused, waiting for the one below it to return:

```text
factorial(3)                 -> needs 3 * factorial(2)
    factorial(2)             -> needs 2 * factorial(1)
        factorial(1)         -> needs 1 * factorial(0)
            factorial(0)     -> base case, returns 1
        factorial(1) = 1 * 1 = 1     (resumes, returns 1)
    factorial(2) = 2 * 1 = 2         (resumes, returns 2)
factorial(3) = 3 * 2 = 6             (resumes, returns 6)
```

Read it top to bottom: the calls stack up, deeper and deeper, until the base
case is hit. Then read bottom to top: each paused call wakes up, multiplies,
and returns its result to the call above it. The final answer, `6`, falls out
of the topmost call.

This unwinding is the part beginners miss. The recursive call does not just
"happen", it *pauses* the current call, runs to completion, and hands a value
back so the paused call can finish.

## Why trees and graphs love recursion

A tree has a beautiful property: every child of a node is itself the root of a
smaller tree. So a function that processes "a tree" can process each child by
calling itself, and the base case is simply "an empty tree" or "a leaf". This
is why [tree problems](../patterns/tree/intuition.md) are so often three lines
of recursion. The structure of the data matches the structure of the function.

The same logic extends to [graphs](../patterns/graph/intuition.md) and to
[backtracking](../patterns/backtracking_exploration/intuition.md), where the
recursion explores choices and "un-makes" them on the way back up the stack.

## Common mistakes

- **Forgetting the base case**: the recursion never stops and the call stack
  grows until the program crashes with a "maximum recursion depth" error.
- **A base case that is never reached**: for example, recursing on `n - 2` when
  `n` can be odd, so it skips past the `n == 0` base. Make sure every path
  shrinks toward a base case.
- **Doing the same work many times**: plain recursion can re-solve identical
  subproblems over and over. The fix is **memoization** (caching each answer the
  first time you compute it), which is the bridge from recursion to
  [dynamic programming](../patterns/dp_1d_linear/intuition.md).
- **Recursing too deep**: Python stops at about 1,000 nested calls by default.
  For very deep structures (a linked list of 100,000 nodes), an iterative loop
  with an explicit stack avoids the limit.

## The one-sentence summary

A recursive function trusts itself on a smaller input and stops at a base case;
the call stack is what remembers each paused step so the answers can be combined
on the way back up.

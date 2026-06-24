# Big-O Notation

Big-O is a way to answer one question: **as the input grows, how does the
amount of work grow?** It is not about seconds on your laptop. It is about the
*shape* of the growth, because that shape is what decides whether your solution
survives a large input or times out.

## The core idea

Imagine an input of size `n` (the length of an array, the number of nodes in a
tree). Big-O describes how the number of steps grows as `n` gets bigger. We
drop constants and small terms and keep only the dominant growth, because for
large `n` that is all that matters.

Two examples make the idea concrete:

- A loop that touches every element once does about `n` steps. We call that
  **O(n)**: the work grows in step with the input.
- A loop nested inside another loop, each over the input, does about `n × n`
  steps. We call that **O(n²)**: double the input, quadruple the work.

The letter `O` means "on the order of", and `n` is the input size. So `O(n)`
reads as "on the order of `n` steps".

## The classes you will meet

From fastest-growing-slowest to slowest, the ones that appear in this guide:

| Big-O | Name | Plain meaning | Everyday analogy |
|-------|------|---------------|------------------|
| `O(1)` | Constant | Same work no matter the input size | Looking up a word you already memorized |
| `O(log n)` | Logarithmic | Each step throws away half the remaining work | Finding a name in a phone book by halving |
| `O(n)` | Linear | Work grows in step with the input | Reading every page of a book once |
| `O(n log n)` | Linearithmic | A linear pass that does a halving amount of work each time | Sorting a deck of cards efficiently |
| `O(n²)` | Quadratic | For every item, you touch every item | Comparing every person in a room to every other |
| `O(2ⁿ)` | Exponential | Each new item doubles the work | Trying every yes/no combination of `n` switches |

`O(1)` and `O(log n)` are excellent. `O(n)` and `O(n log n)` are the usual
targets for a good solution. `O(n²)` is often the brute force you start from.
`O(2ⁿ)` is usually only acceptable when `n` is tiny.

## Why the halving classes are so fast

`O(log n)` keeps appearing because halving is powerful. Each step of
[binary search](../patterns/binary_search/intuition.md) discards half of what
is left. Starting from a million items, you reach the answer in about 20 steps,
because you can only halve a million about 20 times before nothing is left.
That is the difference between `O(n)` (a million steps) and `O(log n)` (twenty).

## When to worry: matching Big-O to the input size

Competitive judges and interviewers care about Big-O because it predicts
whether you finish in time. A rough rule of thumb, assuming a budget of roughly
one hundred million simple operations:

| If `n` is up to | Then this is usually fast enough |
|-----------------|----------------------------------|
| 1,000,000,000+ | `O(log n)` or `O(1)` |
| 1,000,000 | `O(n)` or `O(n log n)` |
| 10,000 | `O(n²)` |
| 20 | `O(2ⁿ)` |

This is why the **Constraints** section on every problem page matters: it tells
you the size of `n`, which tells you what Big-O you must reach. If the
constraint says `n` can be 100,000, an `O(n²)` solution doing ten billion steps
will be too slow, and you know to look for an `O(n)` or `O(n log n)` approach.

## Counting the Big-O of your own code

A practical way to estimate:

- A single loop over the input is `O(n)`.
- A loop nested inside another loop over the same input is `O(n²)`.
- Halving the search range each step (or recursing on half) contributes a
  `log n` factor.
- Sorting a collection costs `O(n log n)`.
- A hash map lookup, insert, or membership test is `O(1)` on average.
- Constant work outside of any loop is `O(1)` and gets absorbed.

When several parts run one after another, the largest one wins: an `O(n)` pass
followed by an `O(n²)` pass is `O(n²)` overall.

## Space complexity is the same idea

Everything above measures *time* (steps). **Space complexity** measures *extra
memory* the same way. A solution that builds a hash map of every element uses
`O(n)` extra space. One that uses a handful of variables uses `O(1)` extra
space. The input itself is usually not counted, only the additional memory your
approach allocates.

Many problems offer a time-space trade: spend `O(n)` memory to cut time from
`O(n²)` down to `O(n)`. [Two Sum](../problems/two_sum.md) is the classic
example, and the [Hashing guide](../patterns/hashing/intuition.md) is built
entirely on that trade.

## The one-sentence summary

Big-O describes how work grows with input size, ignoring constants, so you can
predict whether a solution scales before you ever run it.

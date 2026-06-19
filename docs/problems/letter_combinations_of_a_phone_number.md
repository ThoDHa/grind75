# [Letter Combinations of a Phone Number](https://leetcode.com/problems/letter-combinations-of-a-phone-number/)

**Medium** | **30 minutes** | **Hash Table, String, Backtracking**

**Pattern:** [Backtracking](../patterns/backtracking_exploration/intuition.md)

**Practice:** [`practice/letter_combinations_of_a_phone_number/solution.py`](https://github.com/ThoDHa/grind75/blob/main/practice/letter_combinations_of_a_phone_number/solution.py)

Given a string containing digits from `2-9` inclusive, return all possible letter combinations that the number could represent. Return the answer in **any order**.

A mapping of digits to letters (just like on the telephone buttons) is given below. Note that `1` does not map to any letters.

![Phone Keypad](assets/letter_combinations_keypad.png)

## Examples

### Example 1

**Input:** `digits = "23"`

**Output:** `["ad","ae","af","bd","be","bf","cd","ce","cf"]`

### Example 2

**Input:** `digits = ""`

**Output:** `[]`

**Explanation:** An empty input maps to no combinations.

### Example 3

**Input:** `digits = "2"`

**Output:** `["a","b","c"]`

## Constraints

- `0 <= digits.length <= 4`
- `digits[i]` is a digit in the range `['2', '9']`.

## Solutions

### Iterative Build-up

```python
from typing import List


class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        if not digits:
            return []

        digit_to_letters = {
            '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
            '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz',
        }

        combinations = [""]
        for digit in digits:
            letters = digit_to_letters[digit]
            new_combinations = []
            for combination in combinations:
                for letter in letters:
                    new_combinations.append(combination + letter)
            combinations = new_combinations

        return combinations
```

#### Approach

Build the combinations one digit at a time. Start with a single empty
combination, then for each digit replace the current list with an expanded list
that appends every letter of that digit to every existing combination.

1. Return `[]` immediately for empty input, since no combinations exist.
2. Seed the working list with one empty string.
3. For each digit, look up its letters and build a new list by appending each
   letter to each current combination.
4. Replace the working list with the expanded list and continue.

For `digits = "23"` the list evolves as `[""]` then `["a", "b", "c"]` then
`["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]`.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(3^n * 4^m)`

Where `n` is the count of digits mapping to three letters and `m` the count
mapping to four letters. The expansion produces exactly this many combinations,
and each is built incrementally.

##### Space Complexity: `O(3^n * 4^m)`

The working list holds every intermediate and final combination during the
build-up, which is dominated by the final result size.

#### Key Insights

- The result is the Cartesian product of the per-digit letter sets, built one
  factor at a time.
- No recursion is required, which avoids recursion-stack overhead.
- Replacing the list each iteration keeps the state to exactly one generation of
  combinations at a time, aside from the new list being constructed.

### Recursive Suffix Expansion

```python
from typing import List


class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        if not digits:
            return []

        digit_to_letters = {
            '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
            '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz',
        }

        def generate(index: int) -> List[str]:
            if index == len(digits):
                return [""]
            suffixes = generate(index + 1)
            letters = digit_to_letters[digits[index]]
            return [letter + suffix for letter in letters for suffix in suffixes]

        return generate(0)
```

#### Approach

Frame the problem with divide and conquer: the combinations for `digits[index:]`
equal each letter of `digits[index]` prepended to every combination of
`digits[index + 1:]`.

1. The base case at `index == len(digits)` returns `[""]`, a single empty suffix.
2. Recurse on the remaining digits to obtain all suffix combinations.
3. Combine each letter of the current digit with each suffix.
4. The top-level call returns the full set for `digits[0:]`.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(3^n * 4^m)`

Each combination is produced exactly once, with additional linear work combining
suffixes at every recursion level.

##### Space Complexity: `O(3^n * 4^m)`

The combined lists hold every combination, plus `O(k)` recursion-stack depth for
`k = len(digits)`.

#### Key Insights

- Expresses the combinatorial structure recursively:
  `combos(digits) = letters(first) x combos(rest)`.
- Recomputes suffix lists once per level rather than per branch, since each
  `generate(index)` call evaluates `generate(index + 1)` a single time.
- The base case returning `[""]` (not `[]`) is essential; an empty list would
  collapse every product to empty.

### Queue-based BFS

```python
from collections import deque
from typing import List


class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        if not digits:
            return []

        digit_to_letters = {
            '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
            '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz',
        }

        queue = deque([""])
        for digit in digits:
            letters = digit_to_letters[digit]
            for _ in range(len(queue)):
                current = queue.popleft()
                for letter in letters:
                    queue.append(current + letter)

        return list(queue)
```

#### Approach

Treat each digit as a level in an implicit tree and explore breadth-first. The
queue holds all combinations of the current length; processing one digit advances
every entry to the next length.

1. Return `[]` for empty input.
2. Seed the queue with one empty string.
3. For each digit, snapshot the current queue length and dequeue exactly that
   many entries, enqueuing each extended by every letter of the digit.
4. After all digits are processed, the queue holds the full-length combinations.

Snapshotting the length before the inner loop keeps each level isolated, so a
combination is never extended twice within one digit's pass.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(3^n * 4^m)`

The level-by-level expansion enqueues each combination exactly once.

##### Space Complexity: `O(3^n * 4^m)`

The queue holds all combinations of the current length, which grows to the full
result size.

#### Key Insights

- Equivalent to the iterative build-up but framed as breadth-first traversal of
  the choice tree.
- The fixed-count inner loop (`range(len(queue))`) is what separates one level
  from the next.
- `deque` gives `O(1)` pops from the front, avoiding the `O(n)` cost of
  `list.pop(0)`.

### Backtracking

```python
from typing import List


class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        if not digits:
            return []

        digit_to_letters = {
            '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
            '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz',
        }

        result: List[str] = []
        n = len(digits)

        def backtrack(index: int, path: List[str]) -> None:
            if index == n:
                result.append("".join(path))
                return
            for letter in digit_to_letters[digits[index]]:
                path.append(letter)
                backtrack(index + 1, path)
                path.pop()

        backtrack(0, [])
        return result
```

#### Approach

Walk a decision tree depth-first, where each level chooses one letter for the
current digit. A shared `path` accumulates the current choices; on reaching the
end it is joined and recorded, then the last choice is undone before trying the
next branch.

1. Return `[]` for empty input.
2. At `index == n`, join the accumulated `path` and append it to `result`.
3. Otherwise, for each letter of the current digit, push it onto `path`, recurse,
   then pop it to restore state for the next letter.

Each digit position has its own independent set of choices, so no
visited-tracking is needed, unlike permutation problems.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(3^n * 4^m)`

Every leaf of the decision tree corresponds to one combination, and each is
produced once.

##### Space Complexity: `O(3^n * 4^m)`

The result stores all combinations, plus `O(k)` for the recursion stack and the
shared `path` of length `k = len(digits)`.

#### Key Insights

- The canonical interview answer: it makes the choose / explore / unchoose
  structure explicit.
- Accumulating into a list and joining once avoids repeated string concatenation
  along the path.
- Popping after each recursive call (`path.pop()`) is the backtracking step that
  reuses one buffer across all branches.

### Built-in itertools.product

```python
from itertools import product
from typing import List


class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        if not digits:
            return []

        digit_to_letters = {
            '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
            '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz',
        }

        letter_groups = [digit_to_letters[digit] for digit in digits]
        return ["".join(combo) for combo in product(*letter_groups)]
```

#### Approach

The problem is exactly the Cartesian product of the per-digit letter sets, which
`itertools.product` computes directly.

1. Return `[]` for empty input.
2. Map each digit to its letter group.
3. Spread the groups into `product`, which yields one tuple per combination, and
   join each tuple into a string.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(3^n * 4^m)`

`product` enumerates exactly the combinations of the Cartesian product.

##### Space Complexity: `O(3^n * 4^m)`

The returned list stores every combination.

#### Key Insights

- The shortest expression of the solution, leaning on the standard library to do
  the combinatorial work.
- Maps the mathematical view (Cartesian product) onto a single library call.
- Less suitable when an interviewer wants to see the underlying algorithm.

## Comparison of Solutions

### Time Complexity

- **Iterative Build-up**: `O(3^n * 4^m)` - expands every existing combination per digit, producing the full set.
- **Recursive Suffix Expansion**: `O(3^n * 4^m)` - same combination count, with extra work combining suffixes at each level.
- **Queue-based BFS**: `O(3^n * 4^m)` - level-by-level expansion generates the identical set.
- **Backtracking**: `O(3^n * 4^m)` - generates each combination once across the leaves of the decision tree.
- **Built-in itertools.product**: `O(3^n * 4^m)` - enumerates the Cartesian product directly.

### Space Complexity

- **Iterative Build-up**: `O(3^n * 4^m)` - holds intermediate and final combinations during build-up.
- **Recursive Suffix Expansion**: `O(3^n * 4^m)` - stores all combinations plus `O(k)` recursion stack.
- **Queue-based BFS**: `O(3^n * 4^m)` - the queue holds all combinations of the current length.
- **Backtracking**: `O(3^n * 4^m)` - stores the result plus `O(k)` recursion stack and a shared `path`.
- **Built-in itertools.product**: `O(3^n * 4^m)` - stores the resulting combinations.

### Trade-offs

- **Iterative Build-up**: Avoids recursion with a step-by-step build, at the cost of intermediate space.
- **Recursive Suffix Expansion**: Offers a clean divide-and-conquer view, with more involved combination logic.
- **Queue-based BFS**: Frames the work as level-order traversal, but adds queue-management overhead.
- **Backtracking**: Clear, educational, and buffer-efficient, but carries recursion overhead.
- **Built-in itertools.product**: Most concise, but depends on a library and reveals little of the algorithm.

### When to Use Each

- **Iterative Build-up**: When recursion is undesirable or for step-by-step visualization.
- **Recursive Suffix Expansion**: To demonstrate divide-and-conquer thinking on combinatorial generation.
- **Queue-based BFS**: When modeling the problem as level-order tree traversal.
- **Backtracking**: Best for interviews (recommended); it demonstrates the core algorithmic pattern.
- **Built-in itertools.product**: For production code where conciseness matters more than demonstration.

### Optimization Notes

- All approaches share the same asymptotic complexity because the work is bounded
  by producing the output; they differ mainly in intermediate space and clarity.
- String concatenation with `+` allocates a new string each time. For the
  constrained input (at most four digits) this is negligible, but accumulating
  characters in a list and joining once (as in the backtracking solution) scales
  better for longer inputs.
- Prefer `itertools.product` in production for conciseness and speed, but choose a
  from-scratch approach in interviews where demonstrating the algorithm matters.

# [Valid Anagram](https://leetcode.com/problems/valid-anagram/)

**Easy** | **15 minutes** | **String**

**Pattern:** [Hashing & Frequency Counting](../patterns/hashing/intuition.md)

**Practice:** [`practice/valid_anagram/solution.py`](../../practice/valid_anagram/solution.py)

Given two strings `s` and `t`, return `true` if `t` is an anagram of `s`, and `false` otherwise.

An **anagram** is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.

## Examples

### Example 1

**Input:** `s = "anagram"`, `t = "nagaram"`

**Output:** `true`

### Example 2

**Input:** `s = "rat"`, `t = "car"`

**Output:** `false`

## Constraints

- `1 <= s.length, t.length <= 5 * 10^4`
- `s` and `t` consist of lowercase English letters.

## Follow-up

What if the inputs contain Unicode characters? How would you adapt your solution to such a case?

## Solutions

### Iterative Character Removal

```python
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        for c in t:
            if c in s:
                s = s.replace(c, "", 1)
            else:
                return False
        return True
```

#### Approach

This solution directly implements the anagram definition by consuming `s` one
character at a time:

1. If the strings differ in length they cannot be anagrams, so return `False`.
2. For each character `c` in `t`, look for `c` in the remaining `s`.
3. If `c` is present, remove a single occurrence with `replace(c, "", 1)`.
4. If `c` is missing, the strings are not anagrams, so return `False`.
5. If every character of `t` is matched and removed, return `True`.

Equal lengths plus a successful match for every character of `t` guarantees the
two strings hold the same multiset of characters.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n²)`

For each of the `n` characters in `t` we search and rebuild `s`, and both the
`in` test and `replace` scan the whole string in `O(n)`, giving `O(n²)` overall.

##### Space Complexity: `O(n)`

Strings are immutable, so each `replace` allocates a fresh copy of `s` whose
length is proportional to the input.

#### Key Insights

- The most literal translation of "rearranging the same letters" into code.
- Quadratic time makes it unsuitable for the upper constraint of `5 * 10^4`.
- Repeated string copying compounds the cost because strings are immutable.

#### Walkthrough

Trace the first solution on Example 1: `s = "anagram"`, `t = "nagaram"`. The
lengths match (`7` and `7`), so the loop runs. Each row shows the character `c`
taken from `t`, whether it is found in the current `s`, and the value of `s`
after `replace(c, "", 1)` removes one copy:

| Step | `c` from `t` | Found in `s`? | `s` after removal |
|------|--------------|---------------|-------------------|
| start | — | — | `"anagram"` |
| 1 | `n` | yes | `"aagram"` |
| 2 | `a` | yes | `"agram"` |
| 3 | `g` | yes | `"aram"` |
| 4 | `a` | yes | `"ram"` |
| 5 | `r` | yes | `"am"` |
| 6 | `a` | yes | `"m"` |
| 7 | `m` | yes | `""` |

Every character of `t` was found and removed, so the loop never hits the `else`
branch that would return `False`. After the final step `s` is empty, the loop
ends, and the code returns `True`, which matches the expected Output `true`.

### Set-based Counting

```python
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        for c in set(s):
            if s.count(c) != t.count(c):
                return False
        return True
```

#### Approach

This solution compares per-character frequencies without an explicit counter
structure:

1. Reject mismatched lengths immediately.
2. Collect the distinct characters of `s` with `set(s)`.
3. For each distinct character, compare its occurrence count in `s` and `t`.
4. If any count differs, return `False`; otherwise return `True`.

Equal lengths mean that matching the count of every character present in `s` is
sufficient: `t` cannot contain an extra unmatched character without exceeding the
shared length.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n * k)`

Building the set is `O(n)`. For each of the up to `k` distinct characters,
`count()` scans both strings in `O(n)`, yielding `O(n * k)`, which degrades to
`O(n²)` when nearly every character is unique.

##### Space Complexity: `O(k)`

The set holds at most `k` distinct characters, where `k` is the alphabet size.

#### Key Insights

- Restricting the work to distinct characters trims the number of comparisons.
- Repeated `count()` calls reintroduce linear scans, so this is faster than
  iterative removal but slower than a single counting pass.
- Bounded only for a small alphabet; a large character set makes `k` grow.

### Hash Map Count

```python
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        counter = {}
        for c in s:
            counter[c] = counter.get(c, 0) + 1
        for c in t:
            if counter.get(c, 0) == 0:
                return False
            counter[c] -= 1
        return True
```

#### Approach

This solution counts characters once and then cancels them out, all by hand:

1. Reject mismatched lengths immediately.
2. Build a dictionary mapping each character of `s` to its frequency.
3. Walk `t`, decrementing the matching count for each character.
4. If a character of `t` has no remaining count, return `False`.
5. Surviving the full walk means every count cancelled exactly, so return `True`.

The length check makes a single decrementing pass sufficient: if all counts stay
non-negative and the totals match, the multisets are identical.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each string is traversed once, and every dictionary read or write is amortized
`O(1)`, so the total is linear in the input length.

##### Space Complexity: `O(k)`

The dictionary stores at most `k` distinct characters, where `k` is the alphabet
size (`26` for lowercase English letters).

#### Key Insights

- Linear time with no reliance on a counting library, making it portable to any
  language.
- A single decrement pass replaces repeated scans of the input.
- The length guard is what lets one-directional cancellation prove equality.

### Fixed Array Count

```python
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        counts = [0] * 26
        base = ord("a")
        for c in s:
            counts[ord(c) - base] += 1
        for c in t:
            counts[ord(c) - base] -= 1
            if counts[ord(c) - base] < 0:
                return False
        return True
```

#### Approach

This solution specializes the hash map idea to the fixed lowercase alphabet by
replacing the dictionary with a 26-slot array:

1. Reject mismatched lengths immediately.
2. Map each character to an index with `ord(c) - ord("a")`.
3. Increment the slot for every character in `s`.
4. Decrement the slot for every character in `t`, failing fast if any slot goes
   negative.
5. Equal lengths plus no negative slot means every count returned to zero, so
   return `True`.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Both passes are linear, and array indexing by integer offset is a constant-time
operation with no hashing.

##### Space Complexity: `O(1)`

The count array has a fixed size of `26` regardless of the input length, so the
auxiliary space is constant.

#### Key Insights

- Trades generality for speed: direct integer indexing avoids hash overhead.
- Achieves true `O(1)` space because the alphabet size is fixed in advance.
- Fails fast on the first negative slot rather than counting `t` in full.

### Sorting

```python
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        return sorted(s) == sorted(t)
```

#### Approach

This solution relies on a single observation: two strings are anagrams if and
only if they contain the same characters with the same frequencies. Sorting both
strings places their characters in a canonical order, so anagrams produce
identical sorted sequences. Comparing the two sorted lists yields the answer
directly, and unequal lengths naturally produce unequal lists.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n log n)`

Sorting each string costs `O(n log n)`, and the final list comparison is `O(n)`,
which the sort dominates.

##### Space Complexity: `O(n)`

`sorted` materializes a new list of characters for each string, requiring linear
additional space.

#### Key Insights

- Converts frequency matching into a canonical-form comparison through sorting.
- Cleaner to write than counting, at the cost of an `O(n log n)` sort rather than
  a linear pass.
- Scales naturally to Unicode because sorting assumes no fixed alphabet.

### Counter Comparison

```python
from collections import Counter


class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        return Counter(s) == Counter(t)
```

#### Approach

This solution defers the counting to Python's built-in `Counter`, which tallies
the occurrences of each element. Building a `Counter` from each string and
comparing the two for equality determines whether they hold the same characters
with the same frequencies. The equality check covers the length mismatch case for
free, since differing totals produce unequal counters.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Constructing each `Counter` traverses its string once, and comparing the two
counters for equality is linear in the number of distinct keys.

##### Space Complexity: `O(k)`

Each `Counter` stores at most `k` distinct characters, where `k` is the alphabet
size.

#### Key Insights

- The most concise solution, leaning entirely on the standard library.
- Matches the hand-written counter's complexity while hiding the bookkeeping.
- A clear case of reaching for the right built-in tool when one exists.

## Comparison of Solutions

### Time Complexity

- **Iterative Character Removal**: `O(n²)` - Each removal rescans and rebuilds `s`.
- **Set-based Counting**: `O(n * k)` - Repeated `count()` scans per distinct character.
- **Hash Map Count**: `O(n)` - One counting pass plus one cancelling pass.
- **Fixed Array Count**: `O(n)` - Two linear passes over fixed-size integer slots.
- **Sorting**: `O(n log n)` - Sorting each string dominates the comparison.
- **Counter Comparison**: `O(n)` - Linear construction and comparison of counters.

### Space Complexity

- **Iterative Character Removal**: `O(n)` - New string copies on each replacement.
- **Set-based Counting**: `O(k)` - The set holds the distinct characters.
- **Hash Map Count**: `O(k)` - Dictionary of distinct character frequencies.
- **Fixed Array Count**: `O(1)` - A constant 26-slot array regardless of input.
- **Sorting**: `O(n)` - A new sorted list of characters for each string.
- **Counter Comparison**: `O(k)` - Each counter stores the distinct characters.

### Trade-offs

- **Iterative Character Removal** reads as the definition itself but is too slow
  for large inputs because of repeated string copying.
- **Set-based Counting** trims comparisons to distinct characters yet pays for
  repeated `count()` scans.
- **Hash Map Count** balances linear time with portable, library-free code.
- **Fixed Array Count** pushes to optimal constant space by exploiting the fixed
  alphabet, at the cost of being tied to that alphabet.
- **Sorting** is short and assumption-free about the alphabet, trading a linear
  pass for an `O(n log n)` sort.
- **Counter Comparison** is the most concise, delegating all bookkeeping to the
  standard library.

### When to Use Each

- **Iterative Character Removal**: Educational use or tiny inputs where speed is
  irrelevant.
- **Set-based Counting**: Small inputs or when set operations read more naturally.
- **Hash Map Count**: Production code and interviews that want linear time in any
  language (recommended for cross-language work).
- **Fixed Array Count**: Hot paths over a known small alphabet where constant
  space and no hashing matter.
- **Sorting**: When brevity matters, the `O(n log n)` cost is acceptable, or the
  alphabet cannot be assumed fixed.
- **Counter Comparison**: Python code that values readability and concision.

### Optimization Notes

- The early length check short-circuits every approach before any real work.
- The Fixed Array Count demonstrates the time-space tradeoff at its extreme:
  swapping the dictionary for a fixed array buys constant space and removes
  hashing overhead.
- For the Unicode follow-up, the Hash Map Count, Counter Comparison, and Sorting
  scale without modification, while the Fixed Array Count must widen or replace
  its 26-slot array, and Iterative Character Removal and Set-based Counting
  degrade further as the alphabet grows.
- Iterative Character Removal's repeated `replace` is especially costly because
  strings are immutable, forcing a fresh allocation on every step.

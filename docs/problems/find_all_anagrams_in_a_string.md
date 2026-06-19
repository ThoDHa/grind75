# [Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/)

**Medium** | **20 minutes** | **String**

**Pattern:** [Sliding Window](../patterns/sliding_window/intuition.md)

**Practice:** [`practice/find_all_anagrams_in_a_string/solution.py`](https://github.com/ThoDHa/grind75/blob/main/practice/find_all_anagrams_in_a_string/solution.py)

Given two strings `s` and `p`, return an array of all the start indices of `p`'s anagrams in `s`. You may return the answer in any order.

An **anagram** is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.

## Examples

**Example 1:**

```
Input: s = "cbaebabacd", p = "abc"
Output: [0,6]
Explanation:
The substring with start index = 0 is "cba", which is an anagram of "abc".
The substring with start index = 6 is "bac", which is an anagram of "abc".
```

**Example 2:**

```
Input: s = "abab", p = "ab"
Output: [0,1,2]
Explanation:
The substring with start index = 0 is "ab", which is an anagram of "ab".
The substring with start index = 1 is "ba", which is an anagram of "ab".
The substring with start index = 2 is "ab", which is an anagram of "ab".
```

## Constraints

- `1 <= s.length, p.length <= 3 * 10^4`
- `s` and `p` consist of lowercase English letters only.

## Solutions

### Brute Force

```python
class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        n, k = len(s), len(p)
        if k > n:
            return []

        # Target frequency of p as a fixed 26-slot array (one per letter).
        need = [0] * 26
        for c in p:
            need[ord(c) - ord("a")] += 1

        result = []
        # Try every possible window start; the last valid start is n - k.
        for i in range(n - k + 1):
            window = [0] * 26
            # Count the characters of the window s[i:i+k] from scratch.
            for j in range(i, i + k):
                window[ord(s[j]) - ord("a")] += 1
            # A window is an anagram of p iff the two count arrays match.
            if window == need:
                result.append(i)

        return result
```

#### Approach

A substring of `s` is an anagram of `p` exactly when it has length `k = len(p)`
and the same multiset of characters. The most direct strategy tries every
possible window of width `k` and rebuilds its frequency count independently.

1. If `p` is longer than `s`, no anagram can exist, so return an empty list.
2. Build `need`, a fixed 26-slot array holding the frequency of each lowercase
   letter in `p`. Indexing by `ord(c) - ord('a')` maps `'a'..'z'` to `0..25`.
3. For each start index `i` from `0` to `n - k`, scan the `k` characters of the
   window `s[i:i+k]` and tally them into a fresh `window` array.
4. Compare `window` to `need`. Python compares the two 26-element lists slot by
   slot, so a match means the window is an anagram of `p`.
5. Append `i` on every match, then return the collected start indices.

This rebuilds the entire count for every window, doing no work-sharing between
overlapping windows, which makes it simple but redundant.

#### Time and Space Complexity Analysis

##### Time Complexity: `O((n - k + 1) * k)`

There are `n - k + 1` window positions, and each one fully recounts `k`
characters before a constant 26-slot comparison. In the worst case (`k ≈ n / 2`)
this is quadratic in `n`. Treating the per-window comparison as the dominant
fixed cost, the bound can also be written as `O(n * 26)` when `k` is small.

##### Space Complexity: `O(1)`

Both `need` and the per-window `window` array are fixed at 26 slots regardless
of input size. The `result` list is output, not auxiliary working space.

#### Key Insights

- Anagram detection reduces to comparing character frequency counts, since order
  does not matter.
- A fixed 26-slot array indexed by `ord(c) - ord('a')` replaces any imported
  counter and compares in constant time.
- The inefficiency comes from discarding each window's count and rebuilding the
  next from scratch, ignoring that adjacent windows differ by only two
  characters.

### Sliding Window with Fixed-Size Count Array

```python
class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        n, k = len(s), len(p)
        if k > n:
            return []

        need = [0] * 26
        window = [0] * 26
        for c in p:
            need[ord(c) - ord("a")] += 1

        # matches = how many of the 26 letters currently agree between
        # window and need. When matches == 26 the window is an anagram.
        matches = sum(1 for i in range(26) if need[i] == window[i])

        result = []
        for i in range(n):
            entering = ord(s[i]) - ord("a")
            # Add the incoming character, updating its match status in O(1).
            if window[entering] == need[entering]:
                matches -= 1
            window[entering] += 1
            if window[entering] == need[entering]:
                matches += 1

            # Once the window exceeds width k, drop the leftmost character.
            if i >= k:
                leaving = ord(s[i - k]) - ord("a")
                if window[leaving] == need[leaving]:
                    matches -= 1
                window[leaving] -= 1
                if window[leaving] == need[leaving]:
                    matches += 1

            # A full-width window with all 26 letters matching is an anagram.
            if i >= k - 1 and matches == 26:
                result.append(i - k + 1)

        return result
```

#### Approach

Adjacent windows overlap heavily: sliding one step removes a single character on
the left and adds a single character on the right. Rather than recounting, we
maintain the window's 26-slot count incrementally and track a running `matches`
value, the number of letters whose window count already equals the needed count.

1. If `p` is longer than `s`, return an empty list.
2. Build `need` and a zeroed `window`, both fixed 26-slot arrays, then initialize
   `matches` by comparing the two arrays slot by slot (initially the 26 zeros of
   `window` match every zero slot of `need`).
3. Walk `i` across `s`. For the entering character, adjust `matches` before and
   after incrementing its slot: a slot only counts as a match when the two values
   are equal, so we decrement `matches` if it was matching, bump the count, then
   increment `matches` if it now matches.
4. Once `i >= k`, the window has grown past width `k`, so apply the mirror update
   for the leaving character `s[i - k]`, keeping the window exactly `k` wide.
5. When the window is full width (`i >= k - 1`) and `matches == 26`, every letter
   agrees, so the window is an anagram; record its start index `i - k + 1`.

Each character's entry and exit touches a single slot and adjusts `matches` in
constant time, so the whole scan is linear.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each of the `n` characters enters the window once and leaves at most once. Every
entry and exit performs a constant number of array updates and `matches`
adjustments. There is no per-window 26-slot comparison because `matches` is
maintained incrementally, so the total work is linear in `n`.

##### Space Complexity: `O(1)`

The `need` and `window` arrays are fixed at 26 slots, and `matches` is a single
integer, all independent of input size. The `result` list is output rather than
auxiliary space.

#### Key Insights

- A fixed-size window fits perfectly because every anagram of `p` has exactly
  length `k`.
- Maintaining counts incrementally turns the brute force's repeated `O(k)`
  recount into `O(1)` per slide.
- The `matches` counter avoids re-comparing all 26 slots each step: only the one
  or two slots that actually change can flip a letter's match status.
- Indexing a 26-slot array by `ord(c) - ord('a')` removes the need for any
  imported counter while keeping every operation constant time.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O((n - k + 1) * k)` because each of the
  `n - k + 1` windows is recounted from scratch over `k` characters.
- **Sliding Window**: `O(n)` because each character enters and leaves the window
  exactly once with constant-time updates.

### Space Complexity

- **Brute Force**: `O(1)`, using only fixed 26-slot arrays.
- **Sliding Window**: `O(1)`, also using fixed 26-slot arrays plus a single
  integer counter.

Both approaches use constant auxiliary space; they differ only in time.

### Trade-offs

- The brute force is the easiest to reason about: build a count, compare, repeat.
  Its cost is the repeated work across overlapping windows, which becomes
  quadratic when `k` is a large fraction of `n`.
- The sliding window adds the bookkeeping of incremental updates and a `matches`
  counter, trading a little extra logic for a linear runtime that scales to the
  largest allowed inputs.

### When to Use Each

- **Brute Force**: Suitable when `s` is short, `p` is tiny, or clarity matters
  more than speed, such as a first pass or a teaching example.
- **Sliding Window**: Preferred for any sizeable input and for the constraint
  ceiling of `3 * 10^4`, where the quadratic approach risks being too slow.

### Optimization Notes

- The key optimization is recognizing that consecutive windows share all but two
  characters, so the count can be updated rather than rebuilt.
- The `matches` counter is a second-level optimization: it replaces an `O(26)`
  full-array comparison per window with `O(1)` adjustments to a single integer.
- Mapping letters to a fixed 26-slot array (via `ord(c) - ord('a')`) keeps the
  solution import-free and makes every count operation constant time.

# [Longest Substring Without Repeating Characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/)

**Medium** | **25 minutes** | **Hash Table, String, Sliding Window**

**Pattern:** [Sliding Window](../patterns/sliding_window/intuition.md)

**Practice:** [`practice/longest_substring_without_repeating_characters/solution.py`](https://github.com/ThoDHa/grind75/blob/main/practice/longest_substring_without_repeating_characters/solution.py)

Given a string `s`, find the length of the longest substring without repeating characters.

## Examples

### Example 1

**Input:** `s = "abcabcbb"`

**Output:** `3`

**Explanation:** The answer is "abc", with the length of 3.

### Example 2

**Input:** `s = "bbbbb"`

**Output:** `1`

**Explanation:** The answer is "b", with the length of 1.

### Example 3

**Input:** `s = "pwwkew"`

**Output:** `3`

**Explanation:** The answer is "wke", with the length of 3.
Notice that the answer must be a substring, "pwke" is a subsequence and not a substring.

### Example 4

**Input:** `s = ""`

**Output:** `0`

## Constraints

- `0 <= s.length <= 5 * 10^4`
- `s` consists of English letters, digits, symbols and spaces.

## Solutions

### Sliding Window with Set

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        # Tracks the characters currently inside the window
        seen = set()
        longest = 0
        left = 0

        for right in range(len(s)):
            # If the new character duplicates one in the window, shrink from the
            # left one step at a time until that duplicate is removed
            while s[right] in seen:
                seen.remove(s[left])
                left += 1
            seen.add(s[right])
            longest = max(longest, right - left + 1)

        return longest
```

#### Approach

We maintain a sliding window `[left, right]` whose characters are kept in a set,
guaranteeing the window never holds a duplicate. The `right` pointer expands the
window one character at a time. Whenever the incoming character already lives in
the window, we advance `left` one step at a time, removing each evicted
character from the set, until the duplicate has been dropped.

1. Initialize an empty `seen` set, `longest = 0`, and `left = 0`.
2. Move `right` across each character of `s`.
3. While the character at `right` is already in `seen`, remove `s[left]` from the
   set and advance `left`.
4. Add the character at `right` to `seen`.
5. The window length `right - left + 1` is a candidate for `longest`.
6. Return `longest`.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2n)`

Each character is added to the set once by `right` and removed at most once by
`left`. In the worst case the pointers together traverse the string twice, which
is linear, written here as `O(2n)` to make the double traversal explicit.

##### Space Complexity: `O(min(n, charset))`

The set holds at most one entry per distinct character in the window, bounded by
both the string length and the size of the character set.

#### Key Insights

- A set gives `O(1)` average membership tests, which is exactly what the
  duplicate check needs.
- The `left` pointer only ever moves forward, so although there is a nested
  `while`, the total movement is bounded and the pass stays linear.
- This is the most fundamental form of the sliding window: it shrinks one
  character at a time rather than jumping.

### Sliding Window with Last-Seen Index

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        # Maps each character to the index where it was last seen
        last_seen = {}
        longest = 0
        left = 0

        for right, char in enumerate(s):
            # If we have seen char inside the current window, jump the left
            # edge just past its previous occurrence
            if char in last_seen and last_seen[char] >= left:
                left = last_seen[char] + 1
            last_seen[char] = right
            longest = max(longest, right - left + 1)

        return longest
```

#### Approach

We maintain a sliding window `[left, right]` that always holds a substring with
no repeated characters. The `right` pointer scans forward one character at a
time, and the `left` pointer jumps forward whenever a repeat would enter the
window.

The key is a hash map `last_seen` that records the most recent index of each
character. When the current character has been seen at an index that falls
inside the current window, the window must shrink from the left past that
occurrence.

1. Initialize an empty `last_seen` map, `longest = 0`, and `left = 0`.
2. Iterate `right` over each character `char` in `s`.
3. If `char` is in `last_seen` and its stored index is at or after `left`, it
   lies inside the window, so set `left = last_seen[char] + 1`.
4. Update `last_seen[char]` to the current index `right`.
5. The current window length is `right - left + 1`; update `longest` with it.
6. Return `longest`.

The guard `last_seen[char] >= left` is essential: a character may exist in the
map from a position that has already been passed by `left`, and that stale entry
must not drag `left` backward.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each character is visited once by `right`, and `left` only ever moves forward.
Every hash map lookup and update is `O(1)` on average, so the total work is
linear in the length of `s`.

##### Space Complexity: `O(min(n, m))`

The map stores at most one entry per distinct character. Its size is bounded by
both the length `n` and the size `m` of the character set (English letters,
digits, symbols, and spaces), giving `O(min(n, m))`.

#### Key Insights

- A "without repeating characters" constraint maps directly onto a sliding
  window that never contains a duplicate.
- Storing the last-seen index lets `left` jump in one step instead of shrinking
  the window one character at a time, which keeps the pass linear.
- The `>= left` check prevents stale indices outside the window from incorrectly
  rewinding `left`.
- Both pointers move only forward, so despite the nested feel there is no
  quadratic blowup.

## Comparison of Solutions

### Time Complexity

- **Sliding Window with Set**: `O(2n)` - Each character is added once and removed at most once as the window shrinks step by step
- **Sliding Window with Last-Seen Index**: `O(n)` - `left` jumps directly past duplicates, so each character is touched a single time

### Space Complexity

- **Sliding Window with Set**: `O(min(n, charset))` - The set holds at most one entry per distinct character in the window
- **Sliding Window with Last-Seen Index**: `O(min(n, m))` - The map holds at most one entry per distinct character

### Trade-offs

- The set version is the most direct expression of the idea: shrink the window one character at a time until it is valid again, which is easy to reason about
- The last-seen-index version trades a slightly more subtle invariant (the `>= left` guard) for the ability to skip `left` forward in one move, halving the constant factor

### When to Use Each

- **Sliding Window with Set**: When clarity matters most, or when first learning the sliding-window pattern
- **Sliding Window with Last-Seen Index**: For the tightest single-pass solution, especially in interviews where the index jump is a desirable optimization to demonstrate

### Optimization Notes

- Both solutions are linear; the difference is purely in the constant factor, since the set version may revisit characters as `left` advances
- The last-seen-index map subsumes the set: it stores positions rather than mere presence, which is exactly what enables the forward jump
- The crucial correctness detail in the index version is the `last_seen[char] >= left` guard, which prevents a stale index from dragging `left` backward

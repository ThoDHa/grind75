# [Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/)

**Medium** | **25 minutes** | **String, Dynamic Programming**

**Pattern:** [String DP](../patterns/string_dp/intuition.md)

**Practice:** [`practice/longest_palindromic_substring/solution.py`](../../practice/longest_palindromic_substring/solution.py)

Given a string `s`, return the longest palindromic substring in `s`.

## Examples

### Example 1

**Input:** `s = "babad"`

**Output:** `"bab"`

**Explanation:** `"aba"` is also a valid answer.

### Example 2

**Input:** `s = "cbbd"`

**Output:** `"bb"`

## Constraints

- `1 <= s.length <= 1000`
- `s` consist of only digits and English letters.

## Solutions

### Brute Force

```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        n = len(s)

        def is_palindrome(left: int, right: int) -> bool:
            # Walk inward from both ends, comparing mirrored characters.
            while left < right:
                if s[left] != s[right]:
                    return False
                left += 1
                right -= 1
            return True

        start, max_len = 0, 0
        # Try every substring s[i..j] and keep the longest palindrome.
        for i in range(n):
            for j in range(i, n):
                if j - i + 1 > max_len and is_palindrome(i, j):
                    start, max_len = i, j - i + 1

        return s[start:start + max_len]
```

#### Approach

The most direct idea is to look at every possible substring and check whether it
reads the same forwards and backwards, remembering the longest one that does. A
substring is a palindrome exactly when its mirrored characters all match, which a
simple inward two-pointer walk verifies by hand.

1. For each start index `i`, consider every end index `j >= i`, covering all
   `O(n^2)` substrings.
2. Before paying for a palindrome check, skip any substring no longer than the
   best found so far, since it cannot improve the answer.
3. Check `s[i..j]` with `is_palindrome`, which compares `s[left]` and `s[right]`
   while walking the two pointers toward the middle.
4. When a longer palindrome is found, record its start and length, and finally
   return the recorded slice `s[start:start + max_len]`.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^3)`

There are `O(n^2)` substrings, and each palindrome check walks up to `O(n)`
characters, giving `O(n^3)` in the worst case (for example, a string of identical
characters where every check runs to completion).

##### Space Complexity: `O(1)`

Only a handful of integer indices are tracked. The returned substring is output,
not auxiliary working space.

#### Key Insights

- Enumerating all substrings and verifying each one by hand needs no insight
  about palindrome structure, making it the most self-derivable approach.
- The length guard (`j - i + 1 > max_len`) prunes substrings that cannot beat the
  current best, a cheap optimization that does not change the asymptotic bound.
- The cubic cost comes from re-checking overlapping substrings from scratch; every
  later approach removes this redundancy by reusing already-verified work.

### Bottom-Up DP

```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        if n < 2:
            return s

        # dp[i][j] is True when the substring s[i..j] (inclusive) is a palindrome.
        dp = [[False] * n for _ in range(n)]
        start, max_len = 0, 1

        # Base case: every single character is a palindrome.
        for i in range(n):
            dp[i][i] = True

        # Fill by increasing length, since dp[i][j] depends on dp[i+1][j-1].
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                if s[i] != s[j]:
                    continue
                # Length-2 spans have no inner substring; longer ones defer to it.
                if length == 2 or dp[i + 1][j - 1]:
                    dp[i][j] = True
                    if length > max_len:
                        start, max_len = i, length

        return s[start:start + max_len]
```

#### Approach

Define `dp[i][j]` to be `True` when the substring `s[i..j]` (inclusive) is a
palindrome. A substring is a palindrome exactly when its two ends match and the
inside is already known to be a palindrome, which gives the recurrence:

`dp[i][j] = (s[i] == s[j]) and (j - i < 2 or dp[i + 1][j - 1])`

Because `dp[i][j]` depends on the shorter substring `dp[i + 1][j - 1]`, we fill the
table in increasing order of substring length so every dependency is ready first.

1. Seed every single character as a palindrome (`dp[i][i] = True`).
2. For each `length` from 2 to `n`, scan all start indices `i` and set `j = i + length - 1`.
3. When `s[i] == s[j]` and either the span is length 2 or the inner substring is a
   palindrome, mark `dp[i][j]` and update the best `(start, max_len)` seen so far.
4. Return the recorded slice `s[start:start + max_len]`.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Filling the `n × n` table touches each `(i, j)` pair once with constant work per cell.

##### Space Complexity: `O(n^2)`

The `dp` table stores `n × n` boolean entries.

#### Key Insights

- The recurrence builds longer palindromes from shorter verified ones, the hallmark
  of dynamic programming.
- Iterating by substring length guarantees `dp[i + 1][j - 1]` is computed before
  `dp[i][j]` needs it.
- The length-2 base case (`j - i < 2`) covers adjacent equal characters that have no
  inner substring to consult.
- This trades `O(n^2)` space for an explicit, tabular view of which substrings are
  palindromes, useful when the full palindrome table is itself the goal.

### Expand Around Center

```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        # Track the bounds of the best palindrome found so far
        start, end = 0, 0

        def expand(left: int, right: int) -> tuple[int, int]:
            # Grow outward while the characters keep matching
            while left >= 0 and right < len(s) and s[left] == s[right]:
                left -= 1
                right += 1
            # Step back to the last valid (inclusive) bounds
            return left + 1, right - 1

        for i in range(len(s)):
            # Odd-length palindrome centered on a single character
            l1, r1 = expand(i, i)
            if r1 - l1 > end - start:
                start, end = l1, r1
            # Even-length palindrome centered between two characters
            l2, r2 = expand(i, i + 1)
            if r2 - l2 > end - start:
                start, end = l2, r2

        return s[start:end + 1]
```

#### Approach

A palindrome mirrors around its center. Every palindromic substring has a
center, but that center is either a single character (odd length, like `"aba"`)
or the gap between two characters (even length, like `"bb"`). There are `n`
single-character centers and `n - 1` gap centers, so `2n - 1` centers in total.

The idea is to try every possible center and expand outward as long as the
characters on both sides match, recording the longest palindrome seen.

1. Define a helper `expand(left, right)` that walks the two pointers outward
   while they stay in bounds and `s[left] == s[right]`.
2. When the loop stops, the pointers have overshot by one, so return
   `(left + 1, right - 1)` as the inclusive bounds of the matched palindrome.
3. For each index `i`, expand once with `(i, i)` for the odd case and once with
   `(i, i + 1)` for the even case.
4. Track the widest `(start, end)` window across all expansions using
   `r - l > end - start` as the comparison.
5. Return the slice `s[start:end + 1]`.

Comparing widths with `r - l` avoids recomputing lengths and naturally keeps the
first-found palindrome when ties occur, which is acceptable since any longest
palindromic substring is a valid answer.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

There are `2n - 1` centers, and each expansion can extend up to `O(n)` steps in
the worst case (for example, a string of identical characters like `"aaaa"`).
The product gives `O(n^2)`.

##### Space Complexity: `O(1)`

Only a constant number of integer pointers are used. The returned substring is
output, not auxiliary working space, so the extra space is constant.

#### Key Insights

- Every palindrome is defined by its center, so iterating over `2n - 1` centers
  covers all palindromes without enumerating substrings explicitly.
- Handling odd and even lengths separately with `(i, i)` and `(i, i + 1)` is the
  clean way to capture both forms with one helper.
- Expanding outward stops the moment a mismatch appears, so most centers do far
  less than `O(n)` work in practice.
- Tracking bounds instead of the substring itself keeps each comparison `O(1)`
  and defers the single slice to the very end.

### Manacher's Algorithm

```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        if not s:
            return ""

        # Transform "abc" into "^#a#b#c#$": the interleaved '#' makes every
        # palindrome odd-length, and the '^'/'$' sentinels never match each
        # other so expansion stops at the boundaries without index checks.
        t = "^#" + "#".join(s) + "#$"
        n = len(t)

        # p[i] is the radius of the palindrome centered at i in the transformed
        # string; that radius equals the length of the corresponding palindrome
        # in the original string.
        p = [0] * n

        # center/right describe the rightmost-reaching palindrome found so far.
        center, right = 0, 0
        for i in range(1, n - 1):
            mirror = 2 * center - i
            if i < right:
                # Reuse the mirror's radius, but never claim more than what the
                # current palindrome already guarantees up to its right edge.
                p[i] = min(right - i, p[mirror])
            # Attempt to grow past the reused portion.
            while t[i + p[i] + 1] == t[i - p[i] - 1]:
                p[i] += 1
            if i + p[i] > right:
                center, right = i, i + p[i]

        max_radius = max(p)
        center_idx = p.index(max_radius)
        start = (center_idx - max_radius) // 2
        return s[start:start + max_radius]
```

#### Approach

Manacher's algorithm achieves linear time by never re-examining characters it
already knows to match. It first transforms the string so that odd- and
even-length palindromes are handled uniformly, then reuses palindrome symmetry
to give each new center a head start.

1. Transform `s` into `t` by inserting `#` between every character and wrapping
   it in `^` and `$` sentinels (for example `"aba"` becomes `"^#a#b#a#$"`). Now
   every palindrome in `t` is odd-length, and the distinct sentinels stop any
   expansion at the boundaries.
2. Keep `p[i]`, the radius of the palindrome centered at `i` in `t`, along with
   the `center`/`right` of the rightmost-reaching palindrome found so far.
3. For each `i`, find its `mirror = 2 * center - i`. If `i` lies inside the
   current palindrome (`i < right`), seed `p[i]` with `min(right - i, p[mirror])`,
   borrowing the mirror's work without overstepping the known right edge.
4. Expand from this seed while the characters straddling `i` still match. The
   sentinels guarantee the inner `while` halts without explicit bounds checks.
5. If the new palindrome extends past `right`, update `center` and `right`.
6. The largest radius is the answer's length; convert its center back to the
   original index with `start = (center_idx - max_radius) // 2`.

The radius in the transformed string equals the palindrome length in the
original string, which is why `max_radius` doubles as both the length and the
slice width.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

The transformed string has length `2n + 3`. The `right` boundary only ever moves
forward, and each inner expansion step advances it, so across the whole run the
total expansion work is bounded by `O(n)`.

##### Space Complexity: `O(n)`

The transformed string `t` and the radius array `p` each hold `O(n)` entries.

#### Key Insights

- Interleaving `#` characters removes the odd/even special-casing that the other
  approaches handle with two separate expansions per center.
- The mirror trick reuses already-computed radii so that characters inside the
  current rightmost palindrome are never compared twice.
- The `^` and `$` sentinels make the expansion loop boundary-safe, eliminating
  index range checks entirely.
- The radius in the padded string maps directly to the substring length, so the
  final slice falls out of a single index computation.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n^3)` - `O(n^2)` substrings, each checked in up to `O(n)`.
- **Bottom-Up DP**: `O(n^2)` - fills every `(i, j)` cell once.
- **Expand Around Center**: `O(n^2)` - `2n - 1` centers, each expanding up to `O(n)`.
- **Manacher's Algorithm**: `O(n)` - the right boundary only moves forward, bounding total work.

### Space Complexity

- **Brute Force**: `O(1)` - only a few integer indices.
- **Bottom-Up DP**: `O(n^2)` - the full boolean substring table.
- **Expand Around Center**: `O(1)` - only a few integer pointers.
- **Manacher's Algorithm**: `O(n)` - the padded string and the radius array.

### Trade-offs

- The Brute Force approach is the simplest to derive, checking every substring
  directly, but pays a cubic price by re-verifying overlapping substrings from scratch.
- The Bottom-Up DP approach makes the palindrome relationships explicit in a
  table that is straightforward to reason about, at the cost of quadratic memory.
- The Expand Around Center approach matches the time bound with constant space and
  often stops early on most centers, though its center-expansion invariant is a
  little less obvious than a filled table.
- Manacher's Algorithm reaches the optimal `O(n)` time but pays for it in
  conceptual complexity: the string transform, mirror reuse, and index
  back-conversion are easy to get subtly wrong under interview pressure.

### When to Use Each

- **Brute Force**: As a baseline to confirm correctness, or when `n` is tiny and
  clarity outweighs efficiency.
- **Bottom-Up DP**: When the tabular formulation is clearer to derive, or when
  the palindrome table itself is needed for a related subproblem.
- **Expand Around Center**: For the best space usage and the simplest fast solution in
  practice; the recommended interview answer.
- **Manacher's Algorithm**: When `O(n)` time is genuinely required on very large
  inputs and the extra implementation cost is justified.

### Optimization Notes

- Brute Force drops a full factor of `n` by moving from re-checking every substring
  to either of the `O(n^2)` approaches, which reuse already-verified palindromes.
- Bottom-Up DP and Expand Around Center share the `O(n^2)` time floor; the difference
  is purely `O(n^2)` versus `O(1)` space.
- Expand Around Center stops each expansion at the first mismatch, so it usually does
  less than the worst-case work, whereas the table always does the full `O(n^2)`.
- Manacher's Algorithm is the only sub-quadratic option here; its `#`-padding trick
  also unifies the odd/even cases that the other approaches handle separately.

# [Longest Palindrome](https://leetcode.com/problems/longest-palindrome/)

**Easy** | **15 minutes** | **String, Hash Table, Greedy**

**Pattern:** [Hashing & Frequency Counting](../patterns/hashing/intuition.md)

**Practice:** [`practice/longest_palindrome/solution.py`](../../practice/longest_palindrome/solution.py)

Given a string `s` which consists of lowercase or uppercase letters, return the length of the longest palindrome that can be built with those letters.

Letters are case sensitive, for example, "Aa" is not considered a palindrome here.

## Examples

### Example 1

**Input:** `s = "abccccdd"`

**Output:** `7`

**Explanation:** One longest palindrome that can be built is "dccaccd", whose length is 7.

### Example 2

**Input:** `s = "a"`

**Output:** `1`

### Example 3

**Input:** `s = "bb"`

**Output:** `2`

## Constraints

- `1 <= s.length <= 2000`
- `s` consists of lowercase and/or uppercase English letters only.

## Solutions

### Brute Force

```python
class Solution:
    def longestPalindrome(self, s: str) -> int:
        # Count each character by hand with a plain dictionary
        counts = {}
        for c in s:
            counts[c] = counts.get(c, 0) + 1

        length = 0
        has_odd = False
        for count in counts.values():
            # Every full pair contributes two characters to the palindrome
            length += (count // 2) * 2
            # A leftover single character means this count is odd
            if count % 2 == 1:
                has_odd = True

        # One leftover character can sit in the center
        if has_odd:
            length += 1
        return length
```

#### Approach

The most direct idea follows straight from how a palindrome is built: characters mirror around the center, so each character can contribute only in pairs, except for a single character allowed in the middle. Counting how many of each character we have and then taking as many pairs as possible answers the question without ever constructing a palindrome.

1. Count the frequency of every character with a plain dictionary.
2. For each frequency, add its largest even part `(count // 2) * 2` to the running length, because only complete pairs can mirror across the palindrome.
3. Record whether any frequency is odd, since an odd frequency leaves one unpaired character.
4. If any odd frequency was seen, add `1` for a single center character.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

- Counting every character is one `O(n)` pass over the string of length `n`.
- Iterating the frequency values is `O(k)` where `k` is the number of distinct characters, bounded by the constant alphabet size.
- The total work is therefore linear in the input.

##### Space Complexity: `O(1)`

- The dictionary holds at most `52` entries (`26` lowercase + `26` uppercase English letters).
- This bound is constant regardless of input size, so the auxiliary space is constant.

#### Key Insights

- A palindrome mirrors around its center, so each character contributes only in pairs.
- Exactly one odd-frequency character can be placed in the center, which is why a single `+1` covers all the leftovers.
- Computing the answer from counts alone avoids ever building the palindrome string.
- Taking `(count // 2) * 2` cleanly drops any single unpaired character from each group.

#### Walkthrough

Let us trace the Brute Force solution on Example 1: `s = "abccccdd"`, expected Output `7`.

First pass: count each character with the dictionary. We read the string left to right, bumping `counts[c]` by one each time:

| Step | Char read | `counts` after |
|------|-----------|----------------|
| 1 | `a` | `{a: 1}` |
| 2 | `b` | `{a: 1, b: 1}` |
| 3 | `c` | `{a: 1, b: 1, c: 1}` |
| 4 | `c` | `{a: 1, b: 1, c: 2}` |
| 5 | `c` | `{a: 1, b: 1, c: 3}` |
| 6 | `c` | `{a: 1, b: 1, c: 4}` |
| 7 | `d` | `{a: 1, b: 1, c: 4, d: 1}` |
| 8 | `d` | `{a: 1, b: 1, c: 4, d: 2}` |

So the final counts are `a: 1`, `b: 1`, `c: 4`, `d: 2`.

Second pass: walk the counts, adding the even part `(count // 2) * 2` to `length` and flipping `has_odd` whenever a count is odd. Both `length` and `has_odd` start at `0` and `False`:

| Char | `count` | `(count // 2) * 2` added | `length` | `count % 2 == 1`? | `has_odd` |
|------|---------|--------------------------|----------|-------------------|-----------|
| `a` | 1 | 0 | 0 | yes | True |
| `b` | 1 | 0 | 0 | yes | True |
| `c` | 4 | 4 | 4 | no | True |
| `d` | 2 | 2 | 6 | no | True |

After the loop `length` is `6` and `has_odd` is `True`. Because `has_odd` is `True`, one leftover character (here `a` or `b`) can sit in the center, so we add `1`: `length` becomes `7`.

The function returns `7`, which matches the example's expected Output.

### Set-based Pair Matching

```python
class Solution:
    def longestPalindrome(self, s: str) -> int:
        chars = set()
        count = 0

        for c in s:
            if c in chars:
                chars.remove(c)
                count += 2
            else:
                chars.add(c)

        # If we have any characters left, one can be used as center
        if chars:
            count += 1

        return count
```

#### Approach

This solution uses a set to track unpaired characters as it processes the string:

1. For each character in the string:
    - If it's already in the set, we've found a pair. Remove it from the set and increase count by 2.
    - If it's not in the set, add it to the set as a potential future pair.
2. After processing all characters, if the set is not empty (meaning we have unpaired characters), we can use one character as the center of the palindrome.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

- We iterate through the string once, performing `O(1)` operations (set insertion, lookup, removal) for each character.
- Since set operations are generally `O(1)`, the overall time complexity is `O(n)`.

##### Space Complexity: `O(1)`

- The set stores at most one of each unique character, which is bounded by the size of the character set (`52` letters).
- Since this upper bound is constant regardless of input size, the space complexity is `O(1)`.

#### Key Insights

- This approach elegantly tracks character pairs without explicit counting.
- The set effectively serves as a "pairing station" - characters wait there until their pair arrives.
- The final check for a non-empty set determines if we can place one character at the center.
- This solution is particularly intuitive for understanding the palindrome construction process.

### Character Frequency Counting with Odd Character Tracking

```python
class Solution:
    def longestPalindrome(self, s: str) -> int:
        counter = {}
        odd = -1
        # Count frequency of each character
        for c in s:
            counter[c] = counter.get(c, 0) + 1

        # Count characters with odd frequencies
        for values in counter.values():
            if values % 2 != 0:
               odd += 1

        # Calculate palindrome length
        if odd > 0:
            return len(s) - odd
        else:
            return len(s)
```

#### Approach

This refinement of the brute force avoids the explicit pair arithmetic by working backward from `len(s)`. Every odd-frequency character forces one unpaired character to be discarded, except that one of them may sit in the center:

1. Create a hash map (dictionary) to store the count of each character.
2. Initialize an odd counter at `-1`, which pre-credits one odd character as the allowed center.
3. After counting characters, iterate through the values to count how many have an odd frequency.
4. Calculate the palindrome length:
    - If `odd > 0`: subtract that many characters from the total length, having already kept one odd character for the center.
    - If `odd = 0`: all characters pair up and the whole string is usable.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

- Counting the frequency of each character requires `O(n)` time where `n` is the length of the string.
- Iterating through the counter values is `O(k)` where `k` is the number of unique characters, which is bounded by the constant size of the character set.
- Since `k ≤ n`, the overall time complexity is `O(n)`.

##### Space Complexity: `O(1)`

- The counter dictionary stores at most `52` key-value pairs (`26` lowercase + `26` uppercase English letters).
- Since the size of the counter is bounded by a constant regardless of input size, the space complexity is `O(1)`.

#### Key Insights

- In a palindrome, most characters must appear in pairs (one on each side).
- At most one character can appear an odd number of times (placed in the center).
- The `odd = -1` initialization is a clever way to account for the fact that one odd-frequency character can be fully utilized.
- This approach efficiently handles the palindrome construction without explicitly building the string.

### Counter Frequency Tally

```python
from collections import Counter


class Solution:
    def longestPalindrome(self, s: str) -> int:
        counts = Counter(s)
        length = 0
        has_odd = False
        for freq in counts.values():
            length += freq - (freq & 1)
            if freq & 1:
                has_odd = True
        return length + 1 if has_odd else length
```

#### Approach

This solution leans on `collections.Counter` to tally character frequencies, then derives the answer directly from those counts:

1. Build a `Counter` over `s`, mapping each character to its frequency.
2. For each frequency, add its largest even part (`freq - (freq & 1)`) to the running length, since pairs of characters always contribute to a palindrome.
3. Track whether any character has an odd frequency with `has_odd`.
4. If at least one odd frequency exists, a single leftover character can sit at the center, so add `1` to the result.

The bitwise `freq & 1` is `1` when `freq` is odd and `0` when even, which both detects odd counts and trims the unpaired character off each odd group in a single expression.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

- Building the `Counter` is a single `O(n)` pass over the string.
- Iterating the frequency values is `O(k)` where `k` is the number of distinct characters, bounded by the constant alphabet size.
- The overall time complexity is therefore `O(n)`.

##### Space Complexity: `O(1)`

- The `Counter` holds at most `52` entries (`26` lowercase + `26` uppercase letters).
- This bound is constant regardless of input size, so the space complexity is `O(1)`.

#### Key Insights

- `Counter` removes the manual frequency-counting boilerplate while preserving the same underlying logic.
- The even part of any count contributes fully to the palindrome; only the odd remainder is at risk.
- A single center slot is available whenever any character has an odd count, captured cleanly by the `has_odd` flag.
- `freq & 1` doubles as both an odd-parity test and the amount to subtract, keeping the loop body compact.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n)` - One pass to count characters, one pass over the bounded set of distinct counts
- **Set-based Pair Matching**: `O(n)` - Single-pass approach with constant-time set operations
- **Character Frequency Counting with Odd Character Tracking**: `O(n)` - One pass to count characters and another to process counts
- **Counter Frequency Tally**: `O(n)` - One pass to build the `Counter`, one pass over the bounded set of distinct counts

### Space Complexity

- **Brute Force**: `O(1)` - Uses a dictionary bounded by the character set size
- **Set-based Pair Matching**: `O(1)` - Uses a set bounded by the character set size
- **Character Frequency Counting with Odd Character Tracking**: `O(1)` - Uses a dictionary bounded by the character set size
- **Counter Frequency Tally**: `O(1)` - Uses a `Counter` bounded by the character set size

### Trade-offs

- Brute Force is fully library-free and spells out the pair arithmetic directly, making it the clearest derivation of the answer.
- Set-based Pair Matching has a cleaner single-pass implementation and may be easier to understand conceptually, tracking pairs as they form.
- Character Frequency Counting trims the arithmetic by working backward from `len(s)`, using the `odd = -1` pre-credit to handle the center character implicitly.
- Counter Frequency Tally is the most concise, delegating the counting step to `collections.Counter` while keeping the palindrome arithmetic identical to the manual version.
- All four solutions handle the core requirement efficiently: determining the maximum palindrome length without building the actual palindrome.

### When to Use Each

- **Brute Force**: Preferred as the most direct, library-free derivation, or when the explicit pair-and-center logic aids understanding.
- **Set-based Pair Matching**: Preferred for readability and when solution simplicity is valued over minor optimizations.
- **Character Frequency Counting with Odd Character Tracking**: Preferred when you want a library-free solution and like deriving the answer by subtracting odd leftovers from the full length.
- **Counter Frequency Tally**: Preferred in production Python where `collections.Counter` is available and brevity is valued (Recommended for idiomatic code).

### Optimization Notes

- All four solutions are already optimal in terms of time and space complexity.
- The odd counter initialization in Character Frequency Counting is a clever way to absorb the center character without an extra conditional.
- Set-based Pair Matching demonstrates how using appropriate data structures can lead to elegant algorithmic solutions.
- Counter Frequency Tally uses `freq & 1` to fuse the odd-parity test with the unpaired-character subtraction, trimming the loop body to a single arithmetic step.
- In practice, all four solutions perform similarly for the constraints given.

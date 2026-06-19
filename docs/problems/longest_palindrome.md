# [Longest Palindrome](https://leetcode.com/problems/longest-palindrome/)

**Easy** | **15 minutes** | **String, Hash Table, Greedy**

**Pattern:** [Hashing & Frequency Counting](../patterns/hashing/intuition.md)

**Practice:** [`practice/longest_palindrome/solution.py`](https://github.com/ThoDHa/grind75/blob/main/practice/longest_palindrome/solution.py)

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

This solution counts the frequency of each character and specifically tracks how many characters appear an odd number of times:

1. Create a hash map (dictionary) to store the count of each character.
2. Initialize an odd counter at -1 (this clever initialization handles the first odd count character differently).
3. After counting characters, iterate through the values to count how many have odd frequency.
4. Calculate the palindrome length by:
    - If odd > 0: subtract the number of odd counts from the total length (after accounting for one central character)
    - If odd = 0: all characters can be used in the palindrome

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
- The odd = -1 initialization is a clever way to account for the fact that one odd frequency character can be fully utilized.
- This approach efficiently handles the palindrome construction without explicitly building the string.

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

- **Character Frequency Counting with Odd Character Tracking**: `O(n)` - Requires one pass to count characters and another to process counts
- **Set-based Pair Matching**: `O(n)` - Single-pass approach with constant-time set operations
- **Counter Frequency Tally**: `O(n)` - One pass to build the `Counter`, one pass over the bounded set of distinct counts

### Space Complexity

- **Character Frequency Counting with Odd Character Tracking**: `O(1)` - Uses a dictionary bounded by the character set size
- **Set-based Pair Matching**: `O(1)` - Uses a set bounded by the character set size
- **Counter Frequency Tally**: `O(1)` - Uses a `Counter` bounded by the character set size

### Trade-offs

- Character Frequency Counting is fully library-free and makes the odd-count handling explicit through its manual loop.
- Set-based Pair Matching has a cleaner implementation and may be easier to understand conceptually, tracking pairs as they form.
- Counter Frequency Tally is the most concise, delegating the counting step to `collections.Counter` while keeping the palindrome arithmetic identical to the manual version.
- All three solutions handle the core requirement efficiently: determining the maximum palindrome length without building the actual palindrome.

### When to Use Each

- **Character Frequency Counting with Odd Character Tracking**: Preferred when you want a library-free solution or might need the actual character frequencies for other operations.
- **Set-based Pair Matching**: Preferred for readability and when solution simplicity is valued over minor optimizations.
- **Counter Frequency Tally**: Preferred in production Python where `collections.Counter` is available and brevity is valued (Recommended for idiomatic code).

### Optimization Notes

- All three solutions are already optimal in terms of time and space complexity.
- The odd counter initialization in Character Frequency Counting is a clever way to avoid additional conditionals.
- Set-based Pair Matching demonstrates how using appropriate data structures can lead to elegant algorithmic solutions.
- Counter Frequency Tally uses `freq & 1` to fuse the odd-parity test with the unpaired-character subtraction, trimming the loop body to a single arithmetic step.
- In practice, all three solutions perform similarly for the constraints given.

# [Longest Palindrome](https://leetcode.com/problems/longest-palindrome/)

Easy - 15 minutes - String, Hash Table, Greedy

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

### Solution 1: Character Frequency Counting with Odd Character Tracking

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

### Solution 2: Set-based Pair Matching

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

### Comparison of Solutions

#### Time Complexity

- **Solution 1 (Frequency Counting)**: `O(n)` - Requires one pass to count characters and another to process counts
- **Solution 2 (Set-based Pairing)**: `O(n)` - Single-pass approach with constant-time set operations

#### Space Complexity

- **Solution 1 (Frequency Counting)**: `O(1)` - Uses a dictionary bounded by the character set size
- **Solution 2 (Set-based Pairing)**: `O(1)` - Uses a set bounded by the character set size

#### Trade-offs

- Solution 1 is slightly more memory-efficient for strings with many duplicate characters as it stores only character counts.
- Solution 2 has a cleaner implementation and may be easier to understand conceptually.
- Both solutions handle the core requirements efficiently: determining the maximum palindrome length without building the actual palindrome.

#### When to Use Each

- **Solution 1**: Preferred when you might need the actual character frequencies for other operations or when memory efficiency is a concern.
- **Solution 2**: Preferred for readability and when solution simplicity is valued over minor optimizations.

#### Optimization Notes

- Both solutions are already optimal in terms of time and space complexity.
- The odd counter initialization in Solution 1 is a clever optimization to avoid additional conditionals.
- Solution 2 demonstrates how using appropriate data structures can lead to elegant algorithmic solutions.
- In practice, both solutions would perform similarly for the constraints given.

```



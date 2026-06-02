# [Find All Anagrams in a String](https://leetcode.com/problems/find-all-anagrams-in-a-string/)

**Medium** | **20 minutes** | **String**

Given two strings `s` and `p`, return an array of all the start indices of `p`'s anagrams in `s`. You may return the answer in any order.

An **anagram** is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.

## Examples

**Example 1:**

```
Input: s = "abab", p = "ab"
Output: [0,2]
Explanation:
The substring with start index = 0 is "ab", which is an anagram of "ab".
The substring with start index = 2 is "ab", which is an anagram of "ab".
```

**Example 2:**

```
Input: s = "abacabad", p = "abab"
Output: [0,6]
Explanation:
The substring with start index = 0 is "abac", which is an anagram of "abab".
The substring with start index = 6 is "abad", which is an anagram of "abab".
```

## Constraints

- `1 <= s.length, p.length <= 3 * 10^4`
- `s` and `p` consist of lowercase English letters only.

## Solutions

```python
class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        # TODO: Implement solution
        pass
```


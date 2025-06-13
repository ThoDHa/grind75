# [Valid Anagram](https://leetcode.com/problems/valid-anagram/)

Easy - 15 Minutes - String

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

Follow up: What if the inputs contain Unicode characters? How would you adapt your solution to such a case?

## Solutions

### Solution 1: Iterative Character Removal

```python
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        # Early check: strings of different lengths can't be anagrams
        if len(s)!= len(t):
            return False
        # Iterate through each character in t
        for c in t:
            # If character exists in s, remove it once
            if c in s:
                s = s.replace(c, "", 1)
            # If character doesn't exist in s, not an anagram
            else:
                return False
        return True
```

### Approach

This solution iteratively removes characters from string `s` for each character in `t`. If any character in `t` doesn't exist in the remaining `s`, the strings aren't anagrams. If all characters can be removed exactly once, they are anagrams.

### Time and Space Complexity Analysis

#### Time Complexity: `O(n²)`

- For each character in `t` (O(n)), we perform a string search and replacement in `s` (O(n))
- String operations like `replace()` require scanning the entire string

#### Space Complexity: `O(n)`

- Creating modified versions of string `s` during replacements requires additional space

### Key Insights

- Simple and intuitive approach that directly implements the anagram definition
- Inefficient for large strings due to quadratic time complexity
- String replacements create new strings each time, consuming extra memory

### Solution 2: Hash Map Counter

```python
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        # Dictionary to track character frequencies
        counter = {}
        
        # Early check: strings of different lengths can't be anagrams
        if len(s) != len(t):
            return False
            
        # Count occurrences of each character in s
        for c in s:
            counter[c] = counter.get(c, 0) + 1
            
        # Check if t has matching character counts
        for c in t:
            # If character doesn't exist in s or all occurrences are used
            if counter.get(c, 0) == 0:
                return False
            counter[c] -= 1
            
        return True
```

### Approach

This solution uses a hash map to count character frequencies in string `s`, then decrements these counts for each character in `t`. If at any point a character in `t` has no remaining count, the strings aren't anagrams.

### Time and Space Complexity Analysis

#### Time Complexity: `O(n)`

- We traverse each string once, with `O(1)` dictionary operations
- Total time complexity is `O(n)` where n is the length of the strings

#### Space Complexity: `O(k)`

- Where k is the size of the character set (at most 26 for lowercase English letters)
- The dictionary stores at most k unique characters

### Key Insights

- More efficient than iterative removal with linear time complexity
- Dictionary approach avoids modifying strings in-place
- Well-suited for the constraints of the problem (lowercase English letters)

### Solution 3: Python Counter

```python
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        # Use Python's Counter class to compare character frequencies
        return Counter(s) == Counter(t)
```

### Approach

This elegant solution uses Python's built-in `Counter` collection, which automatically counts occurrences of elements. Simply comparing the counters of both strings determines if they're anagrams.

### Time and Space Complexity Analysis

#### Time Complexity: `O(n)`

- Creating Counter objects requires traversing each string once
- Equality comparison of Counter objects is also linear time

#### Space Complexity: `O(k)`

- Where `k` is the size of the character set
- Each Counter stores at most `k` unique characters

### Key Insights

- Most concise solution using Python's built-in functionality
- Leverages optimized Counter implementation
- Easily readable and maintainable code
- Perfect example of using the right built-in tool for the job

### Solution 4: Set-based Counting

```python
class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        # Early check: strings of different lengths can't be anagrams
        if len(s) != len(t):
            return False
        # Check if each unique character appears the same number of times in both strings
        for i in set(s):
            if s.count(i) != t.count(i):
                return False
        return True
```

### Approach

This solution first verifies the strings have equal length, then checks if each unique character from `s` appears the same number of times in both strings using Python's `count()` method.

### Time and Space Complexity Analysis

#### Time Complexity: `O(n + k²)`

- Creating the set of unique characters is `O(n)`
- For each unique character (at most `k`), we call `count()` on both strings (`O(n)`)
- Overall complexity is `O(n + k*n)`, which is `O(n²)` in worst case when all characters are unique

#### Space Complexity: `O(k)`

- The set stores at most k unique characters

### Key Insights

- Simple approach using Python's built-in methods
- More efficient than Solution 1 but less efficient than Solutions 2 and 3 for large inputs
- Using `set()` reduces the number of characters we need to check

## Comparison of Solutions

### Time Complexity

- **Solution 1 (Iterative Removal)**: `O(n²)` - Each character removal requires searching through the string
- **Solution 2 (Hash Map)**: `O(n)` - Linear time with a single pass through each string
- **Solution 3 (Python Counter)**: `O(n)` - Linear time leveraging Python's optimized Counter implementation
- **Solution 4 (Set-based)**: `O(n²)` - For each unique character, we count occurrences in both strings

### Space Complexity

- **Solution 1 (Iterative Removal)**: `O(n)` - Creates new string copies during replacement operations
- **Solution 2 (Hash Map)**: `O(k)` - Stores frequency counts for at most k unique characters
- **Solution 3 (Python Counter)**: `O(k)` - Similar to Solution 2, using Python's Counter data structure
- **Solution 4 (Set-based)**: `O(k)` - Stores at most k unique characters in the set

### Trade-offs

- **Solution 1** offers a straightforward implementation of the anagram concept but is inefficient for large inputs
- **Solution 2** provides an optimal balance of efficiency and code clarity with a language-agnostic approach
- **Solution 3** delivers maximum conciseness with Python's built-in tools while maintaining efficiency
- **Solution 4** simplifies the process by focusing on unique characters but still suffers from lower performance than Solutions 2 and 3

### When to Use Each

- **Solution 1 (Iterative Removal)**: Suitable for educational purposes or very small inputs where performance isn't critical
- **Solution 2 (Hash Map)**: Ideal for production code, interviews, and cross-language implementations
- **Solution 3 (Python Counter)**: Best for Python environments where readability and conciseness are valued
- **Solution 4 (Set-based)**: Appropriate when working with small inputs or when set operations are more intuitive

### Optimization Notes

- Solution 2's hash map approach demonstrates the classic time-space tradeoff, using a modest amount of memory to achieve linear time complexity
- Solution 3 shows how leveraging language-specific tools can simplify code without sacrificing efficiency
- The early length check in all solutions is a simple optimization that avoids unnecessary processing
- For Unicode character support (follow-up question), Solutions 2 and 3 scale naturally to handle larger character sets without modification, while Solutions 1 and 4 would degrade in performance
- Solution 1's string replacement is particularly costly as strings are immutable in many languages, including Python

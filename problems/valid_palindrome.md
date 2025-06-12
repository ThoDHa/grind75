# [Valid Palindrome](https://leetcode.com/problems/valid-palindrome)

Easy - 15 minutes - String

A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and
removing all non-alphanumeric characters, it reads the same forward and backward.
Alphanumeric characters include letters and numbers.

Given a string `s`, return `true` if it is a palindrome, or `false` otherwise.

## Examples

### Example 1

**Input:** `s = "A man, a plan, a canal: Panama"`

**Output:** `true`

**Explanation:** `"amanaplanacanalpanama"` is a palindrome.

### Example 2

**Input:** `s = "race a car"`

**Output:** `false`

**Explanation:** `"raceacar"` is not a palindrome.

### Example 3

**Input:** `s = " "`

**Output:** `true`

**Explanation:** `s` is an empty string `""` after removing non-alphanumeric characters.
Since an empty string reads the same forward and backward, it is a palindrome.

## Constraints

- `1 <= s.length <= 2 * 10^5`
- `s` consists only of printable ASCII characters.

### Solution 1: Two-Pointer Approach

```python
class Solution:
    def isPalindrome(self, s: str) -> bool:
        # Initialize two pointers at the beginning and end of the string
        left = 0
        right = len(s) - 1
        
        # Handle single-character strings (always palindromes)
        if len(s) == 1:
            return True
            
        # Compare characters from both ends moving inward
        while left < right:
            # Skip non-alphanumeric characters from the left
            if not s[left].isalnum():
                left += 1
                continue
                
            # Skip non-alphanumeric characters from the right
            if not s[right].isalnum():
                right -= 1
                continue
                
            # Compare characters (case-insensitive)
            if s[left].lower() != s[right].lower():
                return False
                
            # Move pointers inward
            left += 1
            right -= 1
            
        # If all characters matched, it's a palindrome
        return True
```

### Approach

This solution uses the two-pointer technique to check if a string is a palindrome after removing non-alphanumeric characters:

1. We initialize two pointers - one at the beginning (`left`) and one at the end (`right`) of the string.
2. We move these pointers towards each other, comparing characters at each step.
3. Non-alphanumeric characters are skipped using Python's built-in `isalnum()` function.
4. Characters are compared case-insensitively using `lower()` to convert both to lowercase.
5. If any pair of characters doesn't match, the string is not a palindrome.
6. If the pointers meet or cross without finding any mismatches, the string is a palindrome.

### Time and Space Complexity

- **Time Complexity**: O(n) - We traverse the string at most once, where n is the length of the string.
- **Space Complexity**: O(1) - We only use a constant amount of extra space for the pointers and condition variables.

### Key Insights

- Two-pointer technique is ideal for palindrome problems as it allows us to compare elements from both ends efficiently.
- Handling non-alphanumeric characters by simply skipping them avoids the need for a separate cleaning step.
- Case-insensitive comparison is performed on-the-fly without modifying the original string.
- The approach is more space-efficient than creating a new cleaned string and then checking if it's a palindrome.

## Solution 2: Filter and Reverse

```python
class Solution:
    def isPalindrome(self, s: str) -> bool:
        s = "".join(filter(str.isalnum,s)).lower()
        return s == s[::-1]
```

### Approach

This solution takes a more concise, Pythonic approach using built-in functions:

1. First, it filters the string to keep only alphanumeric characters using `filter(str.isalnum, s)`
2. Then it converts all remaining characters to lowercase using `.lower()`
3. Finally, it checks if the cleaned string equals its reverse using string slicing `s[::-1]`

### Time and Space Complexity

- **Time Complexity**: O(n) - Filtering the string and reversing both require iterating through each character once.
- **Space Complexity**: O(n) - This approach creates new strings that scale with the input size.

### Key Insights

- This approach is more concise and leverages Python's built-in functions for string manipulation.
- While less space-efficient, it offers excellent readability and simplicity.
- The solution demonstrates how Python's functional programming features can simplify algorithm implementation.

## Comparison of Solutions

### Time Complexity

- **Two-pointer**: O(n) - Single pass through the string with linear time operations
- **Filter/Reverse**: O(n) - Also linear time with string filtering and reversal

### Space Complexity

- **Two-pointer**: O(1) - Uses only constant extra space regardless of input size
- **Filter/Reverse**: O(n) - Creates new strings that scale with input size

### Trade-offs

- The two-pointer solution is more space-efficient but requires more detailed implementation
- The filter/reverse solution is more concise and readable but uses more memory

### When to Use Each

- **Two-pointer**: Preferred for memory-constrained environments or when processing very large strings
- **Filter/Reverse**: Ideal for readability and quick implementations where memory isn't a concern

### Optimization Notes

- The two-pointer approach avoids creating any new strings, processing the input in-place
- The filter/reverse solution makes excellent use of Python's built-in functions and is more Pythonic
- Both approaches handle the core requirements effectively: ignoring case and non-alphanumeric characters

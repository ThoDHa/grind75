# [Valid Parentheses](https://leetcode.com/problems/valid-parentheses/)

Easy - 20 minutes - Stack, String

Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`,
determine if the input string is valid.

An input string is valid if:

- Open brackets must be closed by the same type of brackets.
- Open brackets must be closed in the correct order.
- Every close bracket has a corresponding open bracket of the same type.

## Examples

### Example 1

**Input:** `s = "()"`

**Output:** `true`

### Example 2

**Input:** `s = "()[]{}"`

**Output:** `true`

### Example 3

**Input:** `s = "(]"`

**Output:** `false`

### Example 4

**Input:** `s = "([])"`

**Output:** `true`

## Constraints

- `1 <= s.length <= 10^4`
- `s` consists of parentheses only `'('`, `')'`, `'{'`, `'}'`, `'['`, `']'`.

## Solution

```python
class Solution:
    def isValid(self, s: str) -> bool:
        # Stack to keep track of opening brackets
        valid = []
        
        # Dictionary mapping closing brackets to their corresponding opening brackets
        parens_key = {")": "(", "]":"[", "}":"{"}
        
        # Early check: if string length is odd, it cannot be valid
        if len(s) % 2 != 0:
            return False
            
        # Iterate through each character in the string
        for x in s:
            # If it's an opening bracket, push to stack
            if x in ['(', '{', "["]:
                valid.append(x)
            # If it's a closing bracket
            else:
                # If stack is empty, we have a closing bracket without an opening one
                if not valid:
                    return False
                # Pop the most recent opening bracket
                tail = valid.pop()
                # Check if the popped bracket matches the expected opening bracket
                if tail != parens_key[x]:
                    return False
                    
        # String is valid if all opening brackets were closed (stack is empty)
        return not valid
```

### Solution Approach

This problem is solved using a stack data structure:

- We use a stack to keep track of opening brackets we've seen so far.
- For each opening bracket, we push it onto the stack.
- For each closing bracket, we check if the stack is empty (invalid) or if the top of the stack contains the corresponding opening bracket.
- If the stack is empty at the end, all opening brackets were properly closed.

### Time and Space Complexity Analysis

#### Time Complexity: O(n)

- We iterate through each character in the string exactly once, where n is the
  length of the string.
- All operations inside the loop (append, pop, dictionary lookup) are O(1) operations.

#### Space Complexity: O(n)

- In the worst case, the stack could contain all characters of the string
  (e.g., for a string like "((((").
- The dictionary of parentheses mappings uses constant space O(1).

## Key Insights

- Using a stack is perfect for this matching problem because brackets follow a
   Last-In-First-Out (LIFO) order.
- The early length check (odd number) is an optimization that quickly rules out
   invalid strings.
- The algorithm handles nested brackets correctly because of the stack's LIFO
   property.

# [Evaluate Reverse Polish Notation](https://leetcode.com/problems/evaluate-reverse-polish-notation/)

**Medium** | **25 minutes** | **Stack, Array, Math**

You are given an array of strings `tokens` that represents an arithmetic expression in Reverse Polish Notation (RPN).

Evaluate the expression. Return an integer that represents the value of the expression.

**Note:**

- Valid operators are `+`, `-`, `*`, and `/`.
- Each operand may be an integer or another expression.
- The division between two integers always truncates toward zero.
- There will not be any division by zero.
- The input represents a valid arithmetic expression in RPN.
- The answer and all intermediate calculations can be represented in a 32-bit integer.

## Examples

### Example 1

**Input:** `tokens = ["2","1","+","3","*"]`

**Output:** `9`

**Explanation:** ((2 + 1) * 3) = 9

### Example 2

**Input:** `tokens = ["4","13","5","/","+"]`

**Output:** `6`

**Explanation:** (4 + (13 / 5)) = 4 + 2 = 6

### Example 3

**Input:** `tokens = ["10","6","9","3","+","-11","*","/","*","17","+","5","+"]`

**Output:** `22`

**Explanation:**
  ((10 *(6 / ((9 + 3)* -11))) + 17) + 5
= ((10 *(6 / (12* -11))) + 17) + 5
= ((10 *(6 / -132)) + 17) + 5
= ((10* 0) + 17) + 5
= (0 + 17) + 5
= 17 + 5
= 22

## Constraints

- `1 <= tokens.length <= 10^4`
- `tokens[i]` is either an operator: `"+"`, `"-"`, `"*"`, or `"/"`, or an integer in the range `[-200, 200]`.

## Solutions

```python
class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        # TODO: Implement solution
        pass
```


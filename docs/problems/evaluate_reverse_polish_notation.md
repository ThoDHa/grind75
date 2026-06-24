# [Evaluate Reverse Polish Notation](https://leetcode.com/problems/evaluate-reverse-polish-notation/)

**Medium** | **25 minutes** | **Stack, Array, Math**

**Pattern:** [Stack](../patterns/stack/intuition.md)

**Practice:** [`practice/evaluate_reverse_polish_notation/solution.py`](../../practice/evaluate_reverse_polish_notation/solution.py)

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

### Recursive Evaluation

```python
from typing import List


class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        operators = {'+', '-', '*', '/'}
        # Scan right to left: the last token is always the outermost operator
        pos = len(tokens) - 1

        def evaluate() -> int:
            nonlocal pos
            token = tokens[pos]
            pos -= 1
            if token not in operators:
                return int(token)
            # The token just before an operator closes its right operand;
            # whatever precedes that is the left operand
            right = evaluate()
            left = evaluate()
            if token == '+':
                return left + right
            if token == '-':
                return left - right
            if token == '*':
                return left * right
            # int() truncates toward zero, matching the spec, unlike Python's
            # // which floors toward negative infinity
            return int(left / right)

        return evaluate()
```

#### Approach

An RPN expression is the post-order traversal of an expression tree, so the
final token is always the root operator and the values before it split into a
right operand subtree followed by a left operand subtree. Reading the tokens
from right to left, we can reconstruct and evaluate that tree directly, with no
stack at all.

1. Set `pos` to the last token and define a recursive `evaluate` that consumes
   tokens from the right.
2. Read the token at `pos`, then move `pos` one step left.
3. If the token is a number, convert it with `int(token)` and return it.
4. If the token is an operator, recursively evaluate the `right` operand first
   (it sits immediately to the left), then the `left` operand.
5. Combine `left` and `right` with the operator and return the result, using
   `int(left / right)` so division truncates toward zero.

The right-before-left recursion order is the crux: because we walk leftward, the
operand nearest the operator is its right child, exactly mirroring how the tree
was flattened into post-order.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each of the `n` tokens triggers exactly one `evaluate` call doing constant work,
so the traversal is linear.

##### Space Complexity: `O(n)`

The recursion depth equals the height of the expression tree, which can reach
`O(n)` for a deeply nested expression (for example, a long chain of operators
each combining a number with the previous result).

#### Key Insights

- RPN is post-order, so the rightmost token is the root and the tree can be
  rebuilt by scanning right to left.
- Recursing into the `right` operand before the `left` is mandatory, since the
  operand adjacent to the operator is its right child.
- This derives the answer straight from the expression's structure without ever
  naming a stack, making it the most intuitive starting point.
- The recursion itself plays the role the explicit stack fills in the iterative
  versions; the call stack holds the pending operands.

### Stack

```python
from typing import List


class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        stack = []
        operators = {'+', '-', '*', '/'}

        for token in tokens:
            if token in operators:
                # Operands were pushed in order, so the second popped value
                # is the left-hand side of the operation
                right = stack.pop()
                left = stack.pop()
                if token == '+':
                    stack.append(left + right)
                elif token == '-':
                    stack.append(left - right)
                elif token == '*':
                    stack.append(left * right)
                else:
                    # int() truncates toward zero, matching the spec, unlike
                    # Python's // which floors toward negative infinity
                    stack.append(int(left / right))
            else:
                stack.append(int(token))

        return stack[-1]
```

#### Approach

Reverse Polish Notation places each operator immediately after its two operands,
which is exactly the order a stack consumes. Scanning left to right, we push
operands and, on seeing an operator, pop the two most recent values, combine
them, and push the result back.

1. Initialize an empty `stack` and a set of the four operator symbols.
2. For each `token`, if it is an operator, pop `right` then `left` (this order
   matters for `-` and `/`, which are not commutative).
3. Apply the operator to `left` and `right` and push the result.
4. For division, use `int(left / right)` so the quotient truncates toward zero
   as the problem requires.
5. If the token is a number, convert it with `int(token)` and push it.
6. After processing every token, the single remaining value on the stack is the
   answer.

The pop order is the subtle point: because `left` was pushed before `right`, the
first pop yields `right`. Reversing this would compute `right - left` and
`right / left`, which is wrong for the non-commutative operators.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each of the `n` tokens is processed once, and every stack push and pop is `O(1)`.

##### Space Complexity: `O(n)`

In the worst case (a long run of operands before any operator), the stack holds
on the order of `n` values.

#### Key Insights

- RPN eliminates the need for parentheses and precedence rules; a stack consumes
  operands and operators in exactly the right order.
- Popping yields `right` before `left`, so respecting that order is essential for
  the non-commutative `-` and `/`.
- Python's `//` floors toward negative infinity, so `int(a / b)` is required to
  truncate toward zero (for example, `6 / -132` must give `0`, not `-1`).
- A single pass with constant work per token makes the evaluation linear.

### Operator Dispatch Table

```python
import operator
from typing import Callable, Dict, List


class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        operations: Dict[str, Callable[[int, int], int]] = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            # int() truncates toward zero, unlike // which floors
            '/': lambda left, right: int(left / right),
        }

        stack = []
        for token in tokens:
            if token in operations:
                right = stack.pop()
                left = stack.pop()
                stack.append(operations[token](left, right))
            else:
                stack.append(int(token))

        return stack[-1]
```

#### Approach

This is the same stack-based evaluation, but the four-way `if`/`elif` chain is
replaced by a dictionary that maps each operator symbol to the function that
applies it. The scan logic becomes uniform: every operator is handled by one
lookup and one call.

1. Build a `operations` table mapping each symbol to a binary function.
   Addition, subtraction, and multiplication come straight from the `operator`
   module; division uses a small lambda wrapping `int(left / right)` so the
   quotient truncates toward zero.
2. Initialize an empty `stack`.
3. For each `token`, if it is a key in `operations`, pop `right` then `left`,
   apply `operations[token](left, right)`, and push the result.
4. Otherwise convert the token with `int(token)` and push it.
5. Return the final value left on the stack.

The pop order (`right` first, then `left`) is identical to the explicit version
and is still essential for the non-commutative `-` and `/`.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each of the `n` tokens is processed once. A dictionary lookup and a function
call are both `O(1)`, so the work per token is constant.

##### Space Complexity: `O(n)`

The dispatch table holds a fixed four entries, which is `O(1)`, but the stack
can still grow to hold on the order of `n` operands, so overall auxiliary space
is `O(n)`.

#### Key Insights

- A dispatch table trades a branch chain for a single lookup, keeping the loop
  body uniform and easy to extend with new operators.
- Using `operator.add`, `operator.sub`, and `operator.mul` avoids hand-written
  lambdas for the commutative operations while keeping the code compact.
- Division still needs the explicit `int(left / right)` wrapper because the
  truncation-toward-zero rule is not what `//` provides.
- The membership test `token in operations` doubles as the operator check, so no
  separate operator set is required.

## Comparison of Solutions

### Time Complexity

- **Recursive Evaluation**: `O(n)` - each token drives one recursive call doing
  constant work.
- **Stack**: `O(n)` - one pass, constant work per token.
- **Operator Dispatch Table**: `O(n)` - one pass, constant lookup and call per
  token.

### Space Complexity

- **Recursive Evaluation**: `O(n)` - the recursion can reach a depth proportional
  to the expression-tree height, up to `n`.
- **Stack**: `O(n)` - the operand stack can hold up to `n` values.
- **Operator Dispatch Table**: `O(n)` - same operand stack, plus a fixed-size
  table that is `O(1)`.

### Trade-offs

- The Recursive Evaluation approach derives the answer directly from the
  expression's post-order structure with no explicit stack, but trades an
  iterative loop for recursion that can reach `O(n)` depth on deeply nested
  input.
- The Stack approach spells out each operator inline, which is maximally explicit
  and needs no imports, at the cost of a repetitive `if`/`elif` chain.
- The Operator Dispatch Table approach centralizes operator handling in one data
  structure, making the loop shorter and new operators trivial to add, at the
  cost of an extra import and a small amount of indirection.

### When to Use Each

- **Recursive Evaluation**: When you want to reason about RPN as an expression
  tree from first principles, or to make the post-order structure explicit
  without introducing a stack.
- **Stack**: When you want the most self-evident, dependency-free iterative
  implementation, or in an interview where writing out the branches makes the
  truncation detail obvious to the reader.
- **Operator Dispatch Table**: When the operator set might grow, or when you
  prefer a uniform loop body that separates the "what to do" table from the "how
  to scan" logic.

### Optimization Notes

- All three approaches are already linear and optimal for this problem; the
  differences are purely structural.
- Prefer the iterative Stack over the Recursive Evaluation for the upper
  constraint of `10^4` tokens, where a deeply nested expression could otherwise
  approach Python's default recursion limit.
- Keep the division wrapped in `int(left / right)` in either version; replacing
  it with `left // right` silently breaks cases where exactly one operand is
  negative (for example, `7 / -2` must give `-3`, not `-4`).
- Reading `stack[-1]` (the top) rather than `stack[0]` returns the final result
  even if defensive code leaves stray values below it; for a valid RPN
  expression the stack ends with exactly one element.

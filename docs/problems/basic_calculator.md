# [Basic Calculator](https://leetcode.com/problems/basic-calculator/)

**Hard** | **40 minutes** | **Stack**

**Pattern:** [Stack](../patterns/stack/intuition.md)

**Practice:** [`practice/basic_calculator/solution.py`](../../practice/basic_calculator/solution.py)

Given a string `s` representing a valid expression, implement a basic calculator to evaluate it, and return the result of the evaluation.

**Note:** You are **not** allowed to use any built-in function which evaluates strings as mathematical expressions, such as `eval()`.

## Examples

### Example 1

**Input:** `s = "1 + 1"`

**Output:** `2`

### Example 2

**Input:** `s = " 2-1 + 2 "`

**Output:** `3`

### Example 3

**Input:** `s = "(1+(4+5+2)-3)+(6+8)"`

**Output:** `23`

## Constraints

- `1 <= s.length <= 3 * 10^5`
- `s` consists of digits, `'+'`, `'-'`, `'('`, `')'`, and `' '`.
- `s` represents a valid expression.
- `'+'` is **not** used as a unary operation (i.e., `"+1"` and `"+(2 + 3)"` is invalid).
- `'-'` could be used as a unary operation (i.e., `"-1"` and `"-(2 + 3)"` is valid).
- There will be no two consecutive operators in the input.
- Every number and running calculation will fit in a signed 32-bit integer.

## Solutions

### Stack

```python
class Solution:
    def calculate(self, s: str) -> int:
        result = 0       # Running total of the current parenthesis level
        sign = 1         # Sign to apply to the next number (+1 or -1)
        number = 0       # Digits accumulated for the number being parsed
        stack = []       # Saves (result, sign) when entering a sub-expression

        for char in s:
            if char.isdigit():
                # Build multi-digit numbers left to right
                number = number * 10 + int(char)
            elif char == '+':
                result += sign * number
                number = 0
                sign = 1
            elif char == '-':
                result += sign * number
                number = 0
                sign = -1
            elif char == '(':
                # Push the context and start the sub-expression fresh
                stack.append(result)
                stack.append(sign)
                result = 0
                sign = 1
            elif char == ')':
                # Finish the current number inside the parentheses
                result += sign * number
                number = 0
                # Apply the sign that preceded '(' to the whole group,
                # then add the result computed before '('
                result *= stack.pop()
                result += stack.pop()
            # Spaces are simply ignored

        # Flush the final number after the loop ends
        return result + sign * number
```

#### Approach

The expression contains only addition, subtraction, parentheses, and spaces, and
crucially has no multiplication or division, so there is no operator precedence
to worry about beyond grouping. That lets us evaluate left to right with a single
running total, using a stack only to remember context across parentheses.

We track three running values: `result` (the sum so far at the current level),
`sign` (the `+1`/`-1` to apply to the next number), and `number` (the digits of
the integer currently being read). A parenthesis is the only thing that
interrupts the flat left-to-right scan, so we push the outer context when we
descend and restore it when we return.

1. Scan each character of `s`.
2. For a digit, fold it into `number` with `number * 10 + int(char)`.
3. For `+` or `-`, commit the pending number with `result += sign * number`,
   reset `number`, and set `sign` to `+1` or `-1` for what comes next.
4. For `(`, push `result` and `sign` onto the stack, then reset them to `0` and
   `+1` to evaluate the inner expression independently.
5. For `)`, commit the pending number, multiply `result` by the saved `sign`
   (which may be `-1` for a unary-minus group), then add back the saved outer
   `result`.
6. Ignore spaces.
7. After the loop, commit the last pending number and return `result`.

Unary minus is handled naturally: `-(2 + 3)` reads `-` (setting `sign = -1`),
then `(` pushes that `-1`. When `)` is hit, multiplying the inner result by the
popped `-1` negates the whole group.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each character is processed exactly once with constant work, where `n` is the
length of `s`.

##### Space Complexity: `O(n)`

The stack grows with the depth of nested parentheses, which in the worst case
(deeply nested expression) is `O(n)`.

#### Key Insights

- With no multiplication or division, the expression evaluates flatly left to
  right; the stack is needed only to suspend and resume across parentheses.
- Pushing `(result, sign)` and resetting captures exactly the state needed to
  resume the outer computation after the group closes.
- Multiplying the inner result by the saved sign is what makes unary minus on a
  parenthesized group fall out for free.
- Building numbers with `number * 10 + digit` cleanly handles multi-digit
  operands without slicing the string.

### Stack of Signs

```python
class Solution:
    def calculate(self, s: str) -> int:
        result = 0       # Running total across the whole expression
        number = 0       # Digits accumulated for the number being parsed
        sign = 1         # Effective sign to apply to the next number
        signs = [1]      # Sign that multiplies the current parenthesis level

        for char in s:
            if char.isdigit():
                number = number * 10 + int(char)
            elif char == '+':
                result += sign * number
                number = 0
                sign = signs[-1]
            elif char == '-':
                result += sign * number
                number = 0
                sign = -signs[-1]
            elif char == '(':
                # The whole group inherits the sign in front of it
                signs.append(sign)
                sign = signs[-1]
            elif char == ')':
                result += sign * number
                number = 0
                signs.pop()
                sign = signs[-1]
            # Spaces are simply ignored

        return result + sign * number
```

#### Approach

Instead of saving the partial `result` on a stack and reconstructing it when a
group closes, this approach distributes each group's sign down into the terms it
contains. A single running `result` accumulates every term with its fully
resolved sign, so there is nothing to restore when a parenthesis closes.

The trick is the `signs` stack, which holds the multiplier that applies to the
current parenthesis level. When `(` is reached, the sign currently in front of
the group is pushed; every operator inside then combines the group's sign with
the local `+`/`-`. Because the sign is resolved eagerly, the expression never
needs to remember an outer partial sum.

1. Keep `signs[-1]` as the sign that multiplies the current level (start at `+1`).
2. For a digit, fold it into `number`.
3. For `+`, commit the pending number, then set `sign` to `signs[-1]` so the next
   term carries the group's sign.
4. For `-`, commit the pending number, then set `sign` to `-signs[-1]` so the
   next term is negated relative to the group.
5. For `(`, push the current `sign` as the new level's multiplier.
6. For `)`, commit the pending number, pop the level, and restore `sign` to the
   parent's multiplier.
7. Ignore spaces; after the loop, commit the last number.

A leading `-` before a group sets `sign = -1`, which is pushed on `(`, so every
term inside is negated relative to the parent: exactly the unary-minus behavior.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each character is processed once with constant work, where `n` is the length of
`s`.

##### Space Complexity: `O(n)`

The `signs` stack grows with the nesting depth of parentheses, which is `O(n)` in
the worst case.

#### Key Insights

- Pushing only a single integer (the level's sign) instead of `(result, sign)`
  keeps the running total flat and avoids reconstructing partial sums.
- Resolving each term's sign eagerly means the algorithm never has to "return"
  to an outer computation, only restore which sign currently applies.
- This is a clean reformulation: same `O(n)` cost, but the stack carries less
  state per frame.

### Recursive Descent

```python
class Solution:
    def calculate(self, s: str) -> int:
        self.s = s
        self.i = 0
        return self._parse()

    def _parse(self) -> int:
        result = 0
        sign = 1
        number = 0
        while self.i < len(self.s):
            char = self.s[self.i]
            self.i += 1
            if char.isdigit():
                number = number * 10 + int(char)
            elif char == '+':
                result += sign * number
                number = 0
                sign = 1
            elif char == '-':
                result += sign * number
                number = 0
                sign = -1
            elif char == '(':
                # The parenthesized sub-expression evaluates to a single number
                number = self._parse()
            elif char == ')':
                break
            # Spaces are simply ignored
        return result + sign * number
```

#### Approach

This approach mirrors how the grammar is structured: an expression is a sequence
of signed terms, and a term is either a number or a parenthesized expression. A
shared index `self.i` walks the string while `_parse` evaluates one parenthesis
level and returns when it hits the matching `)` or the end of the string.

When `_parse` encounters `(`, it calls itself to evaluate the inner expression.
The recursive call advances the shared index past the matching `)` and returns
that group's value, which is treated exactly like a freshly parsed number and
folded in with the current `sign`.

1. `calculate` stores the string, resets the index, and calls `_parse`.
2. `_parse` reads characters, building numbers and tracking `sign`, just like the
   flat scan.
3. On `(`, recurse into `_parse`; the returned value becomes the current
   `number`, picking up the pending `sign`.
4. On `)`, stop and return the level's `result` plus the trailing number.
5. The shared index guarantees each character is consumed exactly once across all
   recursive calls.

Unary minus works because a `-` before `(` sets `sign = -1`, and the recursive
call's return value is then multiplied by that `sign` when committed.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

The shared index advances monotonically, so every character is read exactly once
across all recursive calls.

##### Space Complexity: `O(n)`

Recursion depth equals the maximum parenthesis nesting, which is `O(n)` in the
worst case; this consumes call-stack space rather than an explicit stack.

#### Key Insights

- A shared mutable index lets recursion replace the explicit stack while still
  touching each character once.
- Treating a parenthesized group's return value as just another number keeps the
  per-level logic identical to the flat left-to-right scan.
- The recursion structure makes the grammar explicit, which can be easier to
  extend if precedence (for example `*` and `/`) is added later.

## Comparison of Solutions

### Time Complexity

- **Stack**: `O(n)` - single pass, constant work per character.
- **Stack of Signs**: `O(n)` - single pass, constant work per character.
- **Recursive Descent**: `O(n)` - shared index reads each character once.

### Space Complexity

- **Stack**: `O(n)` - pushes two values per nesting level.
- **Stack of Signs**: `O(n)` - pushes one sign per nesting level.
- **Recursive Descent**: `O(n)` - call-stack depth equals nesting depth.

### Trade-offs

- **Stack** stores a full snapshot `(result, sign)` per level, which is the most
  literal "save and restore the context" model and the easiest to reason about
  first.
- **Stack of Signs** stores only a single integer per level by resolving each
  term's sign eagerly; it keeps the running total flat at the cost of a slightly
  less obvious sign bookkeeping.
- **Recursive Descent** trades the explicit stack for the call stack, making the
  grammar explicit and extensible but risking recursion-depth limits on
  pathologically nested input.

### When to Use Each

- **Stack**: The default and clearest choice; reach for it first in an interview.
- **Stack of Signs**: When you want to minimize per-frame state or articulate the
  insight that only the group's sign needs preserving.
- **Recursive Descent**: When the parser may grow to handle operator precedence,
  where a grammar-driven structure pays off (Recommended for extensibility).

### Optimization Notes

- All three are optimal at `O(n)` time; the differences are in clarity and how
  much state each parenthesis level carries.
- The iterative stack approaches avoid Python's recursion-depth ceiling, which
  matters because `s` can be up to `3 * 10^5` characters with deep nesting.
- Building numbers with `number * 10 + int(char)` avoids string slicing and keeps
  the scan allocation-free per character.

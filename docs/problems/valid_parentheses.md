# [Valid Parentheses](https://leetcode.com/problems/valid-parentheses/)

**Easy** | **20 minutes** | **Stack, String**

**Pattern:** [Stack](../patterns/stack/intuition.md)

**Practice:** [`practice/valid_parentheses/solution.py`](../../practice/valid_parentheses/solution.py)

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

## Solutions

### Stack

```python
class Solution:
    def isValid(self, s: str) -> bool:
        stack = []

        for char in s:
            if char == "(" or char == "[" or char == "{":
                stack.append(char)
            elif char == ")":
                if not stack or stack.pop() != "(":
                    return False
            elif char == "]":
                if not stack or stack.pop() != "[":
                    return False
            elif char == "}":
                if not stack or stack.pop() != "{":
                    return False

        return not stack
```

#### Approach

Brackets must close in last-opened, first-closed order, which is exactly the
behaviour of a stack. The most direct idea is to push each opening bracket as it
appears, then on a closing bracket check that the most recently opened bracket is
its matching opener:

1. Walk the string one character at a time.
2. On an opening bracket, push that bracket onto the stack.
3. On a closing bracket, it is valid only if the stack is non-empty and its top is
   the matching opener. Pop and compare; on any mismatch (or an empty stack) the
   string is invalid, so return `False`.
4. After the loop, the string is valid only if the stack is empty, meaning every
   opening bracket was matched.

Each closing bracket spells out its own opener inline, so the logic stays explicit
without any lookup table.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each character is visited once, and the push, pop, and comparison operations are
all `O(1)`, where `n` is the length of `s`.

##### Space Complexity: `O(n)`

In the worst case (a string of only opening brackets such as `"(((("`) every
character is pushed, so the stack grows to size `n`.

#### Key Insights

- A stack models the Last-In-First-Out matching order brackets require.
- Storing the raw opener and comparing it on close handles the "right type" and
  "right order" rules together: the top of the stack is always the only opener
  that may legally be closed next.
- The final emptiness check catches unclosed openers like `"(("`, while the
  empty-stack guard inside the loop catches stray closers like `")"`.

### Stack with Hash Map

```python
class Solution:
    def isValid(self, s: str) -> bool:
        pairs = {")": "(", "]": "[", "}": "{"}
        stack = []

        for char in s:
            if char in pairs:
                if not stack or stack[-1] != pairs[char]:
                    return False
                stack.pop()
            else:
                stack.append(char)

        return not stack
```

#### Approach

This variant keeps the same stack mechanics but makes the bracket relationships
explicit with a hash map from each closing bracket to its opening counterpart:

1. Build a map `pairs` so that `pairs[")"] == "("` and so on.
2. Walk the string. If a character is a key in `pairs`, it is a closing bracket;
   otherwise it is an opening bracket.
3. For an opening bracket, push it onto the stack.
4. For a closing bracket, verify the stack is non-empty and its top equals the
   expected opener `pairs[char]`. If so, pop; otherwise return `False`.
5. Return `True` only when the stack is empty at the end.

Membership in `pairs` doubles as the open-versus-close test, so no separate set
of opening brackets is needed.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Every character drives one pass through the loop, and dictionary lookups, pushes,
and pops are each `O(1)`.

##### Space Complexity: `O(n)`

The stack can hold up to `n` opening brackets. The `pairs` map is fixed-size, so
it contributes only `O(1)`.

#### Key Insights

- Using the closing bracket as the dictionary key lets the `in pairs` check
  classify characters as opening or closing without a second collection.
- Inspecting `stack[-1]` before popping keeps the empty-stack case explicit.
- The logic is the textbook form most interviewers expect to see.

### Iterative Replacement

```python
class Solution:
    def isValid(self, s: str) -> bool:
        while "()" in s or "[]" in s or "{}" in s:
            s = s.replace("()", "").replace("[]", "").replace("{}", "")
        return s == ""
```

#### Approach

A valid string can be collapsed by repeatedly deleting innermost matched pairs:

1. While the string still contains `"()"`, `"[]"`, or `"{}"`, delete every
   occurrence of all three.
2. Each round removes the currently innermost pairs, exposing the pairs that
   surrounded them for the next round.
3. When no matched pair remains, the string is valid if and only if it is empty.

This leans on `str.replace` to do the core matching work, which is why it is
listed after the from-scratch stack solutions despite its brevity.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Each `replace` scan is `O(n)`, and a deeply nested string such as `"(((...)))"`
removes only the innermost layer per round, requiring up to `O(n)` rounds.

##### Space Complexity: `O(n)`

Strings are immutable, so every `replace` builds a new string of size up to `n`.

#### Key Insights

- Deleting matched pairs is an intuitive restatement of the validity rules and is
  easy to reason about.
- It avoids an explicit stack but pays for it with repeated full-string rescans.
- Practical only for short inputs; the quadratic behaviour makes it unsuitable for
  the `10^4`-length upper bound.

## Comparison of Solutions

### Time Complexity

- **Stack**: `O(n)` - one pass with constant-time stack operations.
- **Stack with Hash Map**: `O(n)` - one pass with constant-time lookups.
- **Iterative Replacement**: `O(n^2)` - up to `O(n)` full-string scans.

### Space Complexity

- **Stack**: `O(n)` - the stack can hold every opening bracket.
- **Stack with Hash Map**: `O(n)` - same stack, plus an `O(1)` map.
- **Iterative Replacement**: `O(n)` - each rebuilt string is up to length `n`.

### Trade-offs

- **Stack** is the most direct single-pass solution and needs no auxiliary map, at
  the cost of an `if`/`elif` ladder that spells out each opener-closer pair inline.
- **Stack with Hash Map** trades that ladder for a readable lookup table, which
  scales naturally if more bracket types were ever added.
- **Iterative Replacement** is the shortest to write but the slowest, and it hides
  the matching logic inside `str.replace`.

### When to Use Each

- **Stack**: The default choice for an interview; fast, in-place, and explicit.
- **Stack with Hash Map**: When you want the clearest mapping between closers and
  openers, or anticipate more bracket types.
- **Iterative Replacement**: Only for tiny inputs or a quick sanity check where
  performance does not matter.

### Optimization Notes

- The **Stack** approach avoids a dictionary lookup per character by hard-coding
  each opener-closer pair in the `if`/`elif` ladder; a variant that pushes the
  expected closer instead of the opener would fuse the type and order checks into a
  single equality test.
- An optional early `return False` when `len(s)` is odd skips the whole scan for
  inputs that cannot possibly balance.
- Both stack solutions short-circuit on the first mismatch, so invalid strings are
  often rejected well before the end.

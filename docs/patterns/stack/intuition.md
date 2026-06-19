# Stack: Pattern Intuition Guide

> *"A stack is a memory of unfinished business — the last thing you started is the first thing you must finish."*

---

## The Situation That Calls for a Stack

Imagine you're reading a deeply nested document: a chapter that opens a section, which opens a sub-section, which opens a footnote. To make sense of the footnote, you must remember everything that's still open above it. And when the footnote closes, you return to exactly where you left the sub-section — not the chapter, not some earlier point, but the **most recent unfinished thing**.

You could try to track all of this in your head. But the structure is nested, and the rule is rigid: whatever you opened last must close first. The moment you violate that order, the document is malformed.

**This is the essence of a Stack.**

A stack is a last-in-first-out (LIFO) container. You push work onto it when you encounter something you can't finish yet, and you pop it off when the thing that resolves it finally arrives. The most recent item is always the one on top, always the next to be handled.

You encounter this pattern whenever:
- The structure is **nested** or **balanced** (delimiters, tags, scopes)
- You must **defer** work until a later signal tells you to resolve it
- Each element is paired with its **most recent unmatched** counterpart
- You need to **undo** or **backtrack** to the last open item

The key insight: *You are not scanning for a global answer — you are tracking what is still open, and resolving each thing in reverse order of arrival.*

---

## The Core Insight

Every stack algorithm rests on a single promise:

> **The stack holds the unfinished work, with the most recent on top. You resolve in reverse order of arrival.**

When you read input left to right, some pieces cannot be acted on immediately. An opening bracket means nothing until its closing partner appears. An operand sits idle until an operator tells it what to do. So you set these pieces aside — push them — and carry on.

When the resolving signal arrives, it always pairs with the **top** of the stack: the most recent unfinished item. Not the oldest, not some middle element. The top. This is what makes the stack the right tool: nesting is inherently last-opened-first-closed, and the stack enforces exactly that order for free.

```
The LIFO Promise:
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   Reading:  (  [  {                                                          │
│                                                                             │
│   Stack:  [ (, [, { ]   ← '{' is on top: most recent, still open           │
│             ↑  ↑  ↑                                                          │
│             │  │  └── opened last, must close first                          │
│             │  └───── opened second, closes second                          │
│             └──────── opened first, closes last                             │
│                                                                             │
│   Next char '}' resolves the top '{'. Then ']' resolves '['. Then ')'.      │
│   Always the top. Always reverse order.                                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Four Mental Models

A stack wears several disguises. Recognizing each one tells you what to push and when to pop.

### Model 1: Matching and Balancing Nested Delimiters
> *"Every opener must close, and in the right order."*

Push each opening symbol. On a closing symbol, the top of the stack must be its matching opener. If it matches, pop and continue. If it doesn't match — or the stack is empty — the structure is invalid.

```python
pairs = {')': '(', ']': '[', '}': '{'}
stack = []
for ch in s:
    if ch in '([{':
        stack.append(ch)
    else:
        if not stack or stack.pop() != pairs[ch]:
            return False
return not stack   # leftover openers mean unbalanced
```

### Model 2: Postfix (Expression) Evaluation
> *"Operands wait on the stack until an operator resolves them."*

In Reverse Polish Notation, numbers have no meaning alone — they wait. When an operator arrives, it reaches back for the two most recent operands (the top two on the stack), computes, and pushes the result. The result then waits to become an operand for a later operator.

```python
stack = []
for tok in tokens:
    if tok in '+-*/':
        b = stack.pop()
        a = stack.pop()          # order matters for - and /
        stack.append(apply(tok, a, b))
    else:
        stack.append(int(tok))
return stack[-1]
```

### Model 3: Parsing with Nested Context
> *"Push your current state when context opens, restore it when context closes."*

When you enter a parenthesized sub-expression, you don't lose what you were building — you set it aside. Push the accumulated result and the pending sign onto the stack on `(`. When `)` arrives, pop them and fold the inner result back into the outer context. The stack carries the suspended outer scopes.

### Model 4: An Explicit Stack Replaces the Call Stack
> *"Recursion is a stack you didn't write down."*

Every recursive call quietly pushes a frame onto the program's call stack and pops it on return. Any recursive traversal can be rewritten with an explicit stack: push the work you'd recurse into, pop to process it. This is why iterative DFS uses a stack — it is the call stack made visible, useful when recursion depth would overflow or when you want manual control.

---

## Pattern Recognition Signals

When you see these phrases, think **Stack**:

### Signal: "Balanced" or "Nested" or "Valid"
> *"Determine if the brackets are valid"*
> *"Check that tags are properly nested"*

**Action**: Push openers, match and pop on closers, verify the stack is empty at the end.

### Signal: "Most recent unmatched" or "Last open"
> *"Find the innermost unclosed scope"*
> *"Remove the last added item"*

**Action**: The top of the stack is exactly the most recent unmatched element.

### Signal: "Evaluate an expression"
> *"Evaluate this postfix expression"*
> *"Implement a basic calculator"*

**Action**: Push operands, apply operators to the top of the stack, push the result.

### Signal: "Undo" or "Backtrack to the last open item"
> *"Process directory navigation like `..`"*
> *"Simplify a path"*

**Action**: Push on descent, pop to backtrack to the previous level.

If the problem is specifically *"for each element, find the next greater or smaller element,"* reach for the **monotonic stack** instead — it is a specialization of this pattern that keeps the stack ordered so dominated candidates can be discarded.

---

## Worked Trace 1: Valid Parentheses

Input: `s = "([{}])"`

```
Reading char by char, tracking the stack:

  ch   action                         stack after
  ──   ────────────────────────────   ───────────
  (    push opener                     [ (        ]
  [    push opener                     [ (, [     ]
  {    push opener                     [ (, [, {  ]
  }    closer; top is '{' ✓ pop        [ (, [     ]
  ]    closer; top is '[' ✓ pop        [ (        ]
  )    closer; top is '(' ✓ pop        [          ]

End: stack is empty → VALID
```

Now a malformed input: `s = "(]"`

```
  ch   action                         stack after
  ──   ────────────────────────────   ───────────
  (    push opener                     [ (        ]
  ]    closer; top is '(' but ']'      ── mismatch → INVALID
       needs '[' → fail immediately
```

And an unclosed input: `s = "(("`

```
  ch   action                         stack after
  ──   ────────────────────────────   ───────────
  (    push opener                     [ (        ]
  (    push opener                     [ (, (     ]

End: stack is NOT empty → INVALID (two openers never closed)
```

The two failure modes are the two pitfalls in disguise: a mismatch (or empty stack) on a closer, and leftover items at the end.

---

## Worked Trace 2: Evaluate Reverse Polish Notation

Input: `tokens = ["2", "1", "+", "3", "*"]`, meaning `(2 + 1) * 3`.

```
  token   action                              stack after
  ─────   ─────────────────────────────────   ───────────
  2       push operand                         [ 2       ]
  1       push operand                         [ 2, 1    ]
  +       pop 1, pop 2 → 2 + 1 = 3, push       [ 3       ]
  3       push operand                         [ 3, 3    ]
  *       pop 3, pop 3 → 3 * 3 = 9, push       [ 9       ]

End: result is the lone value on the stack → 9
```

Note the **pop order**: the first value popped is the right operand. For `+` and `*` it doesn't matter, but for `-` and `/` it does. With tokens `["5", "3", "-"]` you pop `3` then `5`, computing `5 - 3 = 4`, not `3 - 5`.

---

## Worked Trace 3: Basic Calculator (Sign and Paren Stack)

Input: `s = "1 + (2 - 3)"`. Here the stack suspends the outer context across parentheses.

We carry a running `result`, a current `number`, and a current `sign` (+1 or -1). On `(` we push the result-so-far and the sign-before-the-paren, then reset. On `)` we fold the inner result back using the saved sign.

```
  read   running computation                       stack
  ────   ─────────────────────────────────────     ──────────────
  1      number=1
  +      result = 0 + (+1)*1 = 1; sign=+1           [ ]
  (      push (result=1, sign=+1); reset            [ 1, +1 ]
         result=0, sign=+1
  2      number=2
  -      result = 0 + (+1)*2 = 2; sign=-1           [ 1, +1 ]
  3      number=3
  )      inner = result + (-1)*3 = 2 - 3 = -1
         pop sign=+1, pop prev=1
         result = 1 + (+1)*(-1) = 0                 [ ]

End: result = 0
```

The stack holds exactly the suspended outer scopes. Each `(` deepens one level; each `)` restores the level above and merges the inner answer in with the correct sign.

---

## Common Pitfalls

### Pitfall 1: Popping an Empty Stack
**Problem**: A closing symbol or operator arrives, but the stack is empty.

**Solution**: Always guard the pop. An empty stack on a closer means there is nothing to match, which is itself the answer (invalid input), not a crash.

```python
if not stack:
    return False        # closer with no opener
top = stack.pop()
```

### Pitfall 2: Non-Empty Stack at the End
**Problem**: Treating "no errors during the scan" as success while ignoring leftovers.

**Solution**: For matching problems, unmatched openers remain on the stack. The structure is valid only if the stack is **empty** at the end.

```python
return len(stack) == 0
```

### Pitfall 3: Operator Precedence and Sign Handling
**Problem**: In infix evaluation, applying operators in reading order ignores that `*` and `/` bind tighter than `+` and `-`; mishandling unary minus corrupts the result.

**Solution**: Apply `*` and `/` immediately against the top of the value stack, but defer `+` and `-` by pushing signed numbers and summing at the end. Track the current sign explicitly so a leading or post-`(` minus is handled correctly.

### Pitfall 4: Mixing the Value Stack and the Operator Stack
**Problem**: When an algorithm uses two stacks (one for operands, one for operators), pushing or popping the wrong one silently produces wrong answers.

**Solution**: Keep them clearly named and separated. Numbers only ever touch the value stack; operators only ever touch the operator stack. When you resolve an operator, pop two values, push one value. Never let an operator leak into the value stack.

---

## Practice Progression

Master the stack through this sequence of Grind75 problems:

1. **Valid Parentheses** — the canonical delimiter-matching problem. Push openers, match on closers, require an empty stack at the end. This builds the core push/pop/match reflex.

2. **Evaluate Reverse Polish Notation** — postfix evaluation. Operands wait on the stack; each operator pops two and pushes a result. Learn to respect operand order for `-` and `/`.

3. **Basic Calculator** — parsing with a sign/number/paren stack. Push the suspended outer context on `(` and fold the inner result back on `)`. This combines matching, evaluation, and nested context into one algorithm.

Work them in order: each one adds a layer onto the last. Matching teaches the mechanics, postfix teaches deferred evaluation, and the calculator teaches nested context.

---

## The Unifying Principle

A stack is about **deferring work until the right moment to resolve it**.

You push what you cannot finish yet, and the stack guarantees that when resolution comes, the right partner is always on top — the most recent unfinished thing. Nesting, matching, evaluation, and backtracking are all the same idea wearing different clothes: last in, first out.

*Push what you can't finish. Pop when the answer arrives. The top of the stack is always the next thing to resolve.*

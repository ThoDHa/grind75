# [Min Stack](https://leetcode.com/problems/min-stack/)

**Medium** | **20 minutes** | **Stack, Design**

**Pattern:** [Data-Structure Design](../patterns/design/intuition.md)

**Algorithm:** [Stack](https://en.wikipedia.org/wiki/Stack_(abstract_data_type))

**Practice:** [`practice/min_stack/solution.py`](../../practice/min_stack/solution.py)

Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.

Implement the MinStack class:

- `MinStack()` initializes the stack object.
- `void push(int val)` pushes the element val onto the stack.
- `void pop()` removes the element on the top of the stack.
- `int top()` gets the top element of the stack.
- `int getMin()` retrieves the minimum element in the stack.

You must implement a solution with `O(1)` time complexity for each function.

## Examples

### Example 1

**Input:**

```
["MinStack","push","push","push","getMin","pop","top","getMin"]
[[],[-2],[0],[-3],[],[],[],[]]
```

**Output:** `[null,null,null,null,-3,null,0,-2]`

**Explanation:**

```
MinStack minStack = new MinStack();
minStack.push(-2);
minStack.push(0);
minStack.push(-3);
minStack.getMin(); // return -3
minStack.pop();
minStack.top();    // return 0
minStack.getMin(); // return -2
```

## Constraints

- `-2^31 <= val <= 2^31 - 1`
- Methods `pop`, `top` and `getMin` operations will always be called on **non-empty** stacks.
- At most `3 * 10^4` calls will be made to `push`, `pop`, `top`, and `getMin`.

## Solutions

### Brute Force

```python
class MinStack:

    def __init__(self):
        self.stack: list[int] = []

    def push(self, val: int) -> None:
        self.stack.append(val)

    def pop(self) -> None:
        self.stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        # Scan the whole stack every time to find the smallest value.
        smallest = self.stack[0]
        for value in self.stack:
            if value < smallest:
                smallest = value
        return smallest


# Your MinStack object will be instantiated and used as such:
# obj = MinStack()
# obj.push(val)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()
```

#### Approach

The most direct idea ignores the `O(1)` requirement at first and keeps a single
plain [stack](https://en.wikipedia.org/wiki/Stack_(abstract_data_type)) of values. `push`, `pop`, and `top` are trivial list operations.
For `getMin`, with no extra bookkeeping, the only option is to walk every
element and track the smallest one seen.

1. Store pushed values in a single list used as a stack.
2. `push` appends, `pop` removes the last element, and `top` reads the last
   element.
3. `getMin` linearly scans the entire stack, comparing each value against a
   running smallest, and returns the smallest found.

This is correct and simple to reason about, but `getMin` does `O(n)` work, which
violates the problem's `O(1)` requirement. Tracing Example 1, after pushing
`-2`, `0`, `-3`, the scan over `[-2, 0, -3]` returns `-3`; after popping `-3`,
the scan over `[-2, 0]` returns `-2`. Correct, just slow.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(1)` for push/pop/top, `O(n)` for getMin

`push`, `pop`, and `top` touch only the last element, but `getMin` scans all `n`
elements on every call, so it fails the constant-time requirement.

##### Space Complexity: `O(n)`

A single list stores the `n` pushed values with no auxiliary structure.

#### Key Insights

- The naive baseline: store values plainly and recompute the minimum on demand.
- It exposes the real challenge, which is making `getMin` constant time rather
  than a full scan.
- Every later solution removes the `getMin` scan by caching the minimum as
  elements are pushed.

#### Walkthrough

Let us watch the Brute Force code run on Example 1, calling each method in order
on a fresh `MinStack`. After `__init__`, `self.stack` is the empty list `[]`.
The table shows `self.stack` after each call, plus what the call returns (`push`
and `pop` return nothing, shown as `None`).

| Call | What runs | `self.stack` after | Returns |
|------|-----------|--------------------|---------|
| `push(-2)` | `append(-2)` | `[-2]` | `None` |
| `push(0)` | `append(0)` | `[-2, 0]` | `None` |
| `push(-3)` | `append(-3)` | `[-2, 0, -3]` | `None` |
| `getMin()` | scan `[-2, 0, -3]` | `[-2, 0, -3]` | `-3` |
| `pop()` | `pop()` removes last | `[-2, 0]` | `None` |
| `top()` | read `stack[-1]` | `[-2, 0]` | `0` |
| `getMin()` | scan `[-2, 0]` | `[-2, 0]` | `-2` |

The two `getMin` calls are where the scan happens. Trace the first one: it sets
`smallest = stack[0] = -2`, then walks the list. `-2 < -2` is false, `0 < -2` is
false, `-3 < -2` is true so `smallest` becomes `-3`, and `-3` is returned. The
second `getMin` runs on the shorter list `[-2, 0]`: `smallest` starts at `-2`,
`0 < -2` is false, so it stays `-2` and returns `-2`.

Collecting every return value in order gives `[null, null, null, null, -3, null,
0, -2]`, which matches the example's expected Output.

### Single Stack of Pairs

```python
class MinStack:

    def __init__(self):
        # Each entry stores (value, minimum of the stack at and below this entry)
        self.stack: list[tuple[int, int]] = []

    def push(self, val: int) -> None:
        current_min = val if not self.stack else min(val, self.stack[-1][1])
        self.stack.append((val, current_min))

    def pop(self) -> None:
        self.stack.pop()

    def top(self) -> int:
        return self.stack[-1][0]

    def getMin(self) -> int:
        return self.stack[-1][1]


# Your MinStack object will be instantiated and used as such:
# obj = MinStack()
# obj.push(val)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()
```

#### Approach

The challenge is retrieving the minimum in `O(1)` even after arbitrary pops.
A plain stack can hold the values, but the running minimum changes as elements
are removed. The trick is to store the minimum alongside each value so every
entry remembers what the minimum was when it sat on top.

1. Store each pushed element as a pair `(val, current_min)`, where
   `current_min` is the smaller of `val` and the minimum currently on top of
   the stack.
2. On `push`, look at the previous top's stored minimum (or use `val` itself
   when the stack is empty) and record the new pair.
3. On `pop`, simply discard the top pair; the entry now on top already carries
   the correct minimum for the remaining elements.
4. `top` returns the value field of the top pair, and `getMin` returns its
   minimum field.

Because each entry caches the minimum of the entire stack beneath it, removing
the top never requires recomputation.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(1)` per operation

`push`, `pop`, `top`, and `getMin` each perform a constant number of list
operations and comparisons, so all four run in constant time as required.

##### Space Complexity: `O(n)`

Each of the `n` pushed elements stores an extra integer for the cached minimum,
which doubles the storage but remains linear in the number of elements.

#### Key Insights

- Pairing every value with the minimum-so-far converts the `getMin` query into
  a constant-time lookup of the top entry.
- The cached minimum is monotonic going down the stack, so popping the top
  automatically exposes the correct minimum underneath.
- Bundling both fields in a single list keeps the data structure compact: there
  is only one container to push to and pop from.

### Two Stacks

```python
class MinStack:

    def __init__(self):
        self.stack: list[int] = []
        # Parallel stack whose top is always the minimum of the value stack.
        self.mins: list[int] = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        # Carry forward the smaller of the new value and the current minimum.
        current_min = val if not self.mins else min(val, self.mins[-1])
        self.mins.append(current_min)

    def pop(self) -> None:
        self.stack.pop()
        self.mins.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.mins[-1]


# Your MinStack object will be instantiated and used as such:
# obj = MinStack()
# obj.push(val)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()
```

#### Approach

This variant splits the two concerns into two separate stacks that move in
lockstep: one holds the raw values, and the other tracks the running minimum so
its top always equals the minimum of everything currently in the value stack.

1. On `push`, append the value to the value stack. Then push the smaller of the
   new value and the current top of the minimum stack (or the value itself when
   the minimum stack is empty).
2. On `pop`, pop both stacks together so they stay aligned.
3. `top` returns the top of the value stack, and `getMin` returns the top of the
   minimum stack.

Because the minimum stack mirrors the value stack one-for-one, every pop exposes
the correct minimum for the remaining elements without recomputation.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(1)` per operation

Each method performs a fixed number of list appends, pops, and comparisons, so
all four operations run in constant time as required.

##### Space Complexity: `O(n)`

The minimum stack grows one entry per push, matching the value stack, so the
total storage is linear in the number of elements.

#### Key Insights

- Separating values from minimums keeps each stack holding plain integers, which
  some readers find clearer than reasoning about tuples.
- The minimum stack is non-increasing from bottom to top, so its top is always
  the global minimum of the current contents.
- Pushing and popping both stacks together is what guarantees alignment; the two
  stacks always have identical heights.

### Single Stack with Encoded Minimum

```python
class MinStack:

    def __init__(self):
        self.stack: list[int] = []
        self.min: int = 0

    def push(self, val: int) -> None:
        if not self.stack:
            self.stack.append(val)
            self.min = val
        elif val < self.min:
            # New minimum: store an encoded marker instead of the value.
            # Since val < min, 2*val - min = val + (val - min) < val, so the
            # stored entry is strictly below the new minimum (val). That is
            # what lets pop and top recognize it as encoded later.
            self.stack.append(2 * val - self.min)
            self.min = val
        else:
            self.stack.append(val)

    def pop(self) -> None:
        popped = self.stack.pop()
        if popped < self.min:
            # Encoded entry: the minimum changed at this element, so restore
            # the previous minimum. With popped = 2*val - old_min and
            # min = val, 2*min - popped = 2*val - 2*val + old_min = old_min.
            self.min = 2 * self.min - popped

    def top(self) -> int:
        value = self.stack[-1]
        # An encoded entry always represents the current minimum itself.
        return self.min if value < self.min else value

    def getMin(self) -> int:
        return self.min


# Your MinStack object will be instantiated and used as such:
# obj = MinStack()
# obj.push(val)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()
```

#### Approach

Both cached approaches above store an extra integer for every pushed element.
This variant keeps a single stack of plain integers plus one minimum variable,
and encodes the history of the minimum directly into the stored numbers, so the
only overhead beyond the values themselves is that one variable.

1. Keep one stack and a `min` variable holding the current minimum.
2. On `push`, if the value is at least the current minimum, store it as is. If
   it is a new minimum, store the encoded value `2 * val - min` instead and set
   `min = val`. Because `val < min`, the encoded number equals
   `val + (val - min)`, which is strictly less than `val`: every encoded entry
   sits strictly below the minimum that was current when it was pushed.
3. On `pop`, compare the removed entry against `min`. A value below `min` can
   only be an encoded "the minimum changed here" marker, so undo that change by
   decoding the previous minimum: `2 * min - popped` expands to
   `2 * val - (2 * val - old_min) = old_min`. A value at or above `min` is a
   plain entry and leaves the minimum untouched.
4. `top` applies the same test: a top entry below `min` is encoded, and the
   real value it represents is the current minimum itself; otherwise the entry
   is the value. `getMin` just returns the variable.

The invariant that makes this work is that no plain entry is ever below the
current minimum, so "stored entry is less than `min`" is an unambiguous signal
that the entry encodes a minimum change. Note that equal values are stored
plainly (the test is a strict `<`), so repeated minima pop off without
disturbing `min` until the entry that actually changed it is removed.

One honest caveat: in Python this is fully correct because integers have
arbitrary precision, so `2 * val - min` can never overflow. In fixed-width
languages the doubling can exceed the integer range (with `val` near the 32-bit
limits, `2 * val - min` needs a 64-bit type), so the trick demands a wider type
or careful bounds analysis. That fragility is why the pairs and two-stack
approaches are usually preferred in interviews unless the space follow-up is
asked explicitly.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(1)` per operation

- `push`: one comparison and at most one multiply-subtract before a single
  append.
- `pop`: one list pop plus a constant-time decode when the entry was encoded.
- `top`: one index lookup and one comparison.
- `getMin`: returns the stored variable directly.

##### Space Complexity: `O(n)`

The single stack holds exactly one integer per pushed element, and the only
auxiliary state is the one `min` variable: `O(1)` extra beyond the values. The
pairs and two-stack versions store up to `2n` integers for the same contents.

#### Key Insights

- The encoding is sentinel-free: no flag, tuple, or second container marks
  where the minimum changed. The ordering invariant itself (encoded entries are
  strictly below the current minimum) carries that information.
- It halves the constant factor on space: `n` stored numbers plus one variable,
  versus up to `2n` for the pairs and two-stack versions, while keeping every
  operation `O(1)`.
- The trick is not fully portable: `2 * val - min` relies on arithmetic that
  cannot overflow. Python grants that for free; C, C++, and Java require a
  wider intermediate type, which is why this is a follow-up answer rather than
  a default interview answer.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(1)` for push/pop/top, `O(n)` for getMin - the scan walks
  every element to find the minimum.
- **Single Stack of Pairs**: `O(1)` per operation - one tuple append, pop, or
  index lookup.
- **Two Stacks**: `O(1)` per operation - one append or pop on each of two stacks.
- **Single Stack with Encoded Minimum**: `O(1)` per operation - one append or
  pop plus a constant amount of encode/decode arithmetic.

### Space Complexity

- **Brute Force**: `O(n)` - a single list of values with no auxiliary structure.
- **Single Stack of Pairs**: `O(n)` - each element stores its value and the
  cached minimum together.
- **Two Stacks**: `O(n)` - the parallel minimum stack adds one integer per push.
- **Single Stack with Encoded Minimum**: `O(n)` - one integer per element plus
  a single minimum variable, so only `O(1)` extra beyond the values themselves.

### Trade-offs

- Brute Force is the simplest to write and uses the least memory, but its `O(n)`
  `getMin` fails the problem's constant-time requirement.
- The two cached approaches store the same amount of extra information (one
  cached minimum per element) and meet the `O(1)` requirement for every
  operation.
- The single stack keeps everything in one container, so push and pop touch only
  one list.
- The two-stack version keeps each container holding plain integers, which some
  find easier to read, at the cost of maintaining two lists in lockstep.
- The encoded variant is the leanest on memory (no second number per element),
  but the stored entries are no longer the raw values, so inspecting the stack
  requires decoding, and in fixed-width languages the arithmetic risks
  overflow.

### When to Use Each

- **Brute Force**: Never for this problem's stated `O(1)` constraint; useful only
  as a teaching baseline that motivates caching the minimum.
- **Single Stack of Pairs**: When you prefer a single data structure and are
  comfortable unpacking tuples.
- **Two Stacks**: When you prefer to keep values and minimums conceptually
  separate, or when an interviewer asks for the classic two-stack formulation.
- **Single Stack with Encoded Minimum**: When memory is at a premium, or as the
  answer to the follow-up "can you do it with `O(1)` extra space beyond the
  values?"; otherwise prefer the pairs or two-stack versions, which have no
  overflow caveat.

### Optimization Notes

- The brute force recomputes the minimum on every `getMin`; both cached solutions
  eliminate that scan by carrying the running minimum forward, which is the core
  trick that turns an `O(n)` query into an `O(1)` lookup.
- A further memory optimization stores only minimums that actually change (a
  monotonic minimum stack), shrinking the auxiliary stack when many pushes share
  the same minimum, at the cost of slightly more bookkeeping on pop.
- The encoded variant takes that idea to its limit: it records minimum changes
  in-place with arithmetic instead of extra storage, leaving exactly one number
  per element plus one variable. The cost is that the arithmetic must not
  overflow, which Python guarantees and fixed-width languages do not.

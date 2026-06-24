# [Maximum Frequency Stack](https://leetcode.com/problems/maximum-frequency-stack/)

**Hard** | **35 minutes** | **Hash Table, Stack, Design**

**Pattern:** [Data-Structure Design](../patterns/design/intuition.md)

**Practice:** [`practice/maximum_frequency_stack/solution.py`](../../practice/maximum_frequency_stack/solution.py)

Design a stack-like data structure to push elements to the stack and pop the most frequent element from the stack.

Implement the `FreqStack` class:

- `FreqStack()` constructs an empty frequency stack.
- `void push(int val)` pushes an integer `val` onto the top of the stack.
- `int pop()` removes and returns the most frequent element in the stack.
    - If there is a tie for the most frequent element, the element closest to the stack's top is removed and returned.

## Examples

### Example 1

**Input:**

```
["FreqStack", "push", "push", "push", "push", "push", "push", "pop", "pop", "pop", "pop"]
[[], [5], [7], [5], [7], [4], [5], [], [], [], []]
```

**Output:**

```
[null, null, null, null, null, null, null, 5, 7, 5, 4]
```

**Explanation:**

```
FreqStack freqStack = new FreqStack();
freqStack.push(5); // The stack is [5]
freqStack.push(7); // The stack is [5,7]
freqStack.push(5); // The stack is [5,7,5]
freqStack.push(7); // The stack is [5,7,5,7]
freqStack.push(4); // The stack is [5,7,5,7,4]
freqStack.push(5); // The stack is [5,7,5,7,4,5]
freqStack.pop();   // return 5, as 5 is the most frequent. The stack becomes [5,7,5,7,4].
freqStack.pop();   // return 7, as 5 and 7 is the most frequent, but 7 is closest to the top. The stack becomes [5,7,5,4].
freqStack.pop();   // return 5, as 5 is the most frequent. The stack becomes [5,7,4].
freqStack.pop();   // return 4, as 4, 5 and 7 is the most frequent, but 4 is closest to the top. The stack becomes [5,7].
```

## Constraints

- `0 <= val <= 10^9`
- At most `2 * 10^4` calls will be made to `push` and `pop`.
- It is guaranteed that there will be at least one element in the stack before calling `pop`.

## Solutions

### Brute Force

```python
class FreqStack:
    def __init__(self):
        """
        Brute force approach maintaining complete element history
        """
        self.stack = []  # Complete stack history
        self.freq_count = {}  # Current frequency of each element

    def push(self, val: int) -> None:
        """
        Add to stack and update frequency
        """
        self.stack.append(val)
        self.freq_count[val] = self.freq_count.get(val, 0) + 1

    def pop(self) -> int:
        """
        Find and remove most frequent element (most recent if tie)
        """
        if not self.stack:
            return -1

        # Find maximum frequency
        max_freq = max(self.freq_count.values())

        # Find the most recent element with maximum frequency
        for i in range(len(self.stack) - 1, -1, -1):
            val = self.stack[i]
            if self.freq_count[val] == max_freq:
                # Remove element from stack and update frequency
                self.stack.pop(i)
                self.freq_count[val] -= 1
                if self.freq_count[val] == 0:
                    del self.freq_count[val]
                return val

        return -1  # Should never reach here
```

#### Approach

This **brute force solution** maintains the complete stack and searches for the most frequent element during each pop operation. While correct, it's highly inefficient for large inputs but useful for understanding the problem requirements.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(1)` for push, `O(n)` for pop

Push is constant time, but pop requires scanning the entire stack to find the target element.

##### Space Complexity: `O(n)`

Maintains the complete element history in the stack.

#### Key Insights

- Keeping the literal push order in one list and a live frequency map is the most direct model: you can answer "most frequent, most recent" by reading both directly.
- The recency tie-break falls out of scanning the stack from the top down and stopping at the first element whose frequency equals the maximum.
- `pop(i)` from the middle of a Python list is `O(n)`, and `max(self.freq_count.values())` re-scans every distinct value, so each pop is linear; this is the cost the later designs eliminate.
- Correct for every valid sequence, but too slow at the upper constraint of `2 * 10^4` calls.

#### Walkthrough

Let us run the **Brute Force** code on Example 1: push `5, 7, 5, 7, 4, 5`, then call `pop()` four times. Each `push` appends to `stack` and bumps that value's count in `freq_count`.

| Operation | `stack` after | `freq_count` after |
| --- | --- | --- |
| `push(5)` | `[5]` | `{5: 1}` |
| `push(7)` | `[5, 7]` | `{5: 1, 7: 1}` |
| `push(5)` | `[5, 7, 5]` | `{5: 2, 7: 1}` |
| `push(7)` | `[5, 7, 5, 7]` | `{5: 2, 7: 2}` |
| `push(4)` | `[5, 7, 5, 7, 4]` | `{5: 2, 7: 2, 4: 1}` |
| `push(5)` | `[5, 7, 5, 7, 4, 5]` | `{5: 3, 7: 2, 4: 1}` |

Now the pops. Each `pop()` first computes `max_freq = max(freq_count.values())`, then scans `stack` from the top down (`i` from the last index toward `0`) and removes the first value whose count equals `max_freq`:

- `pop()`: `max_freq` is `3`. Scanning from the top, the last `5` (index `5`) has count `3`, so it is removed and its count drops. `stack` becomes `[5, 7, 5, 7, 4]`, `freq_count` becomes `{5: 2, 7: 2, 4: 1}`. Returns `5`.
- `pop()`: `max_freq` is `2`. Scanning from the top, `4` (count `1`) is skipped, then `7` (count `2`) matches and is removed. `stack` becomes `[5, 7, 5, 4]`, `freq_count` becomes `{5: 2, 7: 1, 4: 1}`. Returns `7`: the tie between `5` and `7` resolves to `7` because it sits closer to the top.
- `pop()`: `max_freq` is `2`. Scanning from the top, `4` (count `1`) is skipped, then `5` (count `2`) matches and is removed. `stack` becomes `[5, 7, 4]`, `freq_count` becomes `{5: 1, 7: 1, 4: 1}`. Returns `5`.
- `pop()`: `max_freq` is `1`. The top element `4` (count `1`) matches immediately and is removed. `stack` becomes `[5, 7]`, `freq_count` becomes `{5: 1, 7: 1}`. Returns `4`.

The four pops return `5, 7, 5, 4`, which matches the expected Output `[null, null, null, null, null, null, null, 5, 7, 5, 4]` for the pop calls.

### Stack of Stacks

```python
class FreqStack:
    def __init__(self):
        """
        Stack of stacks approach - group elements by frequency level
        """
        self.freq_count = {}  # val -> frequency count
        self.freq_stacks = {}  # frequency -> stack of elements with that frequency
        self.max_freq = 0     # track maximum frequency seen

    def push(self, val: int) -> None:
        """
        Push element and update frequency tracking
        """
        # Update frequency count
        self.freq_count[val] = self.freq_count.get(val, 0) + 1
        freq = self.freq_count[val]

        # Update maximum frequency
        self.max_freq = max(self.max_freq, freq)

        # Add to appropriate frequency stack
        if freq not in self.freq_stacks:
            self.freq_stacks[freq] = []
        self.freq_stacks[freq].append(val)

    def pop(self) -> int:
        """
        Pop the most frequent element (most recent if tie)
        """
        # Get element from highest frequency stack
        val = self.freq_stacks[self.max_freq].pop()

        # Decrease frequency count
        self.freq_count[val] -= 1

        # Update max_freq if highest frequency stack becomes empty
        if not self.freq_stacks[self.max_freq]:
            self.max_freq -= 1

        return val
```

#### Approach

This solution uses a **stack of stacks design** where each frequency level has its own stack. Elements are grouped by their current frequency, and we maintain the maximum frequency seen. The key insight is that elements with the same frequency should be processed in LIFO order (most recent first), which naturally handles the tie-breaking requirement.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(1)` for both push and pop operations

All operations involve simple hash map lookups and stack operations, which are constant time.

##### Space Complexity: `O(n)`

Where n is the total number of elements pushed. Each element appears in exactly one frequency stack at any time.

#### Key Insights

- Grouping elements by their current frequency turns "find the most frequent" into "look at the highest non-empty bucket", a constant-time lookup.
- The LIFO order within each frequency bucket encodes recency for free, so ties resolve to the element closest to the top without any timestamps.
- Tracking `max_freq` and decrementing it when its bucket empties is the only bookkeeping needed; the next-lower bucket is always non-empty when this happens.
- This is the optimal from-scratch design: no library handles the priority logic.

### Heap with Timestamps

```python
import heapq
from collections import defaultdict

class FreqStack:
    def __init__(self):
        """
        Priority queue approach with timestamp-based tie breaking
        """
        self.freq_count = defaultdict(int)  # val -> frequency
        self.max_heap = []  # (-frequency, -timestamp, val)
        self.timestamp = 0  # global timestamp counter

    def push(self, val: int) -> None:
        """
        Push element with frequency and timestamp tracking
        """
        self.timestamp += 1
        self.freq_count[val] += 1

        # Push to max heap (use negative values for max heap behavior)
        heapq.heappush(self.max_heap,
                      (-self.freq_count[val], -self.timestamp, val))

    def pop(self) -> int:
        """
        Pop element with highest frequency (most recent timestamp if tie)
        """
        neg_freq, neg_timestamp, val = heapq.heappop(self.max_heap)
        self.freq_count[val] -= 1
        return val
```

#### Approach

This solution lets a **priority queue (max heap)** do the priority work. Each push records an entry keyed by `(-frequency, -timestamp, val)`, so the heap always surfaces the element with the highest current frequency, breaking ties toward the most recent push.

1. On push, increment the element's frequency and a global timestamp counter, then push the tuple `(-frequency, -timestamp, val)`.
2. On pop, take the heap's top tuple. Because each push records the frequency the element had *at that moment*, the top entry is always the live winner; no stale entries can outrank it.
3. Decrement the popped element's frequency so future comparisons stay accurate.

The negated frequency and timestamp turn Python's min-heap into a max-heap that prefers higher frequency first, then later pushes.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(log n)` for both operations

Each push and pop is a single heap operation over up to `n` entries, so both cost `O(log n)`.

##### Space Complexity: `O(n)`

The heap holds one entry per push, one per element occurrence, which is linear in the number of pushed elements.

#### Key Insights

- A heap reframes the problem as a generic priority queue, which is easy to reach for but lets the library carry the core logic.
- Encoding the snapshot frequency at push time means the top entry is never stale, so no lazy deletion is required.
- The `(-freq, -timestamp)` key is the trick: it layers the recency tie-break underneath the frequency priority in one comparison.
- It is asymptotically slower than the stack-of-stacks design and depends on `heapq`, so it ranks below the from-scratch solutions.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(1)` push, `O(n)` pop - scanning the stack and re-scanning the frequency map on every pop.
- **Stack of Stacks**: `O(1)` for both operations - hash map lookups and per-frequency stack pushes/pops.
- **Heap with Timestamps**: `O(log n)` for both operations - a single heap push or pop over up to `n` entries.

### Space Complexity

- **Brute Force**: `O(n)` - complete stack history plus a frequency map.
- **Stack of Stacks**: `O(n)` - each element stored once across the per-frequency stacks.
- **Heap with Timestamps**: `O(n)` - one heap entry per push, never reclaimed.

### Trade-offs

- **Brute Force**: Linear pop and a re-scanned frequency map, but the most direct mental model and no library reliance. Suitable as a from-scratch baseline for understanding the problem.
- **Stack of Stacks**: Optimal `O(1)` operations with one stored copy per element, built entirely from hash maps and lists. Slightly more bookkeeping than the brute force, but the cleanest fast design.
- **Heap with Timestamps**: Easy to reach for if you already think in priority queues, but it hands the core priority logic to `heapq`, runs in `O(log n)`, and keeps every pushed entry forever.

### When to Use Each

- **Brute Force**: When establishing correctness first, or for very small inputs where the linear pop is irrelevant.
- **Stack of Stacks**: The recommended default - optimal performance with a clean, library-free design.
- **Heap with Timestamps**: When a priority-queue framing is clearer to communicate, accepting the slower bound and the `heapq` dependency.

### Optimization Notes

- The **Stack of Stacks** solution is the recommended approach: it achieves `O(1)` time for both push and pop by grouping elements into a separate stack per frequency level.
- The key implementation detail is tracking `max_freq` and pushing each element onto the stack keyed by its new frequency. Popping from the `max_freq` stack naturally returns the most frequent element, and LIFO ordering within that stack handles the recency tie-breaking automatically.
- A common pitfall is mishandling `max_freq` after a pop: when the highest-frequency stack becomes empty, `max_freq` must be decremented so the next pop targets the correct level.
- The **Heap with Timestamps** design works because each push records the frequency the element had at that instant, so the heap's top entry is always the live winner and no lazy deletion of stale entries is required.
- This problem demonstrates the "group by property" design pattern. Such frequency-based priority systems appear in caching algorithms, load balancing, and resource allocation.

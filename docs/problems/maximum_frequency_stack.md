# [Maximum Frequency Stack](https://leetcode.com/problems/maximum-frequency-stack/)

**Hard** | **35 minutes** | **Hash Table, Stack, Design**

**Pattern:** [Data-Structure Design](../patterns/design/intuition.md)

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
        # Pop from heap until we find an element with correct frequency
        while self.max_heap:
            neg_freq, neg_timestamp, val = heapq.heappop(self.max_heap)
            expected_freq = self.freq_count[val]

            # Check if this entry is still valid
            if -neg_freq == expected_freq:
                self.freq_count[val] -= 1
                return val
            # If not valid, this is a stale entry, continue popping

        return -1  # Should never reach here per problem constraints
```

#### Approach

This solution uses a **priority queue (max heap)** with timestamps to handle both frequency priority and recency tie-breaking. Each push adds an entry with current frequency and timestamp. The challenge is handling stale entries when frequencies change.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(log n)` for both operations

Heap operations dominate the time complexity. In worst case, pop might need to remove several stale entries.

##### Space Complexity: `O(n)`

The heap can contain multiple entries for the same element with different frequencies.

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

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(1)` push, `O(n)` pop - Poor for pop
- **Heap with Timestamps**: `O(log n)` for both operations - Good
- **Stack of Stacks**: `O(1)` for both operations - Optimal

### Space Complexity

- **Brute Force**: `O(n)` - Complete stack history
- **Heap with Timestamps**: `O(n)` - Multiple entries per element possible
- **Stack of Stacks**: `O(n)` - Each element stored once

### Trade-offs

- **Brute Force**: Poor time efficiency for pop operations and only fair space efficiency. Implementation complexity is low and conceptual clarity is very high. Suitable for learning only in an interview setting.
- **Heap with Timestamps**: Good time efficiency and good space efficiency. Implementation complexity is high and conceptual clarity is medium. Serves as an alternative approach in interviews.
- **Stack of Stacks**: Optimal time efficiency with excellent space efficiency. Implementation complexity is medium and conceptual clarity is high. This is the most preferred solution in interviews.

### When to Use Each

- **Brute Force**: Only for understanding problem requirements or very small constraint scenarios
- **Heap with Timestamps**: When you want to demonstrate heap knowledge or when the problem has different constraints
- **Stack of Stacks**: Best solution for production and interviews - optimal performance with clean design

### Optimization Notes

- The **Stack of Stacks** solution is the recommended approach: it achieves `O(1)` time for both push and pop by grouping elements into a separate stack per frequency level.
- The key implementation detail is tracking `max_freq` and pushing each element onto the stack keyed by its new frequency. Popping from the `max_freq` stack naturally returns the most frequent element, and LIFO ordering within that stack handles the recency tie-breaking automatically.
- A common pitfall is mishandling `max_freq` after a pop: when the highest-frequency stack becomes empty, `max_freq` must be decremented so the next pop targets the correct level.
- This problem demonstrates the "group by property" design pattern. Unlike the priority queue approach, which requires lazy deletion of stale entries, the stack-of-stacks design avoids that complexity entirely. Such frequency-based priority systems appear in caching algorithms, load balancing, and resource allocation.

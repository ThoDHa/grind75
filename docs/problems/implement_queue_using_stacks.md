# [Implement Queue using Stacks](https://leetcode.com/problems/implement-queue-using-stacks/)

**Easy** | **20 minutes** | **Stack, Queue, Design**

**Pattern:** [Data-Structure Design](../patterns/design/intuition.md)

**Practice:** [`practice/implement_queue_using_stacks/solution.py`](../../practice/implement_queue_using_stacks/solution.py)

Implement a first in first out (FIFO) queue using only two stacks. The implemented queue should support all the functions of a normal queue (`push`, `pop`, `peek`, and `empty`).

Implement the `MyQueue` class:

- `void push(int x)` Pushes element x to the back of the queue.
- `int pop()` Removes the element from the front of the queue and returns it.
- `int peek()` Returns the element at the front of the queue.
- `boolean empty()` Returns `true` if the queue is empty, `false` otherwise.

**Notes:**

- You must use only standard operations of a stack, which means only `push to top`, `peek/pop from top`, `size`, and `is empty` operations are valid.
- Depending on your language, the stack may not be supported natively. You may simulate a stack using a list or deque (double-ended queue) as long as you use only a stack's standard operations.

## Examples

### Example 1

**Input:**

```
["MyQueue", "push", "push", "peek", "pop", "empty"]
[[], [1], [2], [], [], []]
```

**Output:**

```
[null, null, null, 1, 1, false]
```

**Explanation:**

```
MyQueue myQueue = new MyQueue();
myQueue.push(1); // queue is: [1]
myQueue.push(2); // queue is: [1, 2] (leftmost is front of the queue)
myQueue.peek(); // return 1
myQueue.pop(); // return 1, queue is [2]
myQueue.empty(); // return false
```

## Constraints

- `1 <= x <= 9`
- At most `100` calls will be made to `push`, `pop`, `peek`, and `empty`.
- All the calls to `pop` and `peek` are valid.

Follow-up: Can you implement the queue such that each operation is amortized `O(1)` time complexity? In other words, performing n operations will take overall `O(n)` time even if one of those operations may take longer.

## Solutions

### Eager Push

```python
class MyQueue:
    def __init__(self):
        self.stack = []  # Temporary stack for rearranging elements
        self.queue = []  # Main stack that holds elements in queue order

    def push(self, x: int) -> None:
        # Transfer all elements to temporary stack (reversing order)
        while self.queue:
            self.stack.append(self.queue.pop())

        # Add new element to empty queue (will be at the bottom when elements are moved back)
        self.queue.append(x)

        # Transfer elements back to queue (restoring original order with new element at bottom)
        while self.stack:
            self.queue.append(self.stack.pop())

    def pop(self) -> int:
        # Front of queue is at the top of our queue stack
        return self.queue.pop()

    def peek(self) -> int:
        # Front of queue is at the top of our queue stack
        return self.queue[-1]

    def empty(self) -> bool:
        # Check if the queue stack is empty
        return len(self.queue) == 0
```

#### Approach

This solution implements a queue using two stacks with an "eager" approach where elements are rearranged immediately during the push operation:

1. We maintain a primary stack (`queue`) where elements are stored in queue order
2. When pushing a new element:
    - We transfer all existing elements to a temporary stack, reversing their order
    - Place the new element at the bottom of the queue
    - Transfer all elements back to maintain queue order
3. This arrangement ensures the oldest elements (front of queue) are always at the top of our main stack

#### Time and Space Complexity Analysis

##### Time Complexity

- **push**: `O(n)` - We need to move all n elements twice for each push operation
- **pop**: `O(1)` - Simply remove from the top of the stack
- **peek**: `O(1)` - Simply view the top of the stack
- **empty**: `O(1)` - Just check if the stack is empty

##### Space Complexity: `O(n)`

We need space proportional to the number of elements in the queue.

#### Key Insights

- This implementation sacrifices push efficiency to make pop and peek operations very fast
- The main stack always maintains elements in queue order, with oldest elements at the top
- This approach provides consistent (non-amortized) `O(1)` time for pop and peek operations
- The rearrangement during push operations ensures proper queue ordering

#### Walkthrough

Let us watch the Eager Push solution run on Example 1, the call sequence `push(1)`, `push(2)`, `peek()`, `pop()`, `empty()`. The key idea to hold in mind: `queue` is a list used as a stack, so its last element (rightmost, written here as the top) is what `pop()` and `peek()` see. The whole trick keeps the front of the queue sitting at that top.

`push(1)`: `queue` starts empty, so the first `while self.queue` loop does nothing. We append `1`, giving `queue = [1]`. The second loop finds `stack` empty, so nothing moves back.

`push(2)`: now `queue = [1]` is not empty. The first loop pops `1` off `queue` and pushes it onto `stack`: `queue = []`, `stack = [1]`. We append the new element: `queue = [2]`. The second loop pops `1` off `stack` and pushes it onto `queue`: `queue = [2, 1]`, `stack = []`. Notice `1` (the older element, the front of the queue) is now at the top (rightmost), exactly where `pop` and `peek` look.

Tracking the state after each push:

| Call | `queue` (top is rightmost) | `stack` |
| --- | --- | --- |
| `push(1)` | `[1]` | `[]` |
| `push(2)` | `[2, 1]` | `[]` |

`peek()`: returns `self.queue[-1]`, which is `1`. The queue is unchanged: `queue = [2, 1]`.

`pop()`: returns `self.queue.pop()`, removing and returning the top, `1`. Now `queue = [2]`, leaving `2` ready as the next front.

`empty()`: checks `len(self.queue) == 0`. Since `queue = [2]` has one element, it returns `false`.

The three non-`null` calls return `1`, `1`, and `false`, so the full output sequence is `[null, null, null, 1, 1, false]`, matching the expected Output.

### Lazy Pop

```python
class MyQueue:
    def __init__(self):
        self.stack_input = []  # For push operations
        self.stack_output = []  # For pop/peek operations

    def push(self, x: int) -> None:
        # Simply push element to input stack
        self.stack_input.append(x)

    def pop(self) -> int:
        # Ensure output stack has elements
        self._ensure_output_has_values()
        # Return and remove the front element
        return self.stack_output.pop()

    def peek(self) -> int:
        # Ensure output stack has elements
        self._ensure_output_has_values()
        # Return the front element without removing it
        return self.stack_output[-1]

    def empty(self) -> bool:
        # Queue is empty if both stacks are empty
        return len(self.stack_input) == 0 and len(self.stack_output) == 0

    def _ensure_output_has_values(self) -> None:
        # If output stack is empty, transfer all elements from input stack
        if not self.stack_output:
            while self.stack_input:
                self.stack_output.append(self.stack_input.pop())
```

#### Approach

This solution uses a "lazy" approach with two stacks serving different purposes:

1. `stack_input`: Used exclusively for push operations - new elements are simply added here
2. `stack_output`: Used exclusively for pop/peek operations - elements are consumed from here

The key insight is that we only transfer elements from input to output when necessary:

- When pushing, we simply add to the input stack (fast operation)
- When popping/peeking, we check if the output stack is empty:
    - If empty, we transfer all elements from input to output (which reverses their order)
    - If not empty, we directly use the output stack
- This transfer naturally reverses the elements, converting LIFO to FIFO behavior

#### Time and Space Complexity Analysis

##### Time Complexity

- **push**: `O(1)` - Simply append to the input stack
- **pop**: Amortized `O(1)` - While a single pop might take `O(n)` when transferring elements,
  across multiple operations it averages to `O(1)` per operation
- **peek**: Amortized `O(1)` - Same reasoning as pop
- **empty**: `O(1)` - Just check if both stacks are empty

##### Space Complexity: `O(n)`

We need space proportional to the number of elements in the queue.

#### Key Insights

- This approach optimizes push operations at the expense of occasional costly pop/peek operations
- Elements are only transferred when necessary, avoiding redundant operations
- Each element is moved at most twice (once to input stack, once to output stack)
- The amortization of the transfer cost makes this approach efficient for n operations
- This implementation directly addresses the follow-up question about amortized `O(1)` time complexity

## Comparison of Solutions

### Time Complexity

- **Eager Push**: `push` is `O(n)` because every push moves all elements twice, while `pop`, `peek`, and `empty` are each a guaranteed `O(1)`.
- **Lazy Pop**: `push` is `O(1)` (a simple append to the input stack), `pop` and `peek` are amortized `O(1)` (an occasional transfer costs `O(n)` but averages out across operations), and `empty` is `O(1)`.

### Space Complexity

Both approaches use `O(n)` space to store all queue elements.

### Trade-offs

- **Eager Push**:
    - Pros: Predictable performance for pop/peek with guaranteed `O(1)` time
    - Cons: Every push operation is expensive (`O(n)`), regardless of subsequent operations
    - Best when: Pop/peek operations are much more frequent than push operations

- **Lazy Pop**:
    - Pros: More efficient overall, with better amortized performance
    - Cons: Individual pop/peek operations might occasionally be expensive
    - Best when: Push operations are frequent or balanced with pop/peek operations

### When to Use Each

- **Use Eager Push when**:
    - Consistent, non-amortized time for pop/peek is critical
    - Queue size remains small, limiting the cost of push operations
    - Pop/peek operations significantly outnumber push operations

- **Use Lazy Pop when**:
    - Overall efficiency across multiple operations is the priority
    - Amortized performance is acceptable
    - Push operations are frequent
    - The follow-up requirement for amortized `O(1)` operations needs to be satisfied

### Optimization Notes

- The lazy approach is generally more efficient in practice for most use cases
- For the follow-up question requiring amortized `O(1)` operations, the lazy approach is the appropriate solution
- Both approaches demonstrate the fundamental computer science principle of time-space tradeoffs
- The lazy approach exemplifies how amortization analysis can reveal algorithms that are efficient over a sequence of operations, even if individual operations sometimes take longer

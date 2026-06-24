# [Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/)

**Easy** | **15 minutes** | **Linked List, Recursion**

**Pattern:** [Linked List Reversal](../patterns/linked_list_in_place_reversal/intuition.md)

**Practice:** [`practice/reverse_linked_list/solution.py`](../../practice/reverse_linked_list/solution.py)

Given the `head` of a singly linked list, reverse the list, and return the reversed list.

## Examples

### Example 1

![Reverse Linked List Example 1](assets/reverse_linked_list_example1.jpg)

**Input:** `head = [1,2,3,4,5]`

**Output:** `[5,4,3,2,1]`

### Example 2

![Reverse Linked List Example 2](assets/reverse_linked_list_example2.jpg)

**Input:** `head = [1,2]`

**Output:** `[2,1]`

### Example 3

**Input:** `head = []`

**Output:** `[]`

## Constraints

- The number of nodes in the list is the range `[0, 5000]`.
- `-5000 <= Node.val <= 5000`

**Follow up:** A linked list can be reversed either iteratively or recursively. Could you implement both?

## Solutions

### Brute Force

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # Collect every value in forward order
        values = []
        curr = head
        while curr:
            values.append(curr.val)
            curr = curr.next
        # Walk the nodes again, overwriting each with the value from the back
        curr = head
        i = len(values) - 1
        while curr:
            curr.val = values[i]
            i -= 1
            curr = curr.next
        return head
```

#### Approach

The most direct idea ignores pointer rewiring entirely and instead moves the data. Read all the node values into an array, then walk the same nodes a second time, writing the values back in reverse order. The list structure never changes; only the payload in each node is swapped end for end.

1. Traverse the list once, appending every node's `val` to a `values` array in forward order.
2. Traverse the list a second time from `head`, writing `values[i]` into the current node while `i` counts down from the last index.
3. Return the original `head`, whose nodes now hold the values in reversed order.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Where `n` is the number of nodes in the linked list. Two separate passes each touch every node once, which is still linear.

##### Space Complexity: `O(n)`

The `values` array holds a copy of every node's value, so the auxiliary storage grows linearly with the list length.

#### Key Insights

- Reverses by relocating values rather than flipping links, which is the easiest correct idea to reach without knowing the pointer trick.
- Requires `O(n)` extra space for the value buffer, the cost of not touching the structure.
- Mutating values in place works for a singly linked list, but it would not generalize to cases where node identity or attached payloads must move with the data.

### Iterative

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev = None
        curr = head
        while curr:
            next_node = curr.next
            curr.next = prev
            prev = curr
            curr = next_node
        return prev
```

#### Approach

This solution reverses the linked list iteratively using three pointers. We maintain a `prev` pointer that initially points to `None` (representing the new tail), a `curr` pointer at the node being processed, and a temporary `next_node` reference. For each node in the original list, we:

1. Save the current node's `next` into `next_node` before the link is overwritten.
2. Point the current node's `next` back to `prev`, reversing that edge.
3. Advance `prev` to the current node, growing the reversed portion.
4. Advance `curr` to the saved `next_node`, moving on to the next node.

When `curr` becomes `None`, every edge has been flipped and `prev` points to the original tail, which is the new head of the reversed list.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Where `n` is the number of nodes in the linked list. We visit each node exactly once.

##### Space Complexity: `O(1)`

We use a constant amount of extra space regardless of input size. Only three pointer variables are needed.

#### Key Insights

- An in-place algorithm that flips one edge per iteration without any auxiliary data structure.
- Saving `curr.next` before rewiring is essential: once `curr.next` is reassigned to `prev`, the forward link is gone, so the traversal must capture it first.
- A single pass with constant space makes it the most efficient choice for long lists.

### Recursive

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next:
            return head
        new_head = self.reverseList(head.next)
        head.next.next = head
        head.next = None
        return new_head
```

#### Approach

The recursive solution reverses the tail first, then fixes the current node on the way back up the call stack:

1. The base case returns `head` directly for an empty list or a single node, since either is already reversed.
2. Recurse on `head.next` to reverse the rest of the list; `new_head` is the original tail, which becomes the head of the reversed list and is passed back unchanged through every frame.
3. After the recursion returns, `head.next` is the tail of the already-reversed sublist, so set `head.next.next = head` to make it point back to `head`.
4. Set `head.next = None` so `head` becomes the new tail and the old forward link is broken.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Where `n` is the number of nodes in the linked list. Each node is visited once during the descent and fixed once during the return.

##### Space Complexity: `O(n)`

The recursion creates a stack of function calls proportional to the list length. In the worst case, the recursion depth equals the number of nodes.

#### Key Insights

- Elegant recursive formulation that naturally expresses reversing the tail before the head.
- The `head.next = None` line is mandatory: skipping it leaves the old forward link intact and creates a cycle between the last two nodes of the reversed list.
- More concise to read but carries call-stack overhead, which matters for long lists.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n)` - Two passes, but still linear overall
- **Iterative**: `O(n)` - Single pass through the list
- **Recursive**: `O(n)` - Also processes each node once

### Space Complexity

- **Brute Force**: `O(n)` - Buffers every node's value in an array
- **Iterative**: `O(1)` - Uses fixed amount of extra space
- **Recursive**: `O(n)` - Uses call stack space proportional to list length

### Trade-offs

- The brute force solution is the easiest to derive but spends `O(n)` extra space to copy values rather than rewire links
- The iterative solution is more space-efficient but requires tracking multiple pointers
- The recursive solution is more elegant but uses more memory due to the call stack

### When to Use Each

- **Brute Force**: As a first correct attempt or when reversing values is acceptable and structure must stay fixed
- **Iterative**: When memory efficiency is important or the list might be very long
- **Recursive**: When code readability is valued over memory efficiency and the list is reasonably sized

### Optimization Notes

- **The iterative approach is the recommended solution**: it reverses the list in a single pass using `O(1)` space and avoids the call-stack overhead of recursion, which matters given the constraint of up to 5000 nodes
- A key implementation detail is saving `curr.next` into a `next_node` variable before rewiring the pointer: once `curr.next` is reassigned to `prev`, the original forward link is lost, so the traversal must capture it first
- Avoid the recursive approach for long lists: its `O(n)` stack depth can trigger a stack overflow (Python's default recursion limit is around 1000), and the same per-node pointer rewiring is achievable iteratively without that risk
- In the recursive solution, do not forget the `head.next = None` line: skipping it leaves the old forward link intact and creates a cycle between the last two nodes of the reversed list

# [Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/)

**Easy** | **20 minutes** | **Linked List, Two Pointers**

**Pattern:** [Two Pointers](../patterns/two_pointers/intuition.md)

**Practice:** [`practice/linked_list_cycle/solution.py`](https://github.com/ThoDHa/grind75/blob/main/practice/linked_list_cycle/solution.py)

Given `head`, the head of a linked list, determine if the linked list has a cycle in it.

There is a cycle in a linked list if there is some node in the list that can be reached again by continuously following the `next` pointer. Internally, `pos` is used to denote the index of the node that tail's `next` pointer is connected to. **Note that `pos` is not passed as a parameter**.

Return `true` if there is a cycle in the linked list. Otherwise, return `false`.

## Examples

### Example 1

![Linked List Cycle Example 1](assets/linked_list_cycle_example1.png)

**Input:** `head = [3,2,0,-4]`, `pos = 1`

**Output:** `true`

**Explanation:** There is a cycle in the linked list, where the tail connects to the 1st node (0-indexed).

### Example 2

![Linked List Cycle Example 2](assets/linked_list_cycle_example2.png)

**Input:** `head = [1,2]`, `pos = 0`

**Output:** `true`

**Explanation:** There is a cycle in the linked list, where the tail connects to the 0th node.

### Example 3

![Linked List Cycle Example 3](assets/linked_list_cycle_example3.png)

**Input:** `head = [1]`, `pos = -1`

**Output:** `false`

**Explanation:** There is no cycle in the linked list.

## Constraints

- The number of the nodes in the list is in the range `[0, 10^4]`.
- `-10^5 <= Node.val <= 10^5`
- `pos` is `-1` or a valid index in the linked-list.

## Solutions

### Hash Set

```python
class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        seen = set()
        while head:
            if head in seen:
                return True
            seen.add(head)
            head = head.next
        return False
```

#### Approach

This solution uses a hash set to keep track of nodes we've already visited. As we traverse the linked list, we check if we've seen the current node before. If we have, there must be a cycle. If we reach the end of the list (a null pointer), then there's no cycle.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Where `n` is the number of nodes in the linked list. In the worst case, we might need to visit all nodes once.

##### Space Complexity: `O(n)`

We store each node in the hash set, which in the worst case would contain all `n` nodes.

#### Key Insights

- Hash set provides `O(1)` lookups to quickly check if a node was seen before
- Simple implementation that's easy to understand
- The space complexity is proportional to the size of the list

### Marking Visited Nodes

```python
class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        while head:
            if head.val == float('inf'):
                return True
            head.val = float('inf')
            head = head.next
        return False
```

#### Approach

This solution marks nodes as visited by changing their values to a special sentinel value (like `float('inf')`). As we traverse the list, if we encounter a node that's already been marked, we know there's a cycle. This approach assumes we're allowed to modify the original list structure.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Where `n` is the number of nodes. We traverse the list once.

##### Space Complexity: `O(1)`

We don't use any extra data structures that scale with input size.

#### Key Insights

- Very space-efficient as it uses constant extra space
- Simple implementation
- The main drawback is that it modifies the original list, which may not be allowed in some scenarios

### Floyd's Cycle Detection

```python
class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        slow = head
        fast = head
        while slow and fast and fast.next:
            slow = slow.next          # advance slow by one step
            fast = fast.next.next     # advance fast by two steps
            if slow == fast:
                return True
        return False
```

#### Approach

This solution implements Floyd's Cycle-Finding Algorithm, also known as the "tortoise and hare" algorithm. We use two pointers that move at different speeds: a slow pointer that moves one step at a time and a fast pointer that moves two steps at a time. If there's a cycle, the fast pointer will eventually catch up to the slow pointer. If there's no cycle, the fast pointer will reach the end of the list.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Where `n` is the number of nodes. In the worst case with a cycle, the slow and fast pointers will meet after the slow pointer has traversed at most `n` steps.

##### Space Complexity: `O(1)`

We only use two pointers regardless of the input size.

#### Key Insights

- Uses constant extra space, making it more memory-efficient than the hash set approach
- Elegant mathematical solution that leverages the cycle property
- When pointers move at different speeds in a cycle, they'll eventually meet

## Comparison of Solutions

### Time Complexity

- **Hash Set**: `O(n)` - Traverses the list once
- **Marking Nodes**: `O(n)` - Single traversal of the list
- **Floyd's Cycle Detection**: `O(n)` - Also traverses the list with slow and fast pointers

### Space Complexity

- **Hash Set**: `O(n)` - Stores all nodes in a hash set
- **Marking Nodes**: `O(1)` - No additional data structures
- **Floyd's Cycle Detection**: `O(1)` - Uses only two pointers

### Trade-offs

- The hash set solution is intuitive but uses more memory
- The marking approach is memory-efficient but modifies the original list
- The two-pointer solution is memory-efficient and doesn't modify the list

### When to Use Each

- **Hash Set**: When simplicity is valued over memory efficiency
- **Marking Nodes**: When memory efficiency is important and modifying the list is allowed
- **Floyd's Cycle Detection**: When memory efficiency is important and we can't modify the list

### Optimization Notes

- **Floyd's Cycle Detection is the optimal solution**: it achieves `O(n)` time and `O(1)` space while leaving the list untouched, combining the best properties of the other two approaches
- A key implementation detail is the loop guard `while slow and fast and fast.next`: the fast pointer advances two steps per iteration, so both `fast` and `fast.next` must be non-null before dereferencing `fast.next.next`, otherwise an empty or odd-length acyclic list raises an `AttributeError`
- Avoid the Marking Nodes approach unless mutation is explicitly permitted: overwriting `val` with `float('inf')` destroys the original data and produces a false positive if any legitimate node already held that sentinel value
- The Hash Set approach keys on node identity rather than value, so it correctly handles duplicate values; do not refactor it to store `head.val`, which would falsely report a cycle whenever two distinct nodes share the same value

# [Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/)

Easy - 15 minutes - Linked List, Recursion

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

### Solution 1: Iterative Approach

```python
def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
    reversed = None
    while head:
        temp = head.next    # Save the next node
        head.next = reversed    # Reverse the pointer
        reversed = head     # Move reversed pointer to current node
        head = temp         # Move to the next node
    return reversed
```

#### Approach

This solution reverses the linked list iteratively. We maintain a `reversed` pointer that initially points to `None` (representing the new tail). For each node in the original list, we:

1. Store the next node temporarily
2. Point the current node's `next` to the previously reversed list
3. Update the reversed list to include the current node
4. Move to the next node in the original list

By the end, we have completely reversed the direction of all pointers in the list.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Where `n` is the number of nodes in the linked list. We visit each node exactly once.

##### Space Complexity: `O(1)`

We use a constant amount of extra space regardless of input size. We're only using a few additional pointers.

#### Key Insights

- Simple iterative approach that's efficient and easy to understand
- In-place algorithm that doesn't require additional data structures
- Makes a single pass through the list

### Solution 2: Recursive Approach

```python
def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
    # Base case: empty list or list with one node
    if not head or not head.next:
        return head
    
    # Recursively reverse the rest of the list after head
    new_head = self.reverseList(head.next)
    
    # Reverse the pointer: make head.next point back to head
    head.next.next = head
    
    # Break the original link to avoid cycles
    head.next = None
    
    # Return the new head of the reversed list
    return new_head
```

#### Approach

The recursive solution approaches the problem by:

1. Recursively reversing the sublist starting from the second node
2. After the recursion returns, the sublist is already reversed
3. We only need to fix the connection between the first node and the rest
4. The first node becomes the last node in the reversed list, so its next should be None

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Where `n` is the number of nodes in the linked list. We visit each node exactly once.

##### Space Complexity: `O(n)`

The recursion creates a stack of function calls proportional to the list length. In the worst case, the recursion depth equals the number of nodes.

#### Key Insights

- Elegant recursive solution that naturally expresses the reversal operation
- Each recursive call handles reversing one connection in the list
- More memory-intensive due to call stack overhead
- More concise but potentially less intuitive to understand

## Comparison of Solutions

### Time Complexity

- **Iterative**: `O(n)` - Single pass through the list
- **Recursive**: `O(n)` - Also processes each node once

### Space Complexity

- **Iterative**: `O(1)` - Uses fixed amount of extra space
- **Recursive**: `O(n)` - Uses call stack space proportional to list length

### Trade-offs

- The iterative solution is more space-efficient but requires tracking multiple pointers
- The recursive solution is more elegant but uses more memory due to the call stack

### When to Use Each

- **Iterative**: When memory efficiency is important or the list might be very long
- **Recursive**: When code readability is valued over memory efficiency and the list is reasonably sized
`

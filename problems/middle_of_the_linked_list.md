# [Middle of the Linked List](https://leetcode.com/problems/middle-of-the-linked-list/)

Easy - 10 minutes - Linked List, Two Pointers

Given the `head` of a singly linked list, return the middle node of the linked list.

If there are two middle nodes, return the second middle node.

## Examples

### Example 1

![Middle of the Linked List Example 1](assets/middle_of_the_linked_list_example1.jpg)

**Input:** `head = [1,2,3,4,5]`

**Output:** `[3,4,5]`

**Explanation:** The middle node of the list is node 3.

### Example 2

![Middle of the Linked List Example 2](assets/middle_of_the_linked_list_example2.jpg)

**Input:** `head = [1,2,3,4,5,6]`

**Output:** `[4,5,6]`

**Explanation:** Since the list has two middle nodes with values 3 and 4, we return the second one.

## Constraints

- The number of nodes in the list is in the range `[1, 100]`.
- `1 <= Node.val <= 100`

## Solutions

### Solution 1: Fast and Slow Pointers (Two-Pointer Technique)

```python
def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
    if head == None:
        return None

    fast = slow = head
    while(fast and fast.next):
        fast = fast.next.next
        slow = slow.next
    return slow
```

#### Approach

This solution uses the fast and slow pointer technique (also known as the "tortoise and hare" algorithm). Two pointers start from the head of the list:

- The slow pointer moves one node at a time
- The fast pointer moves two nodes at a time

By the time the fast pointer reaches the end of the list, the slow pointer will be positioned at the middle node.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

We traverse the linked list once, where `n` is the number of nodes.

##### Space Complexity: `O(1)`

Only two pointers are used regardless of the input size.

#### Key Insights

- Efficient single-pass algorithm
- Handles both even and odd-length lists correctly
- Automatically returns the second middle node when there are two middle nodes

### Solution 2: Count and Find

```python
def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
    # Count the number of nodes
    count = 0
    current = head
    while current:
        count += 1
        current = current.next
    
    # Find the middle node
    middle = count // 2
    current = head
    for i in range(middle):
        current = current.next
    
    return current
```

#### Approach

This solution works in two passes:

1. First pass: Count the total number of nodes in the linked list
2. Second pass: Traverse the list again until reaching the middle node

For even-length lists, integer division ensures we get the second middle node.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

We traverse the linked list twice, resulting in `O(n)` time complexity.

##### Space Complexity: `O(1)`

Only a constant amount of extra space is used regardless of input size.

#### Key Insights

- Intuitive approach that's easy to understand
- Works correctly for both odd and even length lists
- Requires two passes through the linked list

## Comparison of Solutions

### Time Complexity

- **Fast and Slow Pointers**: `O(n)` - Single pass through the list
- **Count and Find**: `O(n)` - Two passes through the list

### Space Complexity

- **Fast and Slow Pointers**: `O(1)` - Uses only two pointers
- **Count and Find**: `O(1)` - Uses only counters and pointers

### Trade-offs

- Both solutions have the same asymptotic complexity, but the Fast and Slow Pointers solution is more efficient in practice as it only requires one pass through the list
- The Count and Find solution might be more intuitive for those unfamiliar with the two-pointer technique

### When to Use Each

- **Fast and Slow Pointers**: Preferred in most cases due to its single-pass efficiency
- **Count and Find**: May be easier to understand for beginners, but less efficient

### Optimization Notes

- The Fast and Slow Pointers approach is a classic technique for linked list problems
- This technique can be used for various other linked list problems, such as detecting cycles
- The solution demonstrates how two pointers moving at different speeds can be used to find positional relationships in a linked list

```

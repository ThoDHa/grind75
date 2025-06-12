# [Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/)

Easy - 20 minutes - Linked List

You are given the heads of two sorted linked lists `list1` and `list2`.

Merge the two lists in a one sorted list. The list should be made by splicing
together the nodes of the first two lists.

Return the head of the merged linked list.

## Examples

### Example 1

![merged](https://assets.leetcode.com/uploads/2020/10/03/merge_ex1.jpg)

**Input:** `list1 = [1,2,4]`, `list2 = [1,3,4]`

**Output:** `[1,1,2,3,4,4]`

### Example 2

**Input:** `list1 = []`, `list2 = []`

**Output:** `[]`

### Example 3

**Input:** `list1 = []`, `list2 = [0]`

**Output:** `[0]`

## Constraints

- The number of nodes in both lists is in the range `[0, 50]`.
- `-100 <= Node.val <= 100`
- Both `list1` and `list2` are sorted in non-decreasing order.

## Solution

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode],
                      list2: Optional[ListNode]) -> Optional[ListNode]:
        # Create a dummy node to serve as the head of our result list
        dummy = ListNode(-1)
        current = dummy
        
        # Iterate while both lists have nodes
        while list1 and list2:
            # Compare values and link the smaller node to our result
            if list1.val <= list2.val:
                current.next = list1
                list1 = list1.next
            else:
                current.next = list2
                list2 = list2.next
            # Move the current pointer forward
            current = current.next
        
        # Attach remaining nodes (if any)
        current.next = list1 if list1 else list2
        
        # Return the merged list (skip the dummy node)
        return dummy.next
```

## Solution Approach

This solution uses a dummy head node technique with an iterative approach to merge the two sorted lists. We maintain a "current" pointer that builds the merged list as we traverse both input lists simultaneously. At each step, we compare the values at the heads of both lists and connect the smaller node to our result list, then advance the appropriate list pointer. Once one list is exhausted, we simply attach the remainder of the other list, as it's already sorted.

## Time and Space Complexity Analysis

### Time Complexity: `O(n + m)`

Where `n` and `m` are the lengths of `list1` and `list2` respectively. We traverse each node in both lists exactly once.

### Space Complexity: `O(1)`

We only use a constant amount of extra space for pointers. The solution reuses the existing nodes without allocating additional memory for the merged list structure.

## Key Insights

- Using a dummy head node simplifies handling edge cases and avoids special treatment for the first node insertion
- The solution leverages the fact that both input lists are already sorted
- Attaching remaining nodes at once is more efficient than continuing comparisons after one list is exhausted
- In-place merging saves memory by reusing existing nodes instead of creating new ones

# [Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/)

**Easy** | **20 minutes** | **Linked List**

**Pattern:** [K-Way Merge](../patterns/k_way_merge/intuition.md)

**Practice:** [`practice/merge_two_sorted_lists/solution.py`](../../practice/merge_two_sorted_lists/solution.py)

You are given the heads of two sorted linked lists `list1` and `list2`.

Merge the two lists in a one sorted list. The list should be made by splicing
together the nodes of the first two lists.

Return the head of the merged linked list.

## Examples

### Example 1

![merged](assets/merge_two_sorted_list_ex1.jpg)

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

## Solutions

### Iterative

```python
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

#### Approach

This solution uses a dummy head node technique with an iterative approach to merge the two sorted lists. We maintain a "current" pointer that builds the merged list as we traverse both input lists simultaneously. At each step, we compare the values at the heads of both lists and connect the smaller node to our result list, then advance the appropriate list pointer. Once one list is exhausted, we simply attach the remainder of the other list, as it's already sorted.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n + m)`

Where `n` and `m` are the lengths of `list1` and `list2` respectively. We traverse each node in both lists exactly once.

##### Space Complexity: `O(1)`

We only use a constant amount of extra space for pointers. The solution reuses the existing nodes without allocating additional memory for the merged list structure.

#### Key Insights

- Using a dummy head node simplifies handling edge cases and avoids special treatment for the first node insertion
- The solution leverages the fact that both input lists are already sorted
- Attaching remaining nodes at once is more efficient than continuing comparisons after one list is exhausted
- In-place merging saves memory by reusing existing nodes instead of creating new ones

### Recursive

```python
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode],
                      list2: Optional[ListNode]) -> Optional[ListNode]:
        # Base cases: if one list is empty, the merged result is the other list
        if list1 is None:
            return list2
        if list2 is None:
            return list1

        # Pick the smaller head, then merge the rest behind it
        if list1.val <= list2.val:
            list1.next = self.mergeTwoLists(list1.next, list2)
            return list1
        else:
            list2.next = self.mergeTwoLists(list1, list2.next)
            return list2
```

#### Approach

This solution expresses the merge as a recurrence. The smaller of the two heads
is the head of the merged list, and its `next` is the merge of the remainder of
that list with the entire other list. The recursion bottoms out when either
list becomes empty, at which point the other list is already sorted and can be
returned as-is.

1. If `list1` is empty, the merge is simply `list2`, and vice versa
2. Otherwise compare the heads, splice the smaller node onto the front of the
   recursively merged tail, and return that node as the new head

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n + m)`

Each recursive call consumes exactly one node from one of the lists, so the
total number of calls equals the combined length of both lists.

##### Space Complexity: `O(n + m)`

The recursion stack grows one frame per node consumed, reaching depth `n + m`
in the worst case before any frame returns. Unlike the iterative version, this
does not achieve constant space.

#### Key Insights

- The recursive formulation reads almost like the problem statement: the merged
  list is the smaller head followed by the merge of what remains
- No dummy node is needed because each call returns the correct head directly
- The tradeoff for this clarity is `O(n + m)` stack space, which can overflow
  for very long lists in languages without tail-call optimization

## Comparison of Solutions

### Time Complexity

- **Iterative**: `O(n + m)` - Each node from both lists is visited exactly once
- **Recursive**: `O(n + m)` - One recursive call consumes one node, totaling `n + m` calls

### Space Complexity

- **Iterative**: `O(1)` - Only a handful of pointers regardless of list length
- **Recursive**: `O(n + m)` - Recursion stack reaches depth equal to the combined length

### Trade-offs

- **Iterative** uses constant space and avoids any risk of stack overflow, at the cost of slightly more bookkeeping with the dummy node and current pointer
- **Recursive** is more concise and maps directly onto the recurrence, but its stack usage scales linearly and can overflow on very long lists

### When to Use Each

- **Iterative**: The default choice for interviews and production, especially when lists may be long or constant space is required
- **Recursive**: When clarity matters most and inputs are known to be small, or to demonstrate the recursive structure of the problem

### Optimization Notes

- The iterative solution is recommended for its `O(1)` space and freedom from recursion-depth limits; both approaches share the same `O(n + m)` time
- Both solutions splice existing nodes rather than allocating new ones, so no extra heap memory is used for the merged structure itself
- The `<=` comparison (rather than `<`) preserves the relative order of equal-valued nodes, keeping the merge stable

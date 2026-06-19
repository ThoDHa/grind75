# [Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/)

**Easy** | **20 minutes** | **Linked List**

**Pattern:** [K-Way Merge](../patterns/k_way_merge/intuition.md)

**Practice:** [`practice/merge_two_sorted_lists/solution.py`](https://github.com/ThoDHa/grind75/blob/main/practice/merge_two_sorted_lists/solution.py)

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

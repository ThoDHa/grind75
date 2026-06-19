# [Kth Smallest Element in a BST](https://leetcode.com/problems/kth-smallest-element-in-a-bst/)

**Medium** | **25 minutes** | **Tree, Depth-First Search, Binary Search Tree**

**Pattern:** [Tree Traversal](../patterns/tree/intuition.md)

**Practice:** [`practice/kth_smallest_element_in_a_bst/solution.py`](../../practice/kth_smallest_element_in_a_bst/solution.py)

Given the `root` of a binary search tree, and an integer `k`, return the `kth` smallest value (1-indexed) of all the values of the nodes in the tree.

## Examples

### Example 1

![BST Tree 1](assets/kth_smallest_element_in_a_bst_example1.jpg)

**Input:** `root = [3,1,4,null,2]`, `k = 1`

**Output:** `1`

### Example 2

![BST Tree 2](assets/kth_smallest_element_in_a_bst_example2.jpg)

**Input:** `root = [5,3,6,2,4,null,null,1]`, `k = 3`

**Output:** `3`

## Constraints

- The number of nodes in the tree is `n`.
- `1 <= k <= n <= 10^4`
- `0 <= Node.val <= 10^4`

## Follow-up

If the BST is modified often (i.e., we can do insert and delete operations) and you need to find the kth smallest frequently, how would you optimize?

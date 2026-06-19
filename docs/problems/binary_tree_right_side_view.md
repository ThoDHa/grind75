# [Binary Tree Right Side View](https://leetcode.com/problems/binary-tree-right-side-view/)

**Medium** | **20 minutes** | **Tree**

**Pattern:** [Tree Traversal](../patterns/tree/intuition.md)

**Practice:** [`practice/binary_tree_right_side_view/solution.py`](https://github.com/ThoDHa/grind75/blob/main/practice/binary_tree_right_side_view/solution.py)

Given the `root` of a binary tree, imagine yourself standing on the **right side** of it, return the values of the nodes you can see ordered from top to bottom.

## Examples

### Example 1

![Binary Tree Right Side View Example1](assets/binary_tree_right_side_view_example1.jpg)

**Input:** `root = [1,2,3,null,5,null,4]`

**Output:** `[1,3,4]`

### Example 2

**Input:** `root = [1,null,3]`

**Output:** `[1,3]`

### Example 3

**Input:** `root = []`

**Output:** `[]`

## Constraints

- The number of nodes in the tree is in the range `[0, 100]`.
- `-100 <= Node.val <= 100`

# [Binary Tree Maximum Path Sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/)

**Hard** | **35 minutes** | **Tree**

**Pattern:** [Tree DP](../patterns/tree_dp/intuition.md)

A **path** in a binary tree is a sequence of nodes where each pair of adjacent nodes in the sequence has an edge connecting them. A node can only appear in the sequence **at most once**. Note that the path does not need to pass through the root.

The **path sum** of a path is the sum of the node's values in the path.

Given the `root` of a binary tree, return the **maximum path sum** of any **non-empty** path.

## Examples

### Example 1

![Binary Tree Maximum Path Sum Example1](assets/binary_tree_maximum_path_sum_example1.jpg)

**Input:** `root = [1,2,3]`

**Output:** `6`

**Explanation:** The optimal path is `2 -> 1 -> 3` with a path sum of `2 + 1 + 3 = 6`.

### Example 2

![Binary Tree Maximum Path Sum Example2](assets/binary_tree_maximum_path_sum_example2.jpg)

**Input:** `root = [-10,9,20,null,null,15,7]`

**Output:** `42`

**Explanation:** The optimal path is `15 -> 20 -> 7` with a path sum of `15 + 20 + 7 = 42`.

## Constraints

- The number of nodes in the tree is in the range `[1, 3 * 10^4]`.
- `-1000 <= Node.val <= 1000`

## Solutions

### Post-Order DFS

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        self.max_sum = float("-inf")

        def max_gain(node: Optional[TreeNode]) -> int:
            if not node:
                return 0

            # Best downward path from each child, clamped at 0 so a
            # negative branch is simply dropped rather than dragging us down
            left_gain = max(max_gain(node.left), 0)
            right_gain = max(max_gain(node.right), 0)

            # A path that bends through this node uses both children
            self.max_sum = max(self.max_sum, node.val + left_gain + right_gain)

            # But a path returned to the parent can only descend one side
            return node.val + max(left_gain, right_gain)

        max_gain(root)
        return self.max_sum
```

#### Approach

A maximum path can take two shapes at any node: it can **bend** through the node,
descending into both the left and right subtrees, or it can **pass straight
through**, continuing up to the node's parent on only one side. We handle this by
having the recursion return the best straight (single-side) path while a global
maximum captures the best bent path seen anywhere.

1. Define `max_gain(node)` to return the largest sum of a downward path that
   starts at `node` and goes through at most one child. An empty node
   contributes `0`.
2. Recurse into both children, clamping each gain with `max(..., 0)`. If a
   subtree's best contribution is negative, we drop it: a single positive node
   beats a node plus a negative branch.
3. The best path that *peaks* at this node is `node.val + left_gain +
   right_gain`. Compare it against the running global `max_sum`.
4. Return `node.val + max(left_gain, right_gain)` to the parent, because a path
   the parent extends can only pass through one of this node's sides.

Tracking the bent sum separately from the returned straight sum is what lets a
single post-order traversal consider every possible path.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each node is visited once, performing constant work (two comparisons and two
additions) per visit.

##### Space Complexity: `O(h)`

The recursion stack grows with the tree height `h`: `O(log n)` for a balanced
tree and `O(n)` for a skewed one.

#### Key Insights

- The path returned upward and the path measured for the answer differ: only the
  measured one may use both children, since a node can appear at most once.
- Clamping negative gains to `0` cleanly expresses "skip this branch" without
  special-casing.
- Initializing `max_sum` to negative infinity is required because every value
  can be negative and the path must be non-empty.
- One post-order traversal suffices: children must be evaluated before the
  parent can decide its best bent and straight sums.

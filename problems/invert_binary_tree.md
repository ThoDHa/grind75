# [Invert Binary Tree](https://leetcode.com/problems/invert-binary-tree/)

Easy - 15 minutes - Tree, Depth-First Search, Breadth-First Search

Given the `root` of a binary tree, invert the tree, and return its root.

## Examples

### Example 1

![Invert Binary Tree Example 1](assets/invert_binary_tree_example1.jpg)

**Input:** `root = [4,2,7,1,3,6,9]`

**Output:** `[4,7,2,9,6,3,1]`

### Example 2

![Invert Binary Tree Example 2](assets/invert_binary_tree_example2.jpg)

**Input:** `root = [2,1,3]`

**Output:** `[2,3,1]`

### Example 3

**Input:** `root = []`

**Output:** `[]`

## Constraints

- The number of nodes in the tree is in the range `[0, 100]`
- `-100 <= Node.val <= 100`

## Solution

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if not root:
            return
        self.invertTree(root.left)
        self.invertTree(root.right)

        temp: TreeNode
        temp = root.right
        root.right = root.left
        root.left = temp
        return root
```

### Approach

This problem is solved using recursion with a post-order traversal approach:

- Base case: If the root is None (empty tree), we simply return None.
- Recursive step: We first invert the left subtree and right subtree recursively.
- After both subtrees have been inverted, we swap the left and right children of the current node.
- Finally, we return the modified root.

This post-order traversal (left, right, then node) ensures that we work from the leaves up to the root.

### Time and Space Complexity Analysis

#### Time Complexity: `O(n)`

- We visit each node in the tree exactly once, where n is the number of nodes.
- At each node, we perform constant-time operations (swapping references).

#### Space Complexity: `O(h)`, where h is the height of the tree

- The space complexity is determined by the maximum depth of the recursion stack.
- In the worst case (skewed tree), this could be `O(n)`.
- In a balanced tree, the height is `O(log n)`.

## Key Insights

- This problem demonstrates the elegance of recursion for tree problems.
- Post-order traversal is appropriate here because we want to invert subtrees before swapping them.
- The solution works by applying the same inversion operation at each level of the tree.
- The operation is symmetric: inverting an already inverted tree gives the original tree.
- This is a classic example of a divide-and-conquer approach where we:
  1. Break the problem into subproblems (left and right subtrees)
  2. Solve the subproblems recursively
      3. Combine the results (swap the inverted subtrees)

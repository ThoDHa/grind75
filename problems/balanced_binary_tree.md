# [Balanced Binary Tree](https://leetcode.com/problems/balanced-binary-tree/)

Easy - 20 minutes - Tree, DFS, Binary Tree

Given a binary tree, determine if it is height-balanced.

A height-balanced binary tree is defined as a binary tree in which the left and right subtrees of every node differ in height by no more than `1`.

## Examples

### Example 1

![Balanced Binary Tree Example 1](assets/balanced_binary_tree_example1.jpg)

**Input:** `root = [3,9,20,null,null,15,7]`

**Output:** `true`

### Example 2

![Balanced Binary Tree Example 2](assets/balanced_binary_tree_example2.jpg)

**Input:** root = `[1,2,2,3,3,null,null,4,4]`

**Output:** `false`

### Example 3

**Input:** `root = []`

**Output:** `true`

## Constraints

- The number of nodes in the tree is in the range `[0, 5000]`.
- `-10^4 <= Node.val <= 10^4`

## Solutions

### Solution 1: Bottom-up Recursive Approach

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        if not root:
            return True
        return self.balanced_height(root) != -1

    def balanced_height(self, root) -> int:
        if not root:
            return 0
        left_height = self.balanced_height(root.left)
        right_height = self.balanced_height(root.right)

        if left_height == -1 or right_height == -1 or abs(left_height-right_height) > 1:
            return -1
        return max(left_height, right_height) + 1
```

#### Approach

This solution uses a bottom-up recursive approach with a helper function `balanced_height` that:

1. Returns the height of a subtree if it's balanced
2. Returns -1 if any part of the subtree is unbalanced

The algorithm works through post-order traversal:

- First check if left subtree is balanced (recursively)
- Then check if right subtree is balanced (recursively)
- Finally, check if current node is balanced (height difference ≤ 1)
- If any condition fails, propagate -1 upward

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

- Each node in the tree is visited exactly once
- At each node, we perform constant-time operations (comparison and calculating max)
- The height and balance check are combined, avoiding redundant calculations

##### Space Complexity: `O(h)`

- Where `h` is the height of the tree
- The recursive call stack can go as deep as the height of the tree
- Best case (balanced tree): `O(log n)`
- Worst case (skewed tree): `O(n)`

#### Key Insights

- Using -1 as a special signal value allows us to efficiently propagate "unbalanced" status up the tree
- This solution performs a post-order traversal, processing children before parents
- Combining height calculation with balance checking avoids redundant work
- Early termination occurs as soon as any unbalanced subtree is found

### Solution 2: Top-down Recursive Approach

```python
class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        if not root:
            return True
            
        # Check if current node's subtrees have height difference <= 1
        if abs(self.height(root.left) - self.height(root.right)) > 1:
            return False
            
        # Recursively check if left and right subtrees are balanced
        return self.isBalanced(root.left) and self.isBalanced(root.right)
    
    def height(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        return max(self.height(root.left), self.height(root.right)) + 1
```

#### Approach

This solution uses a top-down approach:

1. For each node, calculate the height of its left and right subtrees
2. Check if the difference in heights is at most 1
3. Recursively check if both left and right subtrees are balanced

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n²)`

- In the worst case, for each node, we calculate the heights of all nodes in its subtree
- For a skewed tree with n nodes, this leads to quadratic time complexity
- For a balanced tree, closer to `O(n log n)`

##### Space Complexity: `O(h)`

- Where `h` is the height of the tree
- The recursive call stack can go as deep as the height of the tree
- Same as Solution 1

#### Key Insights

- More intuitive implementation that directly follows the problem definition
- Separates height calculation from balance checking
- Less efficient due to redundant height calculations for the same nodes
- More readable for developers new to tree algorithms

## Comparison of Solutions

### Time Complexity

- **Solution 1 (Bottom-up)**: `O(n)` - Linear time, highly efficient
- **Solution 2 (Top-down)**: `O(n²)` - Quadratic time in worst case, inefficient for large trees

### Space Complexity

- **Both solutions**: `O(h)` - Proportional to tree height

### Trade-offs

- **Solution 1**: More efficient but slightly less intuitive implementation
- **Solution 2**: More intuitive but much less efficient for large trees

### When to Use Each

- **Solution 1**: Production code, large trees, performance-critical applications
- **Solution 2**: Educational purposes, small trees, when code clarity is more important than performance

### Optimization Notes

- The bottom-up approach avoids recalculating heights of the same subtrees
- The use of a signal value (-1) is an elegant way to propagate failure conditions
- Early termination in Solution 1 provides significant performance advantages for unbalanced trees

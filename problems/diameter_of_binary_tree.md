# [Diameter of Binary Tree](https://leetcode.com/problems/diameter-of-binary-tree/)

Easy - 20 minutes - Tree, Depth-First Search, Binary Tree

Given the `root` of a binary tree, return the length of the **diameter** of the tree.

The **diameter** of a binary tree is the **length** of the longest path between any two nodes in a tree. This path may or may not pass through the root.

The **length** of a path between two nodes is represented by the number of edges between them.

## Examples

### Example 1

![Diameter of Binary Tree Example](assets/diameter_of_binary_tree_example1.jpg)

**Input:** `root = [1,2,3,4,5]`

**Output:** `3`

**Explanation:** The length of the diameter from node 4 to node 3 is 3.

### Example 2

**Input:** `root = [1,2]`

**Output:** `1`

## Constraints

- The number of nodes in the tree is in the range `[1, 10^4]`.
- `-100 <= Node.val <= 100`

## Solutions

### Solution 1: Recursive DFS with Global Variable

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        if root == None:
            return 0
        self.max_diameter = 0
        self.depth(root)

        return self.max_diameter
        
    def depth(self, root: Optional[TreeNode]) -> int:
        if (root == None):
            return 0
        left = self.depth(root.left)
        right = self.depth(root.right)
        current_diameter = left + right
        self.max_diameter = max(current_diameter, self.max_diameter)
        return max(left, right)+1
```

#### Approach

This solution employs a depth-first search (DFS) using recursion to find the diameter. The key insight is that the diameter at any node is the sum of the heights of its left and right subtrees. We use a helper method `depth()` to calculate the height of each node while simultaneously updating a global variable that tracks the maximum diameter found so far.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

We visit each node in the tree exactly once, performing constant time operations at each node, resulting in a linear time complexity.

##### Space Complexity: `O(h)`

Where `h` is the height of the tree. This space is used by the recursive call stack. In the worst case (skewed tree), this could be `O(n)`, but for a balanced tree, it would be `O(log n)`.

#### Key Insights

- The diameter of a tree doesn't necessarily pass through the root
- At each node, the potential diameter is the sum of the heights of left and right subtrees
- Using a global variable allows us to track the maximum diameter as we traverse the tree
- The height of a node is 1 + the maximum height of its children

### Solution 2: Return Pair Approach

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        def dfs(node):
            if not node:
                return 0, 0  # height, diameter
            
            left_height, left_diameter = dfs(node.left)
            right_height, right_diameter = dfs(node.right)
            
            height = max(left_height, right_height) + 1
            diameter = max(left_height + right_height, left_diameter, right_diameter)
            
            return height, diameter
        
        return dfs(root)[1]
```

#### Approach

This solution also uses DFS but avoids using a global variable by returning two values from each recursive call: the height of the subtree and the maximum diameter found in that subtree. At each node, we calculate both values based on the left and right subtree results.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

We still visit each node exactly once, with constant time operations per node.

##### Space Complexity: `O(h)`

Where `h` is the height of the tree, used by the recursive call stack.

#### Key Insights

- This approach makes the function more self-contained by avoiding global variables
- The tuple return pattern is useful for when we need to pass multiple pieces of information up the recursion tree
- This solution is functionally equivalent to the first but with a different coding style

## Comparison of Solutions

### Time Complexity

- **Global Variable Approach**: `O(n)` - We visit each node once
- **Return Pair Approach**: `O(n)` - Also visits each node once

### Space Complexity

- **Global Variable Approach**: `O(h)` - Where h is the height of the tree
- **Return Pair Approach**: `O(h)` - Same space complexity

### Trade-offs

- The global variable approach is slightly more concise but introduces a class-level state
- The return pair approach avoids global state but requires returning multiple values

### When to Use Each

- **Global Variable Approach**: When code simplicity is preferred and state management isn't a concern
- **Return Pair Approach**: When avoiding global state is important or when the function needs to be more self-contained

### Optimization Notes

1. Computing the tree height/depth using DFS is central to both solutions
2. The key realization is that we can compute both height and diameter in a single traversal
3. In both approaches, we're essentially finding the longest path that doesn't necessarily go through the root

Both solutions are efficient with identical time and space complexity characteristics. The choice between them is primarily a matter of coding style and preference.

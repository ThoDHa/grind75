# [Lowest Common Ancestor of a Binary Search Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/)

Easy - 20 minutes - Binary Search Tree, Tree, Recursion

Given a binary search tree (BST), find the lowest common ancestor (LCA) node of two given nodes in the BST.

According to the definition of LCA on Wikipedia: "The lowest common ancestor is defined between two nodes `p` and `q` as the lowest node in `T` that has both `p` and `q` as descendants (where we allow a node to be a descendant of itself)."

## Examples

### Example 1

![Lowest Common Ancestor Tree Example](assets/lowest_comment_ancestor_binary_search_tree_example1.png)

**Input:** `root = [6,2,8,0,4,7,9,null,null,3,5]`, `p = 2`, `q = 8`

**Output:** `6`

**Explanation:** The LCA of nodes `2` and `8` is `6`.

### Example 2

![Lowest Common Ancestor Tree Example](assets/lowest_comment_ancestor_binary_search_tree_example1.png)

**Input:** `root = [6,2,8,0,4,7,9,null,null,3,5]`, `p = 2`, `q = 4`

**Output:** `2`

**Explanation:** The LCA of nodes `2` and `4` is `2`, since a node can be a descendant of itself according to the LCA definition.

### Example 3

**Input:** `root = [2,1]`, `p = 2`, `q = 1`

**Output:** `2`

## Constraints

- The number of nodes in the tree is in the range `[2, 10^5]`.
- `-10^9 <= Node.val <= 10^9`
- All `Node.val` are unique.
- `p != q`
- `p` and `q` will exist in the BST.

## Solutions

### Solution 1: Recursive Using BST Properties

```python
def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
    # If both p and q are smaller than root, LCA is in the left subtree
    if p.val < root.val and q.val < root.val:
        return self.lowestCommonAncestor(root.left, p, q)
    # If both p and q are greater than root, LCA is in the right subtree
    elif p.val > root.val and q.val > root.val:
        return self.lowestCommonAncestor(root.right, p, q)
    # If p and q are on different sides of root (or one of them is root), root is the LCA
    else:
        return root
```

#### Approach

This solution leverages the Binary Search Tree property: values smaller than a node are in its left subtree, and values greater are in its right subtree. We navigate down the tree, choosing the left or right path when both nodes are on the same side. When the nodes diverge (or we hit one of them), we've found the LCA.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(h)`

Where `h` is the height of the tree. In the worst case, we might need to traverse from the root to a leaf, which is the height of the tree. For a balanced BST, this would be `O(log n)`.

##### Space Complexity: `O(h)`

Due to the recursion stack, which can go as deep as the height of the tree.

#### Key Insights

- Utilizes the BST property to efficiently navigate the tree
- Each step eliminates roughly half of the remaining tree
- No need to traverse the entire tree, only the path from root to the divergence point

### Solution 2: Iterative Using BST Properties

```python
def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
    current = root
    
    while current:
        # If both p and q are smaller than current, go left
        if p.val < current.val and q.val < current.val:
            current = current.left
        # If both p and q are greater than current, go right
        elif p.val > current.val and q.val > current.val:
            current = current.right
        # We found the split point, this is the LCA
        else:
            return current
```

#### Approach

This solution uses the same logic as the recursive approach but implements it iteratively. We start at the root and traverse down the tree, moving left when both target nodes are smaller than the current node, and right when both are larger. The first node where the targets diverge (or where we encounter one of the targets) is the LCA.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(h)`

Same as the recursive approach, where `h` is the height of the tree.

##### Space Complexity: `O(1)`

This solution uses only a constant amount of extra space regardless of input size, as we're not using recursion or any data structures that scale with input.

#### Key Insights

- Eliminates recursion overhead and stack space
- Same logical approach as the recursive solution
- More efficient memory usage for very deep trees

### Solution 3: Generic Binary Tree Approach

```python
def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
    if not root:
        return None
    if root.val == p.val or root.val == q.val:
        return root
    
    left = self.lowestCommonAncestor(root.left, p, q)
    right = self.lowestCommonAncestor(root.right, p, q)
    
    if left and right:
        return root
    if left:
        return left
    else:
        return right
```

#### Approach

This is a general solution that works for any binary tree, not just BSTs. It recursively searches for the target nodes in both subtrees. If both subtrees contain one target each, the current node is the LCA. If only one subtree contains a target, that subtree must contain the LCA.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Where `n` is the number of nodes in the tree. In the worst case, we might need to visit all nodes.

##### Space Complexity: `O(h)`

Due to the recursion stack, which can go as deep as the height of the tree.

#### Key Insights

- Works for any binary tree, not just BSTs
- Less efficient than BST-specific approaches for this problem
- Post-order traversal approach (visits children before making decisions)

## Comparison of Solutions

### Time Complexity

- **BST Recursive**: `O(h)` - Leverages BST property to navigate directly to solution
- **BST Iterative**: `O(h)` - Same approach as recursive but without stack overhead
- **Generic Binary Tree**: `O(n)` - Must potentially visit all nodes

### Space Complexity

- **BST Recursive**: `O(h)` - Uses recursion stack proportional to tree height
- **BST Iterative**: `O(1)` - Uses only constant extra space
- **Generic Binary Tree**: `O(h)` - Uses recursion stack proportional to tree height

### Trade-offs

- The BST solutions are significantly more efficient for this specific problem but require the binary search tree property
- The generic solution is more versatile but less efficient for BSTs
- The iterative solution provides the best space efficiency but might be slightly less readable

### When to Use Each

- **BST Recursive**: When dealing with a BST and code readability is prioritized
- **BST Iterative**: When dealing with a BST and memory efficiency is important, or for very deep trees
- **Generic Binary Tree**: When the tree doesn't have the BST property, or when writing a general utility function

### Optimization Notes

- The BST property allows us to eliminate about half the tree at each step
- The iterative solution avoids recursion overhead and is generally preferred for production environments
- For very unbalanced trees (approaching a linked list), the BST approach could degrade to `O(n)` time complexity
`

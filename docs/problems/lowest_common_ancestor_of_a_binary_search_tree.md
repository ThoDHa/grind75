# [Lowest Common Ancestor of a Binary Search Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/)

**Easy** | **20 minutes** | **Binary Search Tree, Tree, Recursion**

**Pattern:** [Tree Traversal](../patterns/tree/intuition.md)

**Practice:** [`practice/lowest_common_ancestor_of_a_binary_search_tree/solution.py`](https://github.com/ThoDHa/grind75/blob/main/practice/lowest_common_ancestor_of_a_binary_search_tree/solution.py)

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

### Recursive Using BST Properties

```python
class Solution:
    def lowestCommonAncestor(
        self, root: TreeNode, p: TreeNode, q: TreeNode
    ) -> TreeNode:
        # Both targets smaller than root: the LCA lives in the left subtree.
        if p.val < root.val and q.val < root.val:
            return self.lowestCommonAncestor(root.left, p, q)
        # Both targets larger than root: the LCA lives in the right subtree.
        if p.val > root.val and q.val > root.val:
            return self.lowestCommonAncestor(root.right, p, q)
        # Targets straddle root, or one equals root: root is the LCA.
        return root
```

#### Approach

This solution leverages the Binary Search Tree property: values smaller than a node sit in its left subtree, and values greater sit in its right subtree. We navigate down the tree, recursing into one side only when both targets fall on that side. The first node where the targets diverge (one on each side, or one equal to the node itself) is the lowest common ancestor.

1. Compare both `p.val` and `q.val` against `root.val`.
2. If both are smaller, recurse into `root.left`.
3. If both are larger, recurse into `root.right`.
4. Otherwise the targets split here, so `root` is the LCA. Return it.

Because the problem guarantees both nodes exist in the BST, the recursion always reaches a valid split point and never falls off the tree.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(h)`

Where `h` is the height of the tree. Each call descends one level, so we make at most `h` calls before reaching the split point. For a balanced BST this is `O(log n)`; for a skewed tree it degrades to `O(n)`.

##### Space Complexity: `O(h)`

The recursion stack can grow as deep as the height of the tree.

#### Key Insights

- The BST ordering invariant lets us pick a direction without exploring both subtrees.
- Each step eliminates roughly half of the remaining tree in the balanced case.
- We only walk the path from the root to the divergence point, never the whole tree.

### Iterative Using BST Properties

```python
class Solution:
    def lowestCommonAncestor(
        self, root: TreeNode, p: TreeNode, q: TreeNode
    ) -> TreeNode:
        current = root
        while current:
            # Both targets smaller than current: go left.
            if p.val < current.val and q.val < current.val:
                current = current.left
            # Both targets larger than current: go right.
            elif p.val > current.val and q.val > current.val:
                current = current.right
            # Split point reached: current is the LCA.
            else:
                return current
        return None
```

#### Approach

This solution uses the same BST logic as the recursive approach but replaces the call stack with a single loop. We start at the root and descend, moving left when both targets are smaller than the current node and right when both are larger. The first node where the targets diverge (or where one of them equals the current node) is the LCA.

1. Set `current` to `root`.
2. While `current` is not `None`, compare both target values against `current.val`.
3. Move `current` left or right while both targets fall on the same side.
4. Return `current` as soon as the targets split.

The loop is guaranteed to terminate at a real node because both targets exist in the tree, so a split point always appears before we run off the end.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(h)`

Same as the recursive approach: at most one iteration per level of the tree, where `h` is the height.

##### Space Complexity: `O(1)`

Only a single pointer is tracked, independent of input size, since there is no recursion or auxiliary structure.

#### Key Insights

- Eliminates recursion overhead and the stack space it consumes.
- Identical decision logic to the recursive version, just driven by a loop.
- Preferred for very deep or skewed trees, where the recursive stack could grow large.

### Generic Binary Tree Approach

```python
class Solution:
    def lowestCommonAncestor(
        self, root: TreeNode, p: TreeNode, q: TreeNode
    ) -> TreeNode:
        if root is None:
            return None
        # Finding either target here makes root a candidate ancestor.
        if root.val == p.val or root.val == q.val:
            return root

        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)

        # Targets found on both sides: root is the split point.
        if left and right:
            return root
        # Otherwise the LCA is whichever side returned a node.
        return left or right
```

#### Approach

This is a general solution that ignores the BST ordering and works for any binary tree. It searches both subtrees for the targets using a post-order traversal. If each subtree reports back one target, the current node is the split point and therefore the LCA. If only one subtree reports a target, the LCA lies entirely within that subtree.

1. Return `None` for an empty subtree.
2. If the current node matches `p` or `q`, return it as a candidate.
3. Recurse into both children.
4. If both children return non-`None`, the targets diverge here, so return the current node.
5. Otherwise propagate whichever child found a target upward.

Because a matching node short-circuits its subtree, a node that is itself an ancestor of the other target is returned correctly without descending further.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Where `n` is the number of nodes. Without the BST ordering, the search may visit every node in the tree.

##### Space Complexity: `O(h)`

The recursion stack can grow as deep as the height of the tree.

#### Key Insights

- Works for any binary tree, not only BSTs, at the cost of efficiency.
- Post-order traversal: children are resolved before the current node decides.
- A node equal to one target short-circuits, naturally handling the ancestor-of-itself case.

## Comparison of Solutions

### Time Complexity

- **BST Recursive**: `O(h)`: leverages the BST property to navigate directly to the split point.
- **BST Iterative**: `O(h)`: the same path as the recursive version, without stack overhead.
- **Generic Binary Tree**: `O(n)`: may need to visit every node.

### Space Complexity

- **BST Recursive**: `O(h)`: recursion stack proportional to tree height.
- **BST Iterative**: `O(1)`: only a single pointer of extra state.
- **Generic Binary Tree**: `O(h)`: recursion stack proportional to tree height.

### Trade-offs

- The BST solutions are significantly more efficient for this specific problem but require the binary search tree property
- The iterative solution provides the best space efficiency but might be slightly less readable
- The generic solution is more versatile but less efficient for BSTs

### When to Use Each

- **BST Recursive**: When dealing with a BST and code readability is prioritized
- **BST Iterative**: When dealing with a BST and memory efficiency is important, or for very deep trees
- **Generic Binary Tree**: When the tree doesn't have the BST property, or when writing a general utility function

### Optimization Notes

- The BST property allows us to eliminate about half the tree at each step
- The iterative solution avoids recursion overhead and is generally preferred for production environments
- For very unbalanced trees (approaching a linked list), the BST approach could degrade to `O(n)` time complexity

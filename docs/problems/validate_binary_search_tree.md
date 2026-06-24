# [Validate Binary Search Tree](https://leetcode.com/problems/validate-binary-search-tree/)

**Medium** | **30 minutes** | **Tree, Depth-First Search, Binary Search Tree, Binary Tree**

**Pattern:** [Tree Traversal](../patterns/tree/intuition.md)

**Practice:** [`practice/validate_binary_search_tree/solution.py`](../../practice/validate_binary_search_tree/solution.py)

Given the `root` of a binary tree, determine if it is a valid binary search tree (BST).

A **valid BST** is defined as follows:

- The left subtree of a node contains only nodes with keys **less than** the node's key.
- The right subtree of a node contains only nodes with keys **greater than** the node's key.
- Both the left and right subtrees must also be binary search trees.

## Examples

### Example 1

![BST](assets/validate_binary_search_tree_example1.jpg)

**Input:** `root = [2,1,3]`

**Output:** `true`

### Example 2

![Invalid BST](assets/validate_binary_search_tree_example2.jpg)

**Input:** `root = [5,1,4,null,null,3,6]`

**Output:** `false`

**Explanation:** The root node's value is 5 but its right child's value is 4.

## Constraints

- The number of nodes in the tree is in the range `[1, 10^4]`.
- `-2^31 <= Node.val <= 2^31 - 1`

## Solutions

### Brute Force

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        def all_less(node: Optional[TreeNode], limit: int) -> bool:
            # Every value in this subtree must be strictly below limit
            if not node:
                return True
            return (node.val < limit and
                    all_less(node.left, limit) and
                    all_less(node.right, limit))

        def all_greater(node: Optional[TreeNode], limit: int) -> bool:
            # Every value in this subtree must be strictly above limit
            if not node:
                return True
            return (node.val > limit and
                    all_greater(node.left, limit) and
                    all_greater(node.right, limit))

        def valid(node: Optional[TreeNode]) -> bool:
            if not node:
                return True
            # Apply the BST definition literally at this node
            if not all_less(node.left, node.val):
                return False
            if not all_greater(node.right, node.val):
                return False
            return valid(node.left) and valid(node.right)

        return valid(root)
```

#### Approach

The BST definition reads almost like an algorithm: every value in a node's left subtree is strictly smaller, every value in its right subtree is strictly larger, and both subtrees are themselves BSTs. The most direct implementation simply enforces that definition word for word at every node, scanning the full subtrees each time.

1. For each node, scan its entire left subtree and confirm every value is strictly less than `node.val`.
2. Scan its entire right subtree and confirm every value is strictly greater than `node.val`.
3. Recurse into both children, applying the same full check at each.
4. An empty subtree is trivially valid.

This rescans descendants repeatedly, but it needs no insight beyond restating the definition, which makes it the natural first attempt.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

Each node triggers a full scan of its subtrees, and in a skewed tree those scans cover up to `O(n)` nodes per call across `O(n)` nodes, giving quadratic work in the worst case.

##### Space Complexity: `O(h)`

The recursion stack reaches the tree's height `h`: `O(log n)` for a balanced tree and `O(n)` for a skewed one. The subtree scans add no extra storage beyond their own stack frames.

#### Key Insights

- Translates the BST definition directly, so it is the easiest version to derive and trust.
- The strict `<` and `>` comparisons reject duplicate values, as the definition requires.
- It re-examines the same descendants once per ancestor, which is the redundancy the bounds and inorder approaches eliminate.

### Recursive Bounds

```python
class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        def validate(node: Optional[TreeNode], low: float, high: float) -> bool:
            if not node:
                return True
            # Every node must lie strictly within the open interval (low, high)
            if not (low < node.val < high):
                return False
            return (validate(node.left, low, node.val) and
                    validate(node.right, node.val, high))

        return validate(root, float("-inf"), float("inf"))
```

#### Approach

The naive check, comparing a node only against its immediate children, is wrong: a value can satisfy its parent yet still violate an ancestor higher up. The correct invariant is that every node must fall within a `(low, high)` range determined by all of its ancestors.

1. Start at the root with the widest possible bounds, `(-inf, +inf)`.
2. For each node, verify `low < node.val < high` using a strict comparison so duplicates are rejected.
3. Recurse left, tightening the upper bound to the current node's value: everything in the left subtree must be smaller.
4. Recurse right, tightening the lower bound to the current node's value: everything in the right subtree must be larger.
5. An empty subtree is trivially valid.

Passing the bounds downward propagates every ancestor's constraint to the deepest descendants, which is exactly what the BST definition demands.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each node is visited once with constant work per visit.

##### Space Complexity: `O(h)`

The recursion stack reaches the tree's height `h`: `O(log n)` for a balanced tree and `O(n)` for a skewed one.

#### Key Insights

- Comparing against ancestor-derived bounds, not just children, is the crux that defeats the common wrong answer.
- Using `float("-inf")` and `float("inf")` sidesteps the `-2^31` to `2^31 - 1` value range without special casing.
- Strict `<` comparisons enforce the "strictly less / strictly greater" rule, correctly rejecting duplicate values.
- Early return on the first violation prunes the rest of the traversal.

### Inorder Traversal

```python
class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        prev = None

        def inorder(node: Optional[TreeNode]) -> bool:
            nonlocal prev
            if not node:
                return True
            if not inorder(node.left):
                return False
            # Inorder of a valid BST is strictly increasing
            if prev is not None and node.val <= prev:
                return False
            prev = node.val
            return inorder(node.right)

        return inorder(root)
```

#### Approach

An inorder traversal of a binary search tree visits values in strictly increasing order. So validating a BST is equivalent to confirming the inorder sequence never decreases or repeats.

1. Traverse in inorder (left, node, right).
2. Track the previously visited value in `prev`.
3. At each node, fail if `node.val <= prev`, since a valid BST must strictly increase.
4. Update `prev` and continue into the right subtree.

This avoids threading bounds through the recursion; instead it leans on the structural property that inorder linearizes a BST into sorted order.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each node is visited once during the traversal.

##### Space Complexity: `O(h)`

The recursion stack is bounded by the tree height `h`, ranging from `O(log n)` to `O(n)`.

#### Key Insights

- Inorder traversal of a valid BST yields a strictly ascending sequence: a clean equivalence to exploit.
- Only the single previous value needs tracking, so no full array of values is required.
- The strict `<=` rejection again handles duplicates correctly.
- Comparing adjacent values means an early exit the moment monotonicity breaks.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n^2)` - each node rescans its full subtrees, quadratic on a skewed tree.
- **Recursive Bounds**: `O(n)` - each node checked once against propagated bounds.
- **Inorder Traversal**: `O(n)` - each node visited once in sorted-order traversal.

### Space Complexity

- **All three solutions**: `O(h)` - dominated by the recursion stack, `O(log n)` balanced to `O(n)` skewed.

### Trade-offs

- **Brute Force** is the most direct restatement of the BST definition but wastes time rescanning descendants once per ancestor.
- **Recursive Bounds** makes the BST invariant explicit by carrying bounds, which generalizes naturally to range-style problems.
- **Inorder Traversal** is conceptually elegant, relying on the sorted-order property, and stores only one prior value.

### When to Use Each

- **Brute Force**: As a teaching baseline or first attempt when correctness matters more than speed.
- **Recursive Bounds**: When you want the validity constraint stated directly, or need to adapt it to subtree range queries.
- **Inorder Traversal**: When you prefer leaning on the BST's sorted-order property, or plan to reuse the inorder sequence for other checks.

### Optimization Notes

- All three approaches short-circuit on the first violation, avoiding unnecessary traversal.
- Recursive Bounds and Inorder Traversal both collapse the brute force's repeated subtree scans into a single pass by propagating constraints instead of re-deriving them.
- The Inorder Traversal can be rewritten with an explicit stack to remove recursion depth limits on extremely skewed trees.
- None of the approaches needs to materialize the full value list, keeping auxiliary space at `O(h)` rather than `O(n)`.

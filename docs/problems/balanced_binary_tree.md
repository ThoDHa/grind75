# [Balanced Binary Tree](https://leetcode.com/problems/balanced-binary-tree/)

**Easy** | **20 minutes** | **Tree, DFS, Binary Tree**

**Pattern:** [Tree Traversal](../patterns/tree/intuition.md)

**Practice:** [`practice/balanced_binary_tree/solution.py`](https://github.com/ThoDHa/grind75/blob/main/practice/balanced_binary_tree/solution.py)

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

The solutions below assume the standard LeetCode node definition and
`from typing import Optional`:

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

### Top-Down Recursion

```python
class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        if not root:
            return True
        if abs(self.height(root.left) - self.height(root.right)) > 1:
            return False
        return self.isBalanced(root.left) and self.isBalanced(root.right)

    def height(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        return 1 + max(self.height(root.left), self.height(root.right))
```

#### Approach

This approach follows the problem definition literally. A tree is balanced when
every node has left and right subtrees whose heights differ by at most `1`, so
we check that condition at each node and recurse into the children.

1. An empty tree is balanced, so return `True` for a null `root`.
2. Compute the height of the left and right subtrees and compare them. If they
   differ by more than `1`, the current node violates the balance condition, so
   return `False`.
3. Otherwise, recursively require that both the left and right subtrees are also
   balanced.

The `height` helper computes the number of nodes on the longest root-to-leaf
path of a subtree, recurring into both children and taking the larger result.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

The `height` helper visits every node of a subtree, and `isBalanced` calls it at
every node. In the worst case (a skewed tree) the same nodes are revisited at
every level, producing quadratic work. For a balanced tree the cost is closer to
`O(n log n)`.

##### Space Complexity: `O(h)`

Where `h` is the height of the tree. The recursion stack grows as deep as the
longest path: `O(log n)` for a balanced tree and `O(n)` for a skewed one.

#### Key Insights

- Mirrors the definition directly, which makes it the easiest version to derive.
- Separating height calculation from the balance check keeps each helper simple.
- The redundant height recomputation at each level is the source of the
  quadratic cost and motivates the bottom-up optimization.

### Bottom-Up Recursion

```python
class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        def check(node: Optional[TreeNode]) -> int:
            if not node:
                return 0
            left = check(node.left)
            if left == -1:
                return -1
            right = check(node.right)
            if right == -1:
                return -1
            if abs(left - right) > 1:
                return -1
            return 1 + max(left, right)

        return check(root) != -1
```

#### Approach

The top-down version is slow because it recomputes heights. The fix is to fold
the balance check into a single post-order traversal that returns the height of
each subtree and reuses a sentinel value to report imbalance.

1. The inner `check` returns the height of a balanced subtree, or `-1` if any
   part of that subtree is unbalanced.
2. An empty subtree has height `0`.
3. Evaluate the left child first. If it already reported `-1`, propagate `-1`
   upward immediately without inspecting the right child.
4. Evaluate the right child with the same early exit.
5. If the two child heights differ by more than `1`, this node is unbalanced, so
   return `-1`.
6. Otherwise return the real height, `1 + max(left, right)`.

The tree is balanced exactly when `check(root)` is not `-1`.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each node is visited exactly once, and only constant-time work happens per node
because the height and balance check are combined.

##### Space Complexity: `O(h)`

Where `h` is the height of the tree. Only the recursion stack is used: `O(log n)`
for a balanced tree and `O(n)` for a skewed one.

#### Key Insights

- The `-1` sentinel doubles as both "unbalanced" and an impossible height,
  letting one return value carry both pieces of information.
- Post-order traversal processes children before parents, so each height is
  computed once and reused.
- Early termination stops as soon as the first unbalanced subtree is found.

### Iterative Post-Order

```python
class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        heights = {None: 0}
        stack = []
        node = root
        last_visited = None
        while stack or node:
            if node:
                stack.append(node)
                node = node.left
            else:
                peek = stack[-1]
                if peek.right and last_visited is not peek.right:
                    node = peek.right
                else:
                    left_h = heights[peek.left]
                    right_h = heights[peek.right]
                    if abs(left_h - right_h) > 1:
                        return False
                    heights[peek] = 1 + max(left_h, right_h)
                    last_visited = stack.pop()
        return True
```

#### Approach

This approach reproduces the bottom-up logic without recursion, which avoids any
risk of exceeding the interpreter's recursion limit on a deeply skewed tree. It
performs an explicit post-order traversal with a manual stack, recording each
node's height in a dictionary as it is finished.

1. Keep a `heights` map seeded with `None -> 0` so absent children contribute a
   height of `0`.
2. Walk left as far as possible, pushing every node onto the stack.
3. When the left spine is exhausted, peek at the top of the stack. If it has a
   right child that has not been processed yet, descend into that right subtree.
4. Otherwise both children are finished, so look up their recorded heights. If
   they differ by more than `1`, return `False` immediately.
5. Record the node's height as `1 + max(left, right)`, mark it visited, and pop
   it.
6. If the traversal completes without finding an imbalance, the tree is balanced.

The `last_visited` pointer distinguishes "about to descend right" from "returning
from the right subtree", which is what makes an iterative post-order traversal
correct.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each node is pushed and popped once, and the per-node work is constant.

##### Space Complexity: `O(h)`

The stack holds at most one root-to-leaf path at a time, and the `heights` map
stores a bounded number of live entries proportional to the current path. Both
are bounded by the tree height `h`.

#### Key Insights

- Converts the recursion into an explicit stack, removing the call-depth limit
  as a failure mode for very deep trees.
- Storing finished heights in a map is the iterative equivalent of returning a
  height from a recursive call.
- The `last_visited` sentinel is the standard trick for iterative post-order
  traversal and is essential for visiting each node only after both children.

## Comparison of Solutions

### Time Complexity

- **Top-Down Recursion**: `O(n^2)` - recomputes subtree heights at every level.
- **Bottom-Up Recursion**: `O(n)` - one combined height-and-balance pass.
- **Iterative Post-Order**: `O(n)` - same single pass, managed with an explicit
  stack.

### Space Complexity

- **All three**: `O(h)` - proportional to tree height, from the recursion stack
  or the explicit stack plus height map.

### Trade-offs

- **Top-Down Recursion**: Easiest to derive from the definition, but quadratic
  on large or skewed trees.
- **Bottom-Up Recursion**: Linear and concise, at the cost of a slightly less
  obvious sentinel trick.
- **Iterative Post-Order**: Linear and immune to recursion-depth limits, at the
  cost of more bookkeeping (manual stack, `last_visited`, height map).

### When to Use Each

- **Top-Down Recursion**: Small trees or when readability outweighs performance.
- **Bottom-Up Recursion**: The default choice for interviews and production code.
- **Iterative Post-Order**: Pathologically deep trees where the recursion limit
  is a real concern.

### Optimization Notes

- The bottom-up pass eliminates the redundant height recomputation that makes the
  top-down version quadratic.
- The `-1` sentinel encodes both imbalance and an impossible height in a single
  return value, enabling early termination.
- The iterative version trades the implicit call stack for an explicit one,
  delivering the same `O(n)` behavior without depending on the interpreter's
  recursion limit.

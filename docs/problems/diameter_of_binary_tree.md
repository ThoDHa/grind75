# [Diameter of Binary Tree](https://leetcode.com/problems/diameter-of-binary-tree/)

**Easy** | **20 minutes** | **Tree, Depth-First Search, Binary Tree**

**Pattern:** [Tree DP](../patterns/tree_dp/intuition.md)

**Practice:** [`practice/diameter_of_binary_tree/solution.py`](../../practice/diameter_of_binary_tree/solution.py)

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

### Brute Force

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        def height(node: Optional[TreeNode]) -> int:
            if not node:
                return 0
            return 1 + max(height(node.left), height(node.right))

        def diameter(node: Optional[TreeNode]) -> int:
            if not node:
                return 0
            # Longest path bending at this node: edges down each side
            through = height(node.left) + height(node.right)
            # Or the best path lies entirely in one of the subtrees
            return max(through, diameter(node.left), diameter(node.right))

        return diameter(root)
```

#### Approach

The most direct reading of the definition is to consider every node in turn as
the bend point of a path. For a path that turns at a given node, its edge length
is the height of the left subtree plus the height of the right subtree. The
diameter is the largest such value over all nodes, or, equivalently, the best
path either bends at the current node or sits entirely within one of its
subtrees.

1. Write a `height(node)` helper that recomputes a subtree's height (in edges)
   from scratch every time it is called.
2. Write a `diameter(node)` helper that, for the current node, measures the path
   bending here as `height(node.left) + height(node.right)`.
3. Take the maximum of that bending path and the diameters of the left and right
   subtrees, recursing on each.
4. Return the diameter of the whole tree from `diameter(root)`.

This separates the two questions (how tall is a subtree, how wide is its best
path) into two independent recursions, which is the straightforward but wasteful
way to reach a correct answer.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

For every node, `diameter` calls `height` on its children, and `height` itself
walks the entire subtree below that node. In the worst case (a skewed tree) the
height computation costs `O(n)` and it is repeated for `O(n)` nodes, giving
`O(n^2)`.

##### Space Complexity: `O(h)`

Where `h` is the tree height. Both recursions descend at most to the depth of the
tree, and they are not active at the same level simultaneously, so the call stack
is bounded by `O(h)`.

#### Key Insights

- Directly encodes the definition: try every node as the path's bend point and
  take the widest.
- The waste is structural: heights are recomputed from scratch at every node
  instead of being reused, which is exactly the redundancy the single-pass
  solutions remove.
- Splitting height and diameter into two separate recursions keeps the logic easy
  to read at the cost of doing the same descent many times over.

#### Walkthrough

Let us trace the brute force on Example 1: `root = [1,2,3,4,5]`. That array
describes this tree: node `1` has children `2` (left) and `3` (right), and node
`2` has children `4` (left) and `5` (right). Nodes `3`, `4`, and `5` are leaves.

The call is `diameter(1)`. Because `diameter` recurses into its children before
combining, the deepest nodes finish first. We follow each call as it returns, and
for every node we record `lh = height(node.left)`, `rh = height(node.right)`,
`through = lh + rh`, and the returned `diameter`. Remember that an empty child has
height `0`, and `height` is recomputed from scratch each time it is asked.

| Call | `lh` | `rh` | `through = lh + rh` | returns `max(through, left_d, right_d)` |
|------|------|------|---------------------|-----------------------------------------|
| `diameter(4)` | `0` | `0` | `0` | `0` (leaf) |
| `diameter(5)` | `0` | `0` | `0` | `0` (leaf) |
| `diameter(2)` | `1` | `1` | `2` | `max(2, 0, 0) = 2` |
| `diameter(3)` | `0` | `0` | `0` | `0` (leaf) |
| `diameter(1)` | `2` | `1` | `3` | `max(3, 2, 0) = 3` |

At node `2`, both children are leaves of height `1`, so the path bending there
spans `2` edges (`4 -> 2 -> 5`). At the root, the left subtree has height `2` (down
to `4` or `5`) and the right subtree has height `1` (down to `3`), so the path
bending at the root spans `3` edges (`4 -> 2 -> 1 -> 3`). Taking the maximum of
that bend (`3`) against the best diameters found inside the subtrees (`2` and `0`)
gives `3`.

`diameter(1)` returns `3`, which matches the expected Output of `3`.

### Recursive DFS with Instance Variable

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        self.diameter = 0

        def height(node: Optional[TreeNode]) -> int:
            if not node:
                return 0
            left_h = height(node.left)
            right_h = height(node.right)
            self.diameter = max(self.diameter, left_h + right_h)
            return 1 + max(left_h, right_h)

        height(root)
        return self.diameter
```

#### Approach

The diameter is the number of edges on the longest path between any two nodes,
and that path may or may not pass through the root. The central observation is
that for any single node, the longest path that bends at that node has length
`left_height + right_height`, where each height counts the edges down to the
deepest leaf on that side. The overall diameter is therefore the maximum of this
quantity taken over every node.

A single post-order DFS computes both pieces of information in one pass:

1. Define a helper `height(node)` that returns the height of the subtree rooted
   at `node`, measured in edges (an empty subtree has height `0`).
2. For each node, recurse into the left and right children to get `left_h` and
   `right_h`.
3. Update the running maximum diameter with `left_h + right_h`, the length of the
   path that passes through this node.
4. Return `1 + max(left_h, right_h)` to the parent, since only one branch can
   continue a path upward.

The instance variable `self.diameter` accumulates the best path seen anywhere in
the tree while the return value feeds the parent's own height computation.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each of the `n` nodes is visited exactly once, with constant work per node.

##### Space Complexity: `O(h)`

Where `h` is the height of the tree, consumed by the recursion call stack. This is
`O(log n)` for a balanced tree and `O(n)` for a fully skewed tree.

#### Key Insights

- The longest path need not pass through the root, so tracking a global maximum
  across all nodes is required rather than reading the answer off the root alone.
- Height and diameter are computed together in one traversal: the function returns
  height while the side effect records diameter.
- A path bends at exactly one node, which is why each node contributes
  `left_h + right_h` and why the parent receives only `1 + max(left_h, right_h)`.

### Recursive DFS with Nonlocal Variable

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        diameter = 0

        def height(node: Optional[TreeNode]) -> int:
            nonlocal diameter
            if not node:
                return 0
            left_h = height(node.left)
            right_h = height(node.right)
            diameter = max(diameter, left_h + right_h)
            return 1 + max(left_h, right_h)

        height(root)
        return diameter
```

#### Approach

This is the same single-pass post-order DFS as above, but the shared maximum lives
in a local variable captured by the closure instead of on the instance. The
`nonlocal` keyword lets the inner `height` function rebind the enclosing
`diameter`, keeping all state confined to the method call rather than persisting on
`self` between invocations.

1. Initialize `diameter` to `0` in the method body.
2. Declare it `nonlocal` inside `height` so updates mutate the captured variable.
3. At each node, update `diameter` with `left_h + right_h` and return
   `1 + max(left_h, right_h)`.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Every node is visited once with constant work, identical to the instance-variable
version.

##### Space Complexity: `O(h)`

The recursion stack uses space proportional to the tree height.

#### Key Insights

- `nonlocal` avoids leaving state on the instance, so repeated calls to the same
  `Solution` object cannot interfere with one another.
- The accumulation pattern is otherwise identical: one traversal computes height
  while recording the widest bend seen.

### Return Pair Approach

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        def dfs(node: Optional[TreeNode]) -> tuple[int, int]:
            if not node:
                return (0, 0)  # (height, diameter)
            left_h, left_d = dfs(node.left)
            right_h, right_d = dfs(node.right)
            height = 1 + max(left_h, right_h)
            diameter = max(left_d, right_d, left_h + right_h)
            return (height, diameter)

        return dfs(root)[1]
```

#### Approach

This version carries no shared state at all. Each recursive call returns a tuple
`(height, diameter)` describing the subtree it just processed, and every value
flows purely through return values.

1. An empty subtree returns `(0, 0)`: height `0` and diameter `0`.
2. For an internal node, recurse to obtain `(left_h, left_d)` and
   `(right_h, right_d)`.
3. The node's height is `1 + max(left_h, right_h)`.
4. The best diameter within this subtree is the maximum of the left subtree's
   diameter, the right subtree's diameter, and the path bending at this node,
   `left_h + right_h`.
5. The final answer is the diameter component returned for the whole tree.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each node is visited once, with constant work to combine its children's results.

##### Space Complexity: `O(h)`

Space is bounded by the recursion depth, which equals the tree height.

#### Key Insights

- A "pure functional" style with no side effects: all information is threaded
  through return values, which can be easier to reason about and test.
- The tuple return generalizes naturally to problems that need to propagate
  several aggregates up the tree in a single traversal.
- Functionally equivalent to the accumulator versions; the difference is purely in
  how the maximum is communicated.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n^2)` - heights are recomputed from scratch at every node.
- **Recursive DFS with Instance Variable**: `O(n)` - each node visited once.
- **Recursive DFS with Nonlocal Variable**: `O(n)` - each node visited once.
- **Return Pair Approach**: `O(n)` - each node visited once.

### Space Complexity

- **Brute Force**: `O(h)` - recursion stack bounded by the tree height.
- **Recursive DFS with Instance Variable**: `O(h)` - recursion stack.
- **Recursive DFS with Nonlocal Variable**: `O(h)` - recursion stack.
- **Return Pair Approach**: `O(h)` - recursion stack, plus a constant-size tuple
  per frame.

### Trade-offs

- The brute force is the most literal translation of the definition but pays for
  that clarity by recomputing every subtree height repeatedly, making it `O(n^2)`.
- The instance-variable version is concise but leaves mutable state on `self`,
  which can surprise callers that reuse a `Solution` object.
- The nonlocal version keeps the shared maximum local to the call while remaining
  just as compact, at the cost of the `nonlocal` declaration.
- The return-pair version eliminates shared state entirely but must pack and unpack
  a tuple at every node.

### When to Use Each

- **Brute Force**: As a teaching baseline that mirrors the definition directly;
  too slow for the upper constraint of `10^4` nodes on a skewed tree.
- **Recursive DFS with Instance Variable**: When brevity matters and the object is
  used for a single call.
- **Recursive DFS with Nonlocal Variable**: When avoiding instance state is
  preferred but a single accumulator is still the clearest expression.
- **Return Pair Approach**: When side-effect-free code is valued, or as a template
  for problems that aggregate multiple values up the tree.

### Optimization Notes

- The key optimization over the brute force is computing height and diameter in a
  single post-order traversal, reusing each subtree's height instead of recomputing
  it. This collapses `O(n^2)` into `O(n)`.
- The three single-pass versions rely on the same core idea: one traversal that
  computes subtree height and simultaneously tracks the widest bend.
- Measuring height in edges (empty subtree height `0`) makes `left_h + right_h`
  directly equal to the edge count of the path through a node, avoiding off-by-one
  corrections.
- The path that realizes the diameter bends at exactly one node, so each parent
  only ever extends one branch upward via `1 + max(left_h, right_h)`.

The three single-pass solutions share identical asymptotic time and space behavior;
the choice among them is primarily a matter of how state is managed.

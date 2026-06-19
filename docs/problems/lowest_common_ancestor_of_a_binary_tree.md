# [Lowest Common Ancestor of a Binary Tree](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/)

**Medium** | **25 minutes** | **Tree, Depth-First Search, Binary Tree**

**Pattern:** [Tree Traversal](../patterns/tree/intuition.md)

**Practice:** [`practice/lowest_common_ancestor_of_a_binary_tree/solution.py`](../../practice/lowest_common_ancestor_of_a_binary_tree/solution.py)

Given a binary tree, find the lowest common ancestor (LCA) of two given nodes in the tree.

According to the definition of LCA on Wikipedia: "The lowest common ancestor is defined between two nodes `p` and `q` as the lowest node in `T` that has both `p` and `q` as descendants (where we allow a node to be a descendant of itself)."

## Examples

### Example 1

**Input:** `root = [3,5,1,6,2,0,8,null,null,7,4]`, `p = 5`, `q = 1`

**Output:** `3`

**Explanation:** The LCA of nodes `5` and `1` is `3`.

### Example 2

**Input:** `root = [3,5,1,6,2,0,8,null,null,7,4]`, `p = 5`, `q = 4`

**Output:** `5`

**Explanation:** The LCA of nodes `5` and `4` is `5`, since a node can be a descendant of itself according to the LCA definition.

### Example 3

**Input:** `root = [1,2]`, `p = 1`, `q = 2`

**Output:** `1`

## Constraints

- The number of nodes in the tree is in the range `[2, 10^5]`.
- `-10^9 <= Node.val <= 10^9`
- All `Node.val` are unique.
- `p != q`
- `p` and `q` will exist in the tree.

## Solutions

### Recursive DFS

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None
class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        # An empty subtree contains neither target; a node that is p or q
        # reports itself upward
        if not root or root is p or root is q:
            return root

        # Search both subtrees for the targets
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)

        # Targets found on opposite sides -> this node is their LCA
        if left and right:
            return root

        # Otherwise both lie in (at most) one subtree; bubble up that result
        return left if left else right
```

#### Approach

The lowest common ancestor is the deepest node from which `p` and `q` are
reachable in different directions (or the node that is itself one of them while
the other lies below). A single post-order traversal answers this: each call
reports back the relevant node it found, and the first node that hears back from
*both* of its sides is the LCA.

1. Base case: a `None` subtree returns `None`. If the current node *is* `p` or
   `q`, return it immediately. Because the inputs are guaranteed present and a
   node may be its own ancestor, this correctly handles the case where one target
   sits above the other.
2. Recurse into the left and right subtrees.
3. If both recursive calls return non-null, `p` and `q` were found on opposite
   sides, so the current node is their lowest common ancestor.
4. If only one side is non-null, both targets live within that side; propagate
   that node upward unchanged.

Correctness follows from the post-order order: a node only declares itself the
LCA once both descendants have reported, guaranteeing we return the deepest such
node.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

In the worst case we visit every node once, doing constant work per node.

##### Space Complexity: `O(h)`

The recursion stack is bounded by the tree height `h`, which is `O(n)` for a
skewed tree and `O(log n)` for a balanced one.

#### Key Insights

- Returning the found target (or `None`) from each call lets the recursion both
  locate the nodes and identify the split point in one pass.
- The node where the search "splits", with one target on each side, is exactly
  the LCA.
- Identity comparison (`is`) is used because we are matching node references, not
  values.
- Allowing a node to be a descendant of itself is handled for free by returning
  early when `root is p or root is q`.

### Iterative with Parent Pointers

```python
from collections import deque

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None
class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        # Record each node's parent by walking the tree until both targets seen.
        parent = {root: None}
        queue = deque([root])

        while p not in parent or q not in parent:
            node = queue.popleft()
            if node.left:
                parent[node.left] = node
                queue.append(node.left)
            if node.right:
                parent[node.right] = node
                queue.append(node.right)

        # Collect every ancestor of p (including p itself) into a set.
        ancestors = set()
        node = p
        while node:
            ancestors.add(node)
            node = parent[node]

        # Climb from q until we hit the first node shared with p's ancestry.
        node = q
        while node not in ancestors:
            node = parent[node]
        return node
```

#### Approach

Instead of recursing, this approach makes the tree's implicit upward edges
explicit by recording each node's parent during a breadth-first walk. Once both
`p` and `q` have parents on record, the LCA becomes the first shared node along
the two upward paths to the root.

1. Traverse the tree (BFS here), storing `parent[child] = node` for every node
   discovered. Stop as soon as both `p` and `q` appear in the `parent` map, since
   nothing below them matters.
2. Walk upward from `p` to the root, collecting every node on that path into an
   `ancestors` set.
3. Walk upward from `q`. The first node already present in `ancestors` is the
   lowest node common to both paths, which is exactly the LCA.

The root's parent is set to `None` so the upward walks terminate cleanly. This
mirrors the classic technique for finding the intersection of two linked paths,
applied to the chains of ancestry running from each target to the root.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Building the parent map visits at most every node once. Each upward walk is
bounded by the tree height, which is itself `O(n)`, so the total stays linear.

##### Space Complexity: `O(n)`

The `parent` map stores one entry per visited node, the BFS queue can hold up to
a full level, and the `ancestors` set holds one path to the root. All three are
bounded by `O(n)`.

#### Key Insights

- Recording parent pointers converts the downward-only tree into a structure
  where each node can climb back toward the root, which is what makes the
  iterative solution possible.
- Halting the traversal once both targets are mapped avoids scanning the entire
  tree when both nodes appear early.
- Gathering one target's ancestry into a set turns the "first common ancestor"
  question into a simple membership test as the other target climbs.
- Setting the root's parent to `None` gives both upward walks a guaranteed
  termination point.

## Comparison of Solutions

### Time Complexity

- **Recursive DFS**: `O(n)` - A single post-order traversal touches each node once.
- **Iterative with Parent Pointers**: `O(n)` - Building the parent map is linear, and the two upward walks are each bounded by the tree height.

### Space Complexity

- **Recursive DFS**: `O(h)` - Only the recursion stack is used, bounded by tree height `h`.
- **Iterative with Parent Pointers**: `O(n)` - The parent map, BFS queue, and ancestor set each scale with the node count.

### Trade-offs

- **Recursive DFS**: Compact and elegant with no auxiliary data structures, but it relies on the call stack, which can overflow on a deeply skewed tree of `10^5` nodes.
- **Iterative with Parent Pointers**: Avoids recursion depth limits entirely, but it allocates explicit maps and sets that consume more memory.

### When to Use Each

- **Recursive DFS (Recommended)**: Best for interviews and balanced trees - the cleanest expression of the LCA idea in a single pass.
- **Iterative with Parent Pointers**: When the tree may be extremely deep and recursion could exceed Python's stack limit, or when an explicit non-recursive solution is required.

### Optimization Notes

- The recursive solution can convert to an explicit stack if recursion depth is the only concern, but the parent-pointer approach reads more naturally.
- Stopping the BFS as soon as both targets are recorded prevents needless traversal of the rest of the tree when `p` and `q` sit near the top.
- For repeated LCA queries on a static tree, precomputing parent pointers (or binary-lifting tables) once amortizes the cost across many queries, which neither single-query solution exploits.

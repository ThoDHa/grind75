# [Binary Tree Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/)

**Medium** | **20 minutes** | **Tree, BFS, Binary Tree**

**Pattern:** [Tree Traversal](../patterns/tree/intuition.md)

**Practice:** [`practice/binary_tree_level_order_traversal/solution.py`](../../practice/binary_tree_level_order_traversal/solution.py)

Given the `root` of a binary tree, return the level order traversal of its nodes' values. (i.e., from left to right, level by level).

## Examples

### Example 1

![Binary Tree Example](assets/binary_tree_level_order_traversal_example1.jpg)

**Input:** `root = [3,9,20,null,null,15,7]`

**Output:** `[[3],[9,20],[15,7]]`

### Example 2

**Input:** `root = [1]`

**Output:** `[[1]]`

### Example 3

**Input:** `root = []`

**Output:** `[]`

## Constraints

- The number of nodes in the tree is in the range `[0, 2000]`.
- `-1000 <= Node.val <= 1000`

## Solutions

### Iterative BFS

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from collections import deque

class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []

        result = []
        queue = deque([root])
        while queue:
            level_size = len(queue)
            level = []
            for _ in range(level_size):
                node = queue.popleft()
                level.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            result.append(level)
        return result
```

#### Approach

Level order traversal is a textbook breadth-first search. The trick is grouping nodes by level, which we achieve by measuring each level's size before draining it:

1. Return an empty list immediately when the tree is empty.
2. Seed a queue with `root`.
3. While the queue is non-empty, capture `level_size = len(queue)`: the exact count of nodes on the current level.
4. Dequeue that many nodes, collecting their values into a fresh `level` list and enqueuing each node's children (left then right).
5. Append the completed `level` to `result` and repeat for the next level.

Snapshotting `level_size` at the top of each iteration is what cleanly partitions the output into per-level sublists, since any children appended during the loop belong to the next level and are excluded from the current count.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Every node is enqueued and dequeued exactly once, and each contributes constant work, giving linear time in the number of nodes.

##### Space Complexity: `O(n)`

The output stores all `n` node values. The queue independently holds at most one level, which is up to `n/2` nodes for a complete tree, so the auxiliary space is also `O(n)`.

#### Key Insights

- Recording `level_size` before the inner loop is the idiomatic way to separate BFS levels without sentinel markers.
- A `deque` gives `O(1)` `popleft`, unlike a plain list whose `pop(0)` is `O(n)`.
- Enqueuing left before right preserves the required left-to-right ordering within each level.
- The pattern generalizes directly to zigzag traversal, right side view, and per-level aggregates.

### Recursive DFS

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        result = []

        def visit(node: Optional[TreeNode], depth: int) -> None:
            if not node:
                return
            # First time we reach this depth, start a fresh sublist for it
            if depth == len(result):
                result.append([])
            result[depth].append(node.val)
            visit(node.left, depth + 1)
            visit(node.right, depth + 1)

        visit(root, 0)
        return result
```

#### Approach

A depth-first traversal can produce level-order output if it tracks how deep each node sits and appends values into the correct per-level bucket:

1. Maintain a `result` list whose index `depth` holds the values for that level.
2. Recurse with a `depth` parameter, starting at `0` for the root.
3. When `depth == len(result)`, this is the first node encountered at that depth, so append a new empty sublist to grow `result`.
4. Append the current node's value to `result[depth]`.
5. Recurse into the left child before the right child, both at `depth + 1`.

Visiting left before right in preorder guarantees that values land in each level's sublist in left-to-right order, matching the BFS output exactly even though the traversal itself is depth-first.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each node is visited once and performs constant work, so the traversal is linear in the number of nodes.

##### Space Complexity: `O(n)`

The output stores all `n` values. The recursion stack adds `O(h)` for the tree height `h`, which is `O(n)` for a skewed tree and `O(log n)` when balanced, so the output term dominates at `O(n)`.

#### Key Insights

- Indexing `result` by depth turns DFS into a level grouping without any queue.
- The `depth == len(result)` check is the lazy-allocation trick that creates each level's bucket exactly when first needed.
- Preorder left-before-right is what keeps every level ordered correctly.
- This approach is convenient when recursion is already natural for the surrounding code, trading queue space for recursion-stack space.

## Comparison of Solutions

### Time Complexity

- **Iterative BFS**: `O(n)` - Each node is enqueued and dequeued once
- **Recursive DFS**: `O(n)` - Each node is visited once

### Space Complexity

- **Iterative BFS**: `O(n)` - Output plus a queue holding up to one full level
- **Recursive DFS**: `O(n)` - Output plus an `O(h)` recursion stack

### Trade-offs

- BFS maps directly to the level-by-level framing, making the level grouping obvious from the queue mechanics.
- Recursive DFS removes the explicit queue but introduces a recursion stack that can overflow on a very deep tree.
- BFS peaks at the widest level, while DFS peaks at the tallest path, so the cheaper auxiliary structure depends on tree shape.

### When to Use Each

- **Iterative BFS**: When the level-by-level reading is the clearest expression of the problem, or when the tree may be very deep.
- **Recursive DFS**: When recursion is already idiomatic in the surrounding code and the tree depth is bounded.

### Optimization Notes

- Both approaches are `O(n)` time, so the choice is driven by which auxiliary structure better fits the expected tree shape.
- For very deep trees, BFS avoids the recursion-depth ceiling that the DFS solution can hit.
- Indexing the result list by depth lets DFS group levels without sentinel markers, mirroring how BFS uses `level_size`.

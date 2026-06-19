# [Maximum Depth of Binary Tree](https://leetcode.com/problems/maximum-depth-of-binary-tree/)

**Easy** | **15 minutes** | **Tree, Depth-First Search, Breadth-First Search, Binary Tree**

**Pattern:** [Tree Traversal](../patterns/tree/intuition.md)

**Practice:** [`practice/maximum_depth_of_binary_tree/solution.py`](../../practice/maximum_depth_of_binary_tree/solution.py)

Given the `root` of a binary tree, return its maximum depth.

A binary tree's **maximum depth** is the number of nodes along the longest path from the root node down to the farthest leaf node.

## Examples

### Example 1

![Maximum Depth of Binary Tree Example 1](assets/maximum_depth_of_binary_tree_example1.jpg)

**Input:** `root = [3,9,20,null,null,15,7]`

**Output:** `3`

### Example 2

**Input:** `root = [1,null,2]`

**Output:** `2`

### Example 3

**Input:** `root = []`

**Output:** `0`

## Constraints

- The number of nodes in the tree is in the range `[0, 10^4]`.
- `-100 <= Node.val <= 100`

## Solutions

### Recursive DFS

```python
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))
```

#### Approach

This recursive solution uses depth-first search to traverse the binary tree. The depth of a node is defined in terms of its children, which makes recursion a natural fit:

1. If the node is `None`, the subtree is empty and its depth is `0`.
2. Otherwise, recursively compute the maximum depth of the left and right subtrees.
3. The depth at the current node is `1` plus the larger of those two subtree depths, where the `1` counts the current node.

Because each node's result is combined only after both children return, this follows the post-order pattern: children are fully processed before the parent produces its answer.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Every node in the tree is visited exactly once, so the work is linear in the number of nodes `n`.

##### Space Complexity: `O(h)`

The space is the depth of the recursion stack, which equals the height of the tree `h`. In the worst case of a completely unbalanced tree this is `O(n)`; for a balanced tree it is `O(log n)`.

#### Key Insights

- The recurrence `depth(node) = 1 + max(depth(left), depth(right))` mirrors the recursive structure of the tree itself.
- Treating the empty subtree as depth `0` removes the need for any special leaf handling.
- It is the most concise and readable approach, though deep trees can risk exceeding the recursion limit.

### Iterative BFS

```python
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0

        queue = deque([root])
        depth = 0

        while queue:
            depth += 1
            for _ in range(len(queue)):
                node = queue.popleft()
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

        return depth
```

#### Approach

This solution uses breadth-first search to walk the tree one level at a time, counting the number of levels:

1. If the root is `None`, return `0`.
2. Seed a queue with the root and start a `depth` counter at `0`.
3. On each iteration, record the current queue length, then dequeue exactly that many nodes, enqueuing each of their children.
4. Processing a full level corresponds to descending one level, so increment `depth` once per level.
5. When the queue empties, `depth` equals the number of levels, which is the maximum depth.

Snapshotting `len(queue)` before the inner loop is what isolates one level from the next, since children added during the loop belong to the following level.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each node is enqueued and dequeued exactly once, giving linear time.

##### Space Complexity: `O(w)`

The queue holds at most one full level at a time, so the space is bounded by the maximum width `w` of the tree. For a perfect binary tree the widest level holds about `n/2` nodes, which is `O(n)`.

#### Key Insights

- Iterating level by level lets depth be counted directly without tracking per-node depths.
- Capturing the level size before draining the queue cleanly separates one level from the next.
- BFS uses recursion-free control flow, avoiding stack-overflow risk on very deep trees.

### Iterative DFS with Stack

```python
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0

        stack = [(root, 1)]
        max_depth = 0

        while stack:
            node, depth = stack.pop()
            max_depth = max(max_depth, depth)
            if node.right:
                stack.append((node.right, depth + 1))
            if node.left:
                stack.append((node.left, depth + 1))

        return max_depth
```

#### Approach

This solution simulates the recursive traversal with an explicit stack, carrying each node's depth alongside the node:

1. If the root is `None`, return `0`.
2. Push `(root, 1)` onto the stack and initialize `max_depth` to `0`.
3. Pop a `(node, depth)` pair, update `max_depth` with `depth`, and push each existing child paired with `depth + 1`.
4. Continue until the stack is empty; `max_depth` then holds the deepest path length seen.

Pairing depth with the node is the key difference from recursion: the call stack no longer tracks depth for us, so we store it explicitly.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each node is pushed and popped exactly once, so the traversal is linear.

##### Space Complexity: `O(h)`

The stack mirrors a root-to-leaf path, so its size is bounded by the height `h`: `O(n)` for an unbalanced tree and `O(log n)` for a balanced one.

#### Key Insights

- Storing `(node, depth)` pairs replaces the implicit depth bookkeeping that recursion provides for free.
- An explicit stack removes recursion-depth limits while keeping the depth-first traversal order.
- Pushing the right child before the left makes the traversal visit the left subtree first, though the final maximum is unaffected by visit order.

## Comparison of Solutions

### Time Complexity

- **Recursive DFS**: `O(n)` - visits each node once.
- **Iterative BFS**: `O(n)` - visits each node once.
- **Iterative DFS with Stack**: `O(n)` - visits each node once.

### Space Complexity

- **Recursive DFS**: `O(h)` - bounded by the recursion depth, the tree height.
- **Iterative BFS**: `O(w)` - bounded by the widest level of the tree.
- **Iterative DFS with Stack**: `O(h)` - bounded by the stack holding one root-to-leaf path.

### Trade-offs

- Recursive DFS is the shortest and clearest, but very deep trees can exceed the recursion limit.
- Iterative BFS removes recursion risk and counts levels directly, at the cost of more memory on wide trees.
- Iterative DFS with Stack removes recursion risk while staying depth-first, at the cost of tracking depths explicitly.

### When to Use Each

- **Recursive DFS**: When readability matters most and the tree is not pathologically deep.
- **Iterative BFS**: When the tree may be deep and you want to avoid recursion, especially when level information is also useful.
- **Iterative DFS with Stack**: When you want recursion-free depth-first traversal and prefer `O(h)` space over BFS's `O(w)`.

### Optimization Notes

- All three approaches are `O(n)` in time, so the practical choice hinges on space and recursion-depth constraints rather than speed.
- For trees deep enough to threaten Python's default recursion limit, prefer either iterative approach over Recursive DFS.
- In interview settings the Recursive DFS solution is usually preferred first for its clarity, with an iterative approach offered as the follow-up that avoids stack overflow.

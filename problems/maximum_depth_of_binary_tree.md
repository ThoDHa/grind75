# [Maximum Depth of Binary Tree](https://leetcode.com/problems/maximum-depth-of-binary-tree/)

Easy - 15 minutes - Tree, Depth-First Search, Breadth-First Search, Binary Tree

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

### Solution 1: Recursive DFS

```python
def maxDepth(self, root: Optional[TreeNode]) -> int:
    if root == None:
        return 0

    left = self.maxDepth(root.left)
    right = self.maxDepth(root.right)

    return max(left, right) + 1
```

#### Approach

This recursive solution uses depth-first search to traverse the binary tree. For each node, it calculates the maximum depth by:

1. If the node is null, the depth is 0
2. Otherwise, recursively find the maximum depth of both left and right subtrees
3. The depth of the current node is the maximum of the left and right subtree depths plus 1 (counting the current node)

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Every node in the tree is visited exactly once, resulting in O(n) time complexity where n is the number of nodes.

##### Space Complexity: `O(h)`

The space complexity is determined by the maximum depth of the recursion stack, which equals the height of the tree (h). In the worst case (completely unbalanced tree), this could be O(n). In the best case (completely balanced tree), this would be O(log n).

#### Key Insights

- Simple and elegant recursive solution
- Follows the post-order traversal pattern (process children before parent)
- Leverages the recursive structure of the tree problem

### Solution 2: Iterative BFS (Level Order Traversal)

```python
def maxDepth(self, root: Optional[TreeNode]) -> int:
    if not root:
        return 0
    
    queue = deque([root])
    depth = 0
    
    while queue:
        level_size = len(queue)
        
        for _ in range(level_size):
            node = queue.popleft()
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        depth += 1
    
    return depth
```

#### Approach

This solution uses breadth-first search with a queue to traverse the tree level by level:

1. Start with the root node in the queue and a depth counter of 0
2. For each level, process all nodes currently in the queue
3. For each node, add its children to the queue
4. Increment depth counter after processing each level
5. Continue until the queue is empty

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each node is processed exactly once, resulting in O(n) time complexity.

##### Space Complexity: `O(w)`

The space required is proportional to the maximum width of the tree. In the worst case (perfect binary tree's widest level), this would be O(n/2) which simplifies to O(n).

#### Key Insights

- Iterative solution that avoids recursion overhead
- Processes tree in level order
- Clear separation of levels makes tracking depth straightforward

### Solution 3: Iterative DFS with Stack

```python
def maxDepth(self, root: Optional[TreeNode]) -> int:
    if not root:
        return 0
    
    stack = [(root, 1)]
    max_depth = 0
    
    while stack:
        node, current_depth = stack.pop()
        
        max_depth = max(max_depth, current_depth)
        
        if node.right:
            stack.append((node.right, current_depth + 1))
        if node.left:
            stack.append((node.left, current_depth + 1))
    
    return max_depth
```

#### Approach

This solution uses depth-first search with a stack to traverse the tree:

1. Use a stack to track nodes and their depths
2. Process nodes in a depth-first manner
3. Keep track of the maximum depth seen so far
4. The final maximum depth is the answer

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each node is processed exactly once, resulting in O(n) time complexity.

##### Space Complexity: `O(h)`

The space required is proportional to the height of the tree, which in the worst case could be O(n) for a completely unbalanced tree, or O(log n) for a balanced tree.

#### Key Insights

- Converts the recursive solution to an iterative one using a stack
- Avoids function call overhead
- Needs to explicitly track the depth of each node

## Comparison of Solutions

### Time Complexity

- **Recursive DFS**: `O(n)` - Visits each node once
- **Iterative BFS**: `O(n)` - Visits each node once
- **Iterative DFS**: `O(n)` - Visits each node once

### Space Complexity

- **Recursive DFS**: `O(h)` - Where h is the height of the tree
- **Iterative BFS**: `O(w)` - Where w is the maximum width of the tree
- **Iterative DFS**: `O(h)` - Where h is the height of the tree

### Trade-offs

- The recursive solution is the most elegant and concise, but may cause stack overflow for very deep trees
- BFS uses more memory for wide trees but less for tall, skinny trees
- Iterative DFS avoids recursion overhead but is slightly more complex to implement

### When to Use Each

- **Recursive DFS**: When code simplicity is valued and the tree is not extremely deep
- **Iterative BFS**: When the tree might be very deep but not very wide
- **Iterative DFS**: When you want to avoid recursion but still approach the problem depth-first

### Optimization Notes

- The choice between these approaches often depends more on space constraints than time, as all have O(n) time complexity
- For very deep trees, the iterative approaches help avoid stack overflow errors
- For interview settings, the recursive solution is typically preferred for its elegance and readability

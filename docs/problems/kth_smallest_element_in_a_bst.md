# [Kth Smallest Element in a BST](https://leetcode.com/problems/kth-smallest-element-in-a-bst/)

**Medium** | **25 minutes** | **Tree, Depth-First Search, Binary Search Tree**

**Pattern:** [Tree Traversal](../patterns/tree/intuition.md)

**Practice:** [`practice/kth_smallest_element_in_a_bst/solution.py`](../../practice/kth_smallest_element_in_a_bst/solution.py)

Given the `root` of a binary search tree, and an integer `k`, return the `kth` smallest value (1-indexed) of all the values of the nodes in the tree.

## Examples

### Example 1

![BST Tree 1](assets/kth_smallest_element_in_a_bst_example1.jpg)

**Input:** `root = [3,1,4,null,2]`, `k = 1`

**Output:** `1`

### Example 2

![BST Tree 2](assets/kth_smallest_element_in_a_bst_example2.jpg)

**Input:** `root = [5,3,6,2,4,null,null,1]`, `k = 3`

**Output:** `3`

## Constraints

- The number of nodes in the tree is `n`.
- `1 <= k <= n <= 10^4`
- `0 <= Node.val <= 10^4`

## Follow-up

If the BST is modified often (i.e., we can do insert and delete operations) and you need to find the kth smallest frequently, how would you optimize?

## Solutions

### Recursive In-Order Traversal

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from typing import List, Optional


class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        def inorder(node: Optional[TreeNode]) -> List[int]:
            if not node:
                return []
            return inorder(node.left) + [node.val] + inorder(node.right)

        sorted_values = inorder(root)
        return sorted_values[k - 1]
```

#### Approach

This solution performs a complete recursive in-order traversal to collect all values in sorted order, then returns the kth element.

1. Recurse into the left subtree, then visit the node, then recurse into the right subtree, accumulating values in a list.
2. Because an in-order walk of a BST yields values in ascending order, the resulting list is sorted.
3. Return the value at index `k - 1`, converting the 1-indexed `k` to a 0-indexed lookup.

The approach is conceptually simple but processes every node regardless of how small `k` is.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

The traversal always visits all `n` nodes regardless of `k`, since it builds the complete sorted list before indexing into it.

##### Space Complexity: `O(n)`

The list holds all `n` node values, and the recursion stack adds `O(H)` for the tree height, which is dominated by the `O(n)` list.

#### Key Insights

- The BST property guarantees that an in-order traversal produces a sorted sequence, removing the need for an explicit sort.
- Concatenating lists at every node (`inorder(left) + [val] + inorder(right)`) is the most readable form but creates many intermediate lists, making it the least efficient of the three approaches.
- The `k - 1` index conversion is the single place where the 1-indexed problem statement meets 0-indexed Python lists.

#### Walkthrough

Let us trace the Recursive In-Order Traversal on Example 1: `root = [3,1,4,null,2]`, `k = 1`. The tree looks like this: the root is `3`, its left child is `1`, its right child is `4`, and node `1` has a right child `2`.

```
      3
     / \
    1   4
     \
      2
```

The key idea: `inorder(node)` returns `inorder(node.left) + [node.val] + inorder(node.right)`. Each call must finish its left subtree before it can hand back its own value. We show the call tree, with each call returning a list that combines on the way back up.

```
inorder(3)
├─ inorder(1)                  # 3's left subtree
│  ├─ inorder(None)  -> []     # 1 has no left child
│  ├─ value [1]
│  └─ inorder(2)               # 1's right child
│     ├─ inorder(None) -> []   # 2 has no left child
│     ├─ value [2]
│     └─ inorder(None) -> []   # 2 has no right child
│     => [] + [2] + []  = [2]
│  => [] + [1] + [2]    = [1, 2]
├─ value [3]
└─ inorder(4)                  # 3's right subtree
   ├─ inorder(None) -> []      # 4 has no left child
   ├─ value [4]
   └─ inorder(None) -> []      # 4 has no right child
   => [] + [4] + []   = [4]
=> [1, 2] + [3] + [4]  = [1, 2, 3, 4]
```

So `sorted_values = [1, 2, 3, 4]`, the node values in ascending order. With `k = 1`, the code returns `sorted_values[k - 1]`, which is `sorted_values[0]`, giving `1`. This matches the expected Output of `1`.

### Iterative In-Order Traversal

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from typing import List, Optional


class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        stack: List[TreeNode] = []
        current = root
        count = 0

        while current or stack:
            # Walk to the leftmost unvisited node
            while current:
                stack.append(current)
                current = current.left

            # Visit the smallest unprocessed node
            current = stack.pop()
            count += 1

            if count == k:
                return current.val

            # Continue into the right subtree
            current = current.right

        return -1  # Unreachable for valid inputs
```

#### Approach

This solution uses an iterative in-order traversal with early termination.

1. Use an explicit stack to simulate the recursion: push nodes while descending left, so the top of the stack is always the smallest unvisited value.
2. Pop a node to "visit" it and increment a running counter.
3. When the counter reaches `k`, the popped node holds the answer, so return its value immediately.
4. Otherwise move into the popped node's right subtree and repeat.

Because the traversal stops the moment the kth node is visited, it never explores the rest of the tree.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(H + k)` where `H` is the height of the tree

The work is the descent down the leftmost path plus `k` visits. For a balanced BST this is `O(log n + k)`; for a skewed BST it degrades to `O(n)`. Early termination is decisive when `k` is small.

##### Space Complexity: `O(H)`

The stack holds at most one path from root to leaf, which is `O(log n)` for a balanced tree and `O(n)` for a skewed tree.

#### Key Insights

- Replacing recursion with an explicit stack makes early termination natural: there is no recursion to unwind once the answer is found.
- The inner `while current` loop is what guarantees the next popped node is the smallest unprocessed value.
- This is the best general-purpose choice: it keeps the simple in-order logic while avoiding the full traversal cost of the recursive version.

### Morris Traversal

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from typing import Optional


class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        current = root
        count = 0

        while current:
            if not current.left:
                # No left child, process current node
                count += 1
                if count == k:
                    return current.val
                current = current.right
            else:
                # Find inorder predecessor
                predecessor = current.left
                while predecessor.right and predecessor.right != current:
                    predecessor = predecessor.right

                if not predecessor.right:
                    # Make current the right child of predecessor
                    predecessor.right = current
                    current = current.left
                else:
                    # Revert the changes - process current node
                    predecessor.right = None
                    count += 1
                    if count == k:
                        return current.val
                    current = current.right

        return -1
```

#### Approach

This solution uses Morris traversal to perform an in-order walk with `O(1)` auxiliary space.

1. For a node with no left child, visit it (increment the counter) and move right.
2. For a node with a left child, find its in-order predecessor: the rightmost node of the left subtree.
3. If that predecessor has no right link yet, create a temporary link back to the current node and descend left.
4. If the predecessor already links back to the current node, the left subtree is done: remove the temporary link, visit the current node, and move right.
5. Return as soon as the visit counter reaches `k`.

The temporary links let the traversal find its way back up the tree without a stack, and removing them restores the original structure.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each edge is traversed at most a constant number of times (once to create the temporary link, once to remove it), so the total work is linear in the number of nodes.

##### Space Complexity: `O(1)`

No stack or output list is used; the only extra storage is a constant number of pointers, with the tree itself temporarily rewired and then restored.

#### Key Insights

- Morris traversal trades pointer mutation for space: it threads predecessor-to-successor links instead of storing the path on a stack.
- Every temporary link must be removed once the left subtree is exhausted; otherwise the tree is left corrupted with cycles.
- Despite the `O(1)` space, each node is still visited, so it does not beat the iterative approach's `O(H + k)` time when `k` is small.

## Comparison of Solutions

### Time Complexity

- **Recursive In-Order Traversal**: `O(n)` - Always processes all nodes
- **Iterative In-Order Traversal**: `O(H + k)` - Optimal for small k values
- **Morris Traversal**: `O(n)` - Processes all nodes up to kth

### Space Complexity

- **Recursive In-Order Traversal**: `O(n)` - Stores all values plus recursion stack
- **Iterative In-Order Traversal**: `O(H)` - Stack space proportional to height
- **Morris Traversal**: `O(1)` - Constant space complexity

### Trade-offs

- **Recursive In-Order Traversal**: Simple implementation complexity with excellent code readability, but no early termination and poor space efficiency since it always builds the full sorted list. Its practical performance is good for learning.
- **Iterative In-Order Traversal**: Medium implementation complexity with good code readability, supports early termination, and offers good space efficiency. Its practical performance is best for most cases.
- **Morris Traversal**: Complex implementation with poor code readability, but supports early termination and delivers excellent space efficiency. Its practical performance is best when space is critical.

### When to Use Each

- **Recursive In-Order Traversal**: When learning BST concepts or when code simplicity is paramount
- **Iterative In-Order Traversal**: Best general-purpose solution for interviews and production code
- **Morris Traversal**: When space constraints are critical and implementation complexity is acceptable

### Optimization Notes

- **Recommended solution**: Iterative In-Order Traversal is the best general-purpose choice, leveraging the BST property that in-order traversal yields values in sorted order and stopping as soon as the kth node is reached.
- **Key implementation detail**: Early termination is the decisive optimization. The Iterative In-Order Traversal and Morris Traversal approaches halt at the kth element instead of processing the entire tree, while Recursive In-Order Traversal always builds the full sorted list. Morris Traversal achieves optimal `O(1)` space by temporarily rewiring tree links, at the cost of implementation complexity.
- **Pitfall**: Morris traversal mutates the tree during traversal and must restore every link it creates; failing to revert these links leaves the tree corrupted. For interviews, start with Iterative In-Order Traversal and mention Morris Traversal when asked about space optimization.
- **Follow-up handling**: For frequently modified BSTs with repeated queries, augment nodes with subtree size information to support `O(log n)` queries.

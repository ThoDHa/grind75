# [Serialize and Deserialize Binary Tree](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/)

**Hard** | **45 minutes** | **Tree, Design, String, Binary Tree**

**Pattern:** [Tree Traversal](../patterns/tree/intuition.md)

**Practice:** [`practice/serialize_and_deserialize_binary_tree/solution.py`](https://github.com/ThoDHa/grind75/blob/main/practice/serialize_and_deserialize_binary_tree/solution.py)

Serialization is the process of converting a data structure or object into a sequence of bits so that it can be stored in a file or memory buffer, or transmitted across a network connection link to be reconstructed later in the same or another computer environment.

Design an algorithm to serialize and deserialize a binary tree. There is no restriction on how your serialization/deserialization algorithm should work. You just need to ensure that a binary tree can be serialized to a string and this string can be deserialized to the original tree structure.

**Clarification:** The input/output format is the same as how LeetCode serializes a binary tree. You do not necessarily need to follow this format, so please be creative and come up with different approaches yourself.

## Examples

### Example 1

**Input:** root = `[1,2,3,null,null,4,5]`

**Output:** `[1,2,3,null,null,4,5]`

### Example 2

**Input:** root = `[]`

**Output:** `[]`

## Constraints

- The number of nodes in the tree is in the range `[0, 10^4]`.
- `-1000 <= Node.val <= 1000`

## Solutions

### Preorder DFS with Null Markers

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Codec:
    def serialize(self, root):
        """Encodes a tree to a single string using preorder traversal"""
        def preorder(node):
            if not node:
                vals.append("null")
            else:
                vals.append(str(node.val))
                preorder(node.left)
                preorder(node.right)

        vals = []
        preorder(root)
        return ','.join(vals)

    def deserialize(self, data):
        """Decodes string back to tree using preorder reconstruction"""
        def build_tree():
            val = next(vals_iter)
            if val == "null":
                return None

            node = TreeNode(int(val))
            node.left = build_tree()
            node.right = build_tree()
            return node

        vals_iter = iter(data.split(','))
        return build_tree()
```

#### Approach

This solution uses **preorder traversal (root → left → right)** for serialization with explicit null markers. The key insight is that preorder traversal with null placeholders provides enough information to uniquely reconstruct the tree. Deserialization uses recursive reconstruction following the same preorder pattern.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)` for both operations

Serialization visits each node once, deserialization processes each serialized value once.

##### Space Complexity: `O(n)` for serialization, `O(h)` for deserialization

Serialization stores all node values. Deserialization uses recursion stack proportional to tree height.

#### Key Insights

- Preorder traversal with explicit null markers captures both the values and the shape of the tree, so the original structure can be reconstructed uniquely without a second traversal.
- Deserialization consumes tokens through a single shared iterator, so each recursive call advances the cursor exactly once and the left subtree is fully built before the right.
- Null markers are mandatory for a general binary tree; without them, distinct trees can produce the same value sequence and become indistinguishable.

### Level-Order BFS

```python
from collections import deque

class Codec:
    def serialize(self, root):
        """Encodes tree using level-order traversal (BFS)"""
        if not root:
            return ""

        queue = deque([root])
        result = []

        while queue:
            node = queue.popleft()
            if node:
                result.append(str(node.val))
                queue.append(node.left)
                queue.append(node.right)
            else:
                result.append("null")

        return ','.join(result)

    def deserialize(self, data):
        """Decodes string back to tree using level-order reconstruction"""
        if not data:
            return None

        values = data.split(',')
        root = TreeNode(int(values[0]))
        queue = deque([root])
        index = 1

        while queue and index < len(values):
            node = queue.popleft()

            # Process left child
            if values[index] != "null":
                node.left = TreeNode(int(values[index]))
                queue.append(node.left)
            index += 1

            # Process right child
            if index < len(values) and values[index] != "null":
                node.right = TreeNode(int(values[index]))
                queue.append(node.right)
            index += 1

        return root
```

#### Approach

This solution uses **level-order traversal (BFS)** which processes nodes level by level from left to right. This approach is more intuitive for many people as it matches the way trees are often visualized. The serialization creates a queue-like structure that can be directly reconstructed.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)` for both operations

Each node is processed exactly once in both serialization and deserialization.

##### Space Complexity: `O(w)` where w is maximum width of tree

The queue can contain at most all nodes at the widest level of the tree.

#### Key Insights

- A breadth-first ordering matches LeetCode's own level-order representation, making the serialized string easy to read and reason about.
- Reconstruction pairs each dequeued node with the next two tokens as its children, so an explicit queue replaces the recursion used by the DFS approaches.
- Using an iterative queue avoids deep recursion, so very deep or skewed trees will not overflow the call stack.

### Postorder DFS with Null Markers

```python
class Codec:
    def serialize(self, root):
        """Encodes a tree to a single string using postorder traversal"""
        def postorder(node):
            if not node:
                vals.append("null")
            else:
                postorder(node.left)
                postorder(node.right)
                vals.append(str(node.val))

        vals = []
        postorder(root)
        return ','.join(vals)

    def deserialize(self, data):
        """Decodes string back to tree by consuming postorder from the end"""
        def build_tree():
            val = vals.pop()
            if val == "null":
                return None

            node = TreeNode(int(val))
            # Postorder is left, right, root; consumed from the end the
            # order reverses, so build the right subtree before the left
            node.right = build_tree()
            node.left = build_tree()
            return node

        vals = data.split(',')
        return build_tree()
```

#### Approach

This solution uses **postorder traversal (left → right → root)** for serialization with explicit null markers. Because the root is written last, the root token sits at the very end of the serialized string. Deserialization consumes tokens from the **end** of the list, which reverses the traversal order to root → right → left, so the right subtree must be built before the left. The null markers tell the recursion exactly where each subtree ends, allowing any general binary tree to be reconstructed uniquely.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)` for both operations

Serialization visits each node once, deserialization processes each serialized value once.

##### Space Complexity: `O(n)` for serialization, `O(h)` for deserialization

Serialization stores all node values plus null markers. Deserialization uses a recursion stack proportional to tree height.

#### Key Insights

- Writing the root last places its token at the end of the string, so deserialization reads the token list from the back, which reverses the traversal to root then right then left.
- Because the order reverses, the right subtree must be built before the left; swapping them is the most common implementation mistake here.
- The same null-marker technique that works for preorder also works for postorder, demonstrating that the choice of traversal is flexible as long as boundaries are marked.

## Comparison of Solutions

### Time Complexity

- **Preorder DFS with Null Markers**: `O(n)` - Linear time for both operations
- **Level-Order BFS**: `O(n)` - Linear time with queue operations
- **Postorder DFS with Null Markers**: `O(n)` - Linear time for both operations

### Space Complexity

- **Preorder DFS with Null Markers**: `O(n)` serialized size, `O(h)` reconstruction stack
- **Level-Order BFS**: `O(w)` for queue, where w is maximum tree width
- **Postorder DFS with Null Markers**: `O(n)` serialized size, `O(h)` reconstruction stack

### Trade-offs

- **Preorder DFS with Null Markers**: Implementation complexity is medium with good intuitive understanding. The serialized size is larger because it includes null markers, but reconstruction uses simple recursive logic that is stack-based during reconstruction and easy to debug.
- **Level-Order BFS**: Implementation complexity is medium with excellent intuitive understanding, matching how trees are commonly visualized. The serialized size is larger because it includes null markers, reconstruction is queue-based iterative logic, memory during reconstruction is queue-based, and it is easy to debug.
- **Postorder DFS with Null Markers**: Implementation complexity is medium. The serialized size is comparable to the preorder approach since it also stores null markers. The one subtlety is that deserialization consumes tokens from the end of the list and builds the right subtree before the left, which is easy to get wrong but straightforward once understood.

### When to Use Each

- **Preorder DFS with Null Markers**: Best general-purpose solution for interviews and production, with a good balance of simplicity and efficiency
- **Level-Order BFS**: When you want intuitive level-by-level processing or when working with very deep trees (avoids deep recursion)
- **Postorder DFS with Null Markers**: When you want a bottom-up traversal, or to demonstrate that the same null-marker technique works in postorder by reading the token list from the end

### Optimization Notes

- The **Preorder DFS with Null Markers** solution is the recommended choice for interviews and production: preorder traversal with null placeholders provides sufficient information for unique reconstruction without requiring an inorder traversal, and the recursive reconstruction is simple to implement and debug.
- Key implementation detail: serialization and deserialization must follow the same preorder order (root, then left, then right), and the null markers are what allow the recursive `build_tree` to know exactly where each subtree ends.
- The **Level-Order BFS** trades recursion (stack space) for an explicit queue (heap space) and avoids deep recursion, making it the better choice for very deep trees that could otherwise overflow the call stack.
- The **Postorder DFS with Null Markers** solution shows the same null-marker idea applied bottom-up. Because the root is serialized last, deserialization must consume the token list from the end and build the right subtree before the left. A tempting but incorrect shortcut is to drop the null markers and reconstruct using BST-style value bounds (`min < val < max`); that only works for binary search trees and silently misplaces nodes in a general binary tree, so explicit null markers are required for correctness here.
- Common pitfall: forgetting that postorder deserialization reverses direction (right before left) when reading from the end. Edge cases such as empty trees, single nodes, and highly unbalanced trees must be tested for each approach.

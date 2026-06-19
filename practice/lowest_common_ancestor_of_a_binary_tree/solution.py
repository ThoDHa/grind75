"""Lowest Common Ancestor of a Binary Tree — https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/

Write-up & approaches: ../../docs/problems/lowest_common_ancestor_of_a_binary_tree.md

Given a binary tree and two nodes `p` and `q`, return their lowest common
ancestor: the deepest node that has both `p` and `q` as descendants (a node may
be a descendant of itself).

  uv run python lowest_common_ancestor_of_a_binary_tree/solution.py   # debug one case (see CASE below)
  uv run pytest lowest_common_ancestor_of_a_binary_tree/              # run the test sets
"""

from typing import Optional

from harness import NotSolved, TreeNode, build_tree, pick_case


class Solution:
    def lowestCommonAncestor(
        self, root: "TreeNode", p: "TreeNode", q: "TreeNode"
    ) -> "TreeNode":
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        raise NotSolved


def _find(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    # Locate the TreeNode whose .val == val via a small DFS so we can pass real
    # node references (not values) into lowestCommonAncestor.
    if root is None:
        return None
    if root.val == val:
        return root
    return _find(root.left, val) or _find(root.right, val)


if __name__ == "__main__":
    # Debug playground: set a breakpoint in lowestCommonAncestor above, then run
    # this file. The case stores the tree as a level-order array plus p/q values;
    # we marshal it to TreeNodes here, the same way the test does.
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    tree_array, p_val, q_val = case["args"]
    root = build_tree(tree_array)
    p_node = _find(root, p_val)
    q_node = _find(root, q_val)
    result = Solution().lowestCommonAncestor(root, p_node, q_node)
    got = result.val if result is not None else None
    print(f"case {case['id']}: tree = {tree_array}, p = {p_val}, q = {q_val}")
    print(f"expected: {case['expected']}")
    print(f"got:      {got}")

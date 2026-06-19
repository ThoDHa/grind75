# [Middle of the Linked List](https://leetcode.com/problems/middle-of-the-linked-list/)

**Easy** | **10 minutes** | **Linked List, Two Pointers**

**Pattern:** [Two Pointers](../patterns/two_pointers/intuition.md)

**Practice:** [`practice/middle_of_the_linked_list/solution.py`](../../practice/middle_of_the_linked_list/solution.py)

Given the `head` of a singly linked list, return the middle node of the linked list.

If there are two middle nodes, return the second middle node.

## Examples

### Example 1

![Middle of the Linked List Example 1](assets/middle_of_the_linked_list_example1.jpg)

**Input:** `head = [1,2,3,4,5]`

**Output:** `[3,4,5]`

**Explanation:** The middle node of the list is node 3.

### Example 2

![Middle of the Linked List Example 2](assets/middle_of_the_linked_list_example2.jpg)

**Input:** `head = [1,2,3,4,5,6]`

**Output:** `[4,5,6]`

**Explanation:** Since the list has two middle nodes with values 3 and 4, we return the second one.

## Constraints

- The number of nodes in the list is in the range `[1, 100]`.
- `1 <= Node.val <= 100`

## Solutions

### Count and Find

```python
class Solution:
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        count = 0
        current = head
        while current:
            count += 1
            current = current.next

        middle = count // 2
        current = head
        for _ in range(middle):
            current = current.next
        return current
```

#### Approach

The most direct way to find the middle is to first learn how long the list is,
then walk back to the midpoint. This takes two passes:

1. First pass: traverse the entire list, counting the nodes into `count`.
2. Compute the middle index as `count // 2`.
3. Second pass: start again from `head` and advance `middle` steps to land on the
   target node.

For an odd-length list of size `n`, `count // 2` lands exactly on the central
node. For an even-length list, integer division biases toward the higher index,
so the second of the two middle nodes is returned, which matches the required
behavior.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

We traverse the list once to count and once more to reach the middle, giving
`2n` steps, which is `O(n)`.

##### Space Complexity: `O(1)`

Only a counter and a pointer are kept, regardless of the input size.

#### Key Insights

- Counting first removes all guesswork: once the length is known, the midpoint is
  a plain index calculation.
- `count // 2` cleanly yields the second middle node for even-length lists, so no
  special casing is needed.
- The approach is easy to reason about, but it reads the list twice.

### Fast and Slow Pointers

```python
class Solution:
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow
```

#### Approach

This solution uses the fast-and-slow pointer technique (also known as the
"tortoise and hare"). Both pointers start at `head`:

1. Advance `slow` by one node and `fast` by two nodes on each iteration.
2. Continue while `fast` and `fast.next` are both non-null, so `fast` always has
   two nodes available to step over.
3. When `fast` runs off the end, `slow` has covered exactly half the distance and
   sits on the middle node.

Because `fast` travels at twice the speed of `slow`, the position of `slow` when
`fast` finishes is the midpoint. For even-length lists, the loop condition stops
`fast` one step later, which leaves `slow` on the second of the two middle nodes.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

The list is traversed a single time; `fast` covers the full list while `slow`
covers half, so the total work is `O(n)`.

##### Space Complexity: `O(1)`

Only the two pointers are used, independent of the input size.

#### Key Insights

- A single pass replaces the count-then-walk pattern: the relative speed of the
  two pointers encodes the midpoint directly.
- The loop guard `fast and fast.next` is what produces the second middle node for
  even-length lists without any extra branching.
- This pattern generalizes to many linked-list problems, including cycle
  detection (Floyd's algorithm) and finding the start of a cycle.

## Comparison of Solutions

### Time Complexity

- **Count and Find**: `O(n)` - two passes through the list.
- **Fast and Slow Pointers**: `O(n)` - one pass through the list.

### Space Complexity

- **Count and Find**: `O(1)` - only a counter and a pointer.
- **Fast and Slow Pointers**: `O(1)` - only two pointers.

### Trade-offs

- Both approaches share the same asymptotic bounds, but Fast and Slow Pointers
  does half the traversal work of Count and Find because it never re-reads the
  list from the start.
- Count and Find is often more approachable for those new to linked lists, since
  it relies on a familiar count-then-index pattern rather than a two-speed walk.

### When to Use Each

- **Fast and Slow Pointers**: The right call in most situations, given its
  single-pass efficiency and reuse across other linked-list problems (Recommended).
- **Count and Find**: A reasonable choice when clarity for a beginner audience
  matters more than shaving a pass off the traversal.

### Optimization Notes

- The Fast and Slow Pointers technique is a classic tool for linked-list problems
  and underlies Floyd's cycle-detection algorithm.
- Moving two pointers at different speeds reveals positional relationships, such
  as the midpoint or a cycle entry point, without knowing the length in advance.

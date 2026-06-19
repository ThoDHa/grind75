# [Merge k Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/)

**Hard** | **45 minutes** | **Linked List, Divide and Conquer, Heap (Priority Queue), Merge Sort**

**Pattern:** [Heap / Priority Queue](../patterns/heap/intuition.md), [K-Way Merge](../patterns/k_way_merge/intuition.md)

**Practice:** [`practice/merge_k_sorted_lists/solution.py`](https://github.com/ThoDHa/grind75/blob/main/practice/merge_k_sorted_lists/solution.py)

You are given an array of k linked-lists lists, each linked-list is sorted in ascending order.

Merge all the linked-lists into one sorted linked-list and return it.

## Examples

### Example 1

**Input:** lists = `[[1,4,5],[1,3,4],[2,6]]`

**Output:** `[1,1,2,3,4,4,5,6]`

**Explanation:** The linked-lists are:

```
[
  1->4->5,
  1->3->4,
  2->6
]
```

merging them into one sorted list:
`1->1->2->3->4->4->5->6`

### Example 2

**Input:** lists = `[]`

**Output:** `[]`

### Example 3

**Input:** lists = `[[]]`

**Output:** `[]`

## Constraints

- `k == lists.length`
- `0 <= k <= 10^4`
- `0 <= lists[i].length <= 500`
- `-10^4 <= lists[i][j] <= 10^4`
- `lists[i]` is sorted in **ascending** order.
- The sum of `lists[i].length` will not exceed `10^4`.

## Solutions

### Collect and Sort

```python
class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        """
        Brute force: collect all values, sort, then build new list
        """
        # Collect all values
        values = []
        for head in lists:
            current = head
            while current:
                values.append(current.val)
                current = current.next

        # Sort values
        values.sort()

        # Build new linked list
        dummy = ListNode(0)
        current = dummy

        for val in values:
            current.next = ListNode(val)
            current = current.next

        return dummy.next
```

#### Approach

This **brute force solution** extracts all values into an array, sorts them, then constructs a new linked list. While straightforward, it doesn't leverage the fact that individual lists are already sorted.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(N log N)`

Dominated by the sorting step, where N is the total number of nodes.

##### Space Complexity: `O(N)`

Stores all values in an array before reconstruction.

#### Key Insights

- The merge is reduced to a single global sort, which makes correctness trivial but discards the sorted structure of each input list.
- The dummy head node simplifies construction of the result list by removing the special case for the first appended node.
- This is the natural first idea, useful as a baseline, but it is the only approach whose time bound depends on `N log N` rather than `N log k`.

### Sequential Merge

```python
class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        """
        Sequential merge - merge lists one by one
        """
        if not lists:
            return None

        def merge_two_lists(l1, l2):
            """Merge two sorted linked lists"""
            dummy = ListNode(0)
            current = dummy

            while l1 and l2:
                if l1.val <= l2.val:
                    current.next = l1
                    l1 = l1.next
                else:
                    current.next = l2
                    l2 = l2.next
                current = current.next

            current.next = l1 or l2
            return dummy.next

        # Sequentially merge all lists
        result = lists[0]
        for i in range(1, len(lists)):
            result = merge_two_lists(result, lists[i])

        return result
```

#### Approach

This solution **sequentially merges** each list with the accumulated result. While simple to implement, it's less efficient because earlier nodes are processed multiple times as the result list grows.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(N × k)`

The first merge processes the first list, the second merge processes the first two lists, etc. This leads to quadratic behavior in the number of lists.

##### Space Complexity: `O(1)`

Uses constant extra space, only manipulating pointers.

#### Key Insights

- Reusing the standard two-list merge keeps the implementation small, but folding the lists in a left-to-right line means early nodes are revisited on every subsequent merge.
- The accumulating result grows toward length `N`, so the i-th merge costs proportional to the running total, producing the `O(N × k)` behavior.
- Pairing the lists instead of accumulating them linearly is what turns this into the optimal divide and conquer approach below.

### Min-Heap

```python
import heapq

class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        """
        Min-heap approach to always select the smallest available node
        """
        if not lists:
            return None

        # Initialize heap with the first node from each non-empty list
        heap = []
        for i, head in enumerate(lists):
            if head:
                heapq.heappush(heap, (head.val, i, head))

        dummy = ListNode(0)
        current = dummy

        while heap:
            # Get the node with minimum value
            val, list_idx, node = heapq.heappop(heap)

            # Add to result
            current.next = node
            current = current.next

            # Add the next node from the same list to heap
            if node.next:
                heapq.heappush(heap, (node.next.val, list_idx, node.next))

        return dummy.next
```

#### Approach

This solution uses a **min-heap (priority queue)** to always select the node with the smallest value from all available list heads. This approach maintains k active candidates and efficiently finds the minimum at each step.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(N log k)`

Each of the N nodes is pushed and popped from the heap once, and heap operations take O(log k) time.

##### Space Complexity: `O(k)`

The heap contains at most k nodes (one from each list) at any time.

#### Key Insights

- The heap entry stores `(value, list_index, node)` so that the list index breaks ties and the heap never has to compare `ListNode` objects, which are not orderable.
- Only one candidate per list lives in the heap at a time, so the heap size stays bounded by `k` even as `N` nodes flow through it.
- This generalizes the greedy "scan all heads" idea by replacing the linear minimum search with an `O(log k)` heap pop, which is the key to handling very large `k`.

### Divide and Conquer

```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        """
        Divide and conquer approach - merge pairs recursively
        """
        if not lists:
            return None

        def merge_two_lists(l1, l2):
            """Merge two sorted linked lists"""
            dummy = ListNode(0)
            current = dummy

            while l1 and l2:
                if l1.val <= l2.val:
                    current.next = l1
                    l1 = l1.next
                else:
                    current.next = l2
                    l2 = l2.next
                current = current.next

            # Attach remaining nodes
            current.next = l1 or l2
            return dummy.next

        # Divide and conquer
        while len(lists) > 1:
            merged_lists = []

            # Merge pairs of lists
            for i in range(0, len(lists), 2):
                l1 = lists[i]
                l2 = lists[i + 1] if i + 1 < len(lists) else None
                merged_lists.append(merge_two_lists(l1, l2))

            lists = merged_lists

        return lists[0] if lists else None
```

#### Approach

This solution uses **divide and conquer** by repeatedly merging pairs of lists until only one remains. The key insight is that merging k lists can be reduced to log(k) levels of pairwise merges, which is more efficient than sequential merging.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(N log k)`

Where N is the total number of nodes and k is the number of lists. Each node is processed log(k) times through the merging levels.

##### Space Complexity: `O(1)` iterative, `O(log k)` if counting merge_two_lists recursion

The main algorithm is iterative with constant space, but merge_two_lists could use recursion stack.

#### Key Insights

- Merging in pairs halves the number of lists each round, so after `log k` rounds a single list remains, and every node participates in exactly `log k` merges.
- Guarding the second list with `lists[i + 1] if i + 1 < len(lists) else None` cleanly handles an odd count by merging the leftover list against `None`.
- This matches the heap approach at `O(N log k)` time while keeping iterative `O(1)` extra space, making it the strongest all-around choice.

## Comparison of Solutions

### Time Complexity

- **Collect and Sort**: `O(N log N)` - May be worse if k << N
- **Sequential Merge**: `O(N × k)` - Quadratic in number of lists
- **Min-Heap**: `O(N log k)` - Same optimal complexity
- **Divide and Conquer**: `O(N log k)` - Optimal for this problem

### Space Complexity

- **Collect and Sort**: `O(N)` - Stores all values
- **Sequential Merge**: `O(1)` - Constant space
- **Min-Heap**: `O(k)` - Heap stores k elements
- **Divide and Conquer**: `O(1)` iterative approach

### Trade-offs

- **Collect and Sort**: Time efficiency depends on k versus N, and space efficiency is poor. Implementation is simple, but it does not leverage the already-sorted property of the input lists. This approach is discouraged in interviews.
- **Sequential Merge**: Poor time efficiency but excellent space efficiency. Implementation is simple and it does leverage the sorted property. Acceptable as an interview answer.
- **Min-Heap**: Optimal time efficiency with good space efficiency. Implementation complexity is medium and it leverages the sorted property. This approach is well-regarded in interviews.
- **Divide and Conquer**: Optimal time efficiency with excellent space efficiency. Implementation complexity is medium and it leverages the sorted property. This is the most preferred solution in interviews.

### When to Use Each

- **Collect and Sort**: Generally not recommended unless constraints are very small
- **Sequential Merge**: When simplicity is paramount and k is small
- **Min-Heap**: When you want to demonstrate knowledge of heap data structures or when k is very large
- **Divide and Conquer**: Best overall solution for interviews and production - optimal time and space

### Optimization Notes

- The **Divide and Conquer** solution is the recommended approach: it achieves optimal `O(N log k)` time with `O(1)` iterative space by reducing k lists to `log(k)` levels of pairwise merges. The **Min-Heap** approach matches the same time complexity and is preferred when k is very large.
- The key implementation detail is the two-list merge helper, which uses a dummy head node to simplify pointer manipulation and attaches the remaining list with `current.next = l1 or l2` once one list is exhausted.
- A common pitfall in the divide and conquer approach is mishandling the odd list out when pairing: guard the second list with `lists[i + 1] if i + 1 < len(lists) else None` so the final unpaired list merges against `None` cleanly.
- The difference between `O(N log k)` and `O(N × k)` becomes significant as k grows, so leveraging the already-sorted property of each input list is crucial for an optimal solution.

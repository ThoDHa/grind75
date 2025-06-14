# [Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/)

Easy - 20 minutes - Linked List, Two Pointers

Given `head`, the head of a linked list, determine if the linked list has a cycle in it.

There is a cycle in a linked list if there is some node in the list that can be reached again by continuously following the `next` pointer. Internally, `pos` is used to denote the index of the node that tail's `next` pointer is connected to. **Note that `pos` is not passed as a parameter**.

Return `true` if there is a cycle in the linked list. Otherwise, return `false`.

## Examples

### Example 1

![Linked List Cycle Example 1](assets/linked_list_cycle_example1.png)

**Input:** `head = [3,2,0,-4]`, `pos = 1`

**Output:** `true`

**Explanation:** There is a cycle in the linked list, where the tail connects to the 1st node (0-indexed).

### Example 2

![Linked List Cycle Example 2](assets/linked_list_cycle_example2.png)

**Input:** `head = [1,2]`, `pos = 0`

**Output:** `true`

**Explanation:** There is a cycle in the linked list, where the tail connects to the 0th node.

### Example 3

![Linked List Cycle Example 3](assets/linked_list_cycle_example3.png)

**Input:** `head = [1]`, `pos = -1`

**Output:** `false`

**Explanation:** There is no cycle in the linked list.

## Constraints

- The number of the nodes in the list is in the range `[0, 10^4]`.
- `-10^5 <= Node.val <= 10^5`
- `pos` is `-1` or a valid index in the linked-list.

## Solutions

### Solution 1: Hash Set Approach

```python
def hasCycle(self, head: Optional[ListNode]) -> bool:
    # Set to store visited nodes
    seen = set()
    
    # Traverse the list
    while head:
        # If we've seen this node before, we have a cycle
        if head in seen:
            return True
        # Add current node to the set
        seen.add(head)
        # Move to the next node
        head = head.next
    
    # If we reach the end, there's no cycle
    return False
```

#### Approach

This solution uses a hash set to keep track of nodes we've already visited. As we traverse the linked list, we check if we've seen the current node before. If we have, there must be a cycle. If we reach the end of the list (a null pointer), then there's no cycle.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Where `n` is the number of nodes in the linked list. In the worst case, we might need to visit all nodes once.

##### Space Complexity: `O(n)`

We store each node in the hash set, which in the worst case would contain all `n` nodes.

#### Key Insights

- Hash set provides `O(1)` lookups to quickly check if a node was seen before
- Simple implementation that's easy to understand
- The space complexity is proportional to the size of the list

### Solution 2: Floyd's Cycle-Finding Algorithm (Two Pointers)

```python
def hasCycle(self, head: Optional[ListNode]) -> bool:
    # Initialize slow and fast pointers
    slow = head
    fast = head
    
    # Traverse the list with different speeds
    while slow and fast and fast.next:
        slow = slow.next          # Move slow pointer by 1 step
        fast = fast.next.next     # Move fast pointer by 2 steps
        
        # If they meet, there's a cycle
        if slow == fast:
            return True
    
    # If fast reaches the end, there's no cycle
    return False
```

#### Approach

This solution implements Floyd's Cycle-Finding Algorithm, also known as the "tortoise and hare" algorithm. We use two pointers that move at different speeds: a slow pointer that moves one step at a time and a fast pointer that moves two steps at a time. If there's a cycle, the fast pointer will eventually catch up to the slow pointer. If there's no cycle, the fast pointer will reach the end of the list.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Where `n` is the number of nodes. In the worst case with a cycle, the slow and fast pointers will meet after the slow pointer has traversed at most `n` steps.

##### Space Complexity: `O(1)`

We only use two pointers regardless of the input size.

#### Key Insights

- Uses constant extra space, making it more memory-efficient than the hash set approach
- Elegant mathematical solution that leverages the cycle property
- When pointers move at different speeds in a cycle, they'll eventually meet

### Solution 3: Marking Visited Nodes

```python
def hasCycle(self, head: Optional[ListNode]) -> bool:
    # Traverse the list
    while head:
        # If we've modified this node before, we found a cycle
        if head.val == float('inf'):
            return True
        
        # Mark this node as visited by changing its value
        head.val = float('inf')
        
        # Move to the next node
        head = head.next
    
    # If we reach the end, there's no cycle
    return False
```

#### Approach

This solution marks nodes as visited by changing their values to a special sentinel value (like `float('inf')`). As we traverse the list, if we encounter a node that's already been marked, we know there's a cycle. This approach assumes we're allowed to modify the original list structure.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Where `n` is the number of nodes. We traverse the list once.

##### Space Complexity: `O(1)`

We don't use any extra data structures that scale with input size.

#### Key Insights

- Very space-efficient as it uses constant extra space
- Simple implementation
- The main drawback is that it modifies the original list, which may not be allowed in some scenarios

## Comparison of Solutions

### Time Complexity

- **Hash Set**: `O(n)` - Traverses the list once
- **Two Pointers**: `O(n)` - Also traverses the list with slow and fast pointers
- **Marking Nodes**: `O(n)` - Single traversal of the list

### Space Complexity

- **Hash Set**: `O(n)` - Stores all nodes in a hash set
- **Two Pointers**: `O(1)` - Uses only two pointers
- **Marking Nodes**: `O(1)` - No additional data structures

### Trade-offs

- The hash set solution is intuitive but uses more memory
- The two-pointer solution is memory-efficient and doesn't modify the list
- The marking approach is memory-efficient but modifies the original list

### When to Use Each

- **Hash Set**: When simplicity is valued over memory efficiency
- **Two Pointers**: When memory efficiency is important and we can't modify the list
- **Marking Nodes**: When memory efficiency is important and modifying the list is allowed

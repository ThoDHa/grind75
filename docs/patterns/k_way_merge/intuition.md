# K-Way Merge - Intuition Guide

**Reference:** [K-way merge](https://en.wikipedia.org/wiki/K-way_merge_algorithm)

## The Mental Model: Racing Snails

Imagine K snails racing on parallel tracks, each carrying numbered flags in ascending order. You need to announce the numbers in global sorted order.

**Naive approach**: Wait for all snails to finish, collect all flags, sort them.
*Problem*: You're ignoring the fact that each track is already sorted!

**Smart approach**: Look at the K snails currently in the lead, announce the smallest number, then that snail advances to show its next flag.

```
Track 1: 🐌[1] → [4] → [5] → FINISH
Track 2: 🐌[1] → [3] → [4] → FINISH
Track 3: 🐌[2] → [6] → FINISH

Step 1: Current leads are [1, 1, 2]. Announce 1, snail 1 advances to [4]
Step 2: Current leads are [4, 1, 2]. Announce 1, snail 2 advances to [3]
Step 3: Current leads are [4, 3, 2]. Announce 2, snail 3 advances to [6]
...
```

The "looking at K leads" is exactly what the min-heap does!

## Why K-Way Merge Matters

### The Naive Trap

Many beginners think: "I have K sorted lists. Let me merge them one by one."

```python
# Don't do this!
result = lists[0]
for i in range(1, K):
    result = merge(result, lists[i])  # O(N) per merge
# Total: O(N*K) - very slow for large K!
```

### The Optimal Insight

> **You only need to compare K elements at any time - the K current heads.**

```
K lists, N total elements:
- Naive merge one-by-one: O(NK)
- Heap of K heads: O(N log K)  ← Much better when K is large!
```

## Three Ways to Merge

### Way 1: Min-Heap (Most Versatile)

**Mental model**: A tournament bracket where K contestants compete. The winner (minimum) exits, and the loser's team sends the next player.

```
Heap state at any moment:
┌─────────────────┐
│   Min-Heap      │
│   (size K)      │
│                 │
│     [1]         │  ← Root is global minimum
│    /   \        │
│  [2]   [1]      │
└─────────────────┘

Operations:
- Pop minimum → O(log K)
- Push successor → O(log K)
- Total for N elements → O(N log K)
```

**When to use**: K is large, streaming data, or you need O(N log K).

### Way 2: Divide and Conquer

**Mental model**: A merge sort tournament. Round 1: merge lists 0+1, 2+3, etc. Round 2: merge results. Continue until one list remains.

```
Round 1:     Round 2:      Round 3:
[L0] [L1]      [M0]          [M0']
  \ /           |              |
 [M0]         [M0']         [FINAL]
              /
[L2] [L3]    /
  \ /       /
 [M1]------/

Lists halve each round → log K rounds
Each round processes N elements → O(N log K) total
```

**When to use**: All data available upfront, want to avoid heap allocation.

### Way 3: Two-Pointer (K=2 Only)

**Mental model**: Two people reading from sorted decks, calling out the smaller card.

```
Person 1: [1, 4, 5]  →  points at 1
Person 2: [2, 3, 6]  →  points at 2

Round 1: 1 < 2, call "1", Person 1 advances to 4
Round 2: 4 > 2, call "2", Person 2 advances to 3
Round 3: 4 > 3, call "3", Person 2 advances to 6
...
```

**When to use**: Exactly 2 lists, or as building block for divide-and-conquer.

## The Backward Merge Trick

For in-place array merge (LC 88), merging forward overwrites elements:

```
Forward merge (BROKEN):
nums1 = [1, 2, 3, _, _, _]
nums2 = [2, 5, 6]

Step 1: Compare 1 and 2, write 1 at position 0
nums1 = [1, 2, 3, _, _, _]  ← We overwrote position 0, but it was already 1!

Step 2: Compare 2 and 2, write 2 at position 1
nums1 = [1, 2, 3, _, _, _]  ← We overwrote 2 with 2, okay...

Step 3: Compare 3 and 2, write 2 at position 2
nums1 = [1, 2, 2, _, _, _]  ← We lost the 3!
```

**Solution: Merge from the end!**

```
Backward merge (CORRECT):
nums1 = [1, 2, 3, _, _, _]
nums2 = [2, 5, 6]

Write position: 5 (rightmost)

Step 1: Compare 3 and 6, write 6 at position 5
nums1 = [1, 2, 3, _, _, 6]

Step 2: Compare 3 and 5, write 5 at position 4
nums1 = [1, 2, 3, _, 5, 6]

Step 3: Compare 3 and 2, write 3 at position 3
nums1 = [1, 2, 3, 3, 5, 6]  ← No overwriting issues!
```

## Common Mistakes

### Mistake 1: Comparing Non-Comparable Objects

```python
# WRONG: Python can't compare ListNode objects
heap = []
for node in lists:
    heapq.heappush(heap, (node.val, node))  # Error when vals are equal!

# RIGHT: Add a tie-breaker (list index)
for i, node in enumerate(lists):
    heapq.heappush(heap, (node.val, i, node))  # i breaks ties
```

### Mistake 2: Forgetting Empty Lists

```python
# WRONG: Empty list causes IndexError
for arr in arrays:
    heap.append((arr[0], arr))  # Crashes if arr is empty!

# RIGHT: Check before adding
for i, arr in enumerate(arrays):
    if arr:  # Skip empty
        heap.append((arr[0], i, 0))
```

### Mistake 3: One-by-One Sequential Merge

```python
# WRONG: O(NK) - too slow
result = lists[0]
for lst in lists[1:]:
    result = merge(result, lst)

# RIGHT: Use heap O(N log K) or divide-and-conquer O(N log K)
```

## Practice Progression

Build the merge instinct in order of increasing K:

1. **Merge Two Sorted Lists (LC 21)**: the K=2 case. A pure two-pointer merge, no heap needed.
2. **Merge Sorted Array (LC 88)**: still K=2, but in-place. Practice the backward merge trick above.
3. **Merge K Sorted Lists (LC 23)**: the general case. A min-heap of the K heads, or divide-and-conquer built from pairwise two-pointer merges.

## Visual Summary

```
┌──────────────────────────────────────────────────────────────────┐
│                    K-Way Merge Pipeline                          │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────┐                                             │
│  │  Initialize     │  Add head of each non-empty list to heap   │
│  │  Heap (size K)  │  Entry: (value, index, node/position)      │
│  └────────┬────────┘                                             │
│           │                                                       │
│           ▼                                                       │
│  ┌─────────────────┐                                             │
│  │  While heap     │  1. Pop minimum element                     │
│  │  not empty:     │  2. Add to result                           │
│  │                 │  3. If successor exists, push to heap       │
│  └────────┬────────┘                                             │
│           │                                                       │
│           ▼                                                       │
│  ┌─────────────────┐                                             │
│  │  Return Result  │  All N elements processed in O(N log K)    │
│  └─────────────────┘                                             │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

## Pattern Recognition Checklist

| See This | Think This |
|----------|------------|
| "Merge K sorted X" | Heap-based K-way merge |
| "Merge two sorted X" | Two-pointer merge |
| "In-place merge with extra space" | Backward merge |
| "K sorted iterators/streams" | Heap-based (streaming) |
| "External sort" | K-way merge from disk |



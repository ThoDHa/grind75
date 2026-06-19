# [Task Scheduler](https://leetcode.com/problems/task-scheduler/)

**Medium** | **30 minutes** | **Array, Hash Table, Greedy, Sorting, Heap**

**Pattern:** [Heap / Priority Queue](../patterns/heap/intuition.md), [Greedy](../patterns/greedy_core/intuition.md)

**Practice:** [`practice/task_scheduler/solution.py`](../../practice/task_scheduler/solution.py)

Given a characters array `tasks`, representing the tasks a CPU needs to do, where each letter represents a different task. Tasks could be done in any order. Each task is done in one unit of time. For each unit of time, the CPU could complete either one task or just be idle.

However, there is a non-negative integer `n` that represents the cooldown period between two same tasks (the same letter in the array), that is, there must be at least `n` units of time between any two same tasks.

Return the least number of units of time that the CPU will take to finish all the given tasks.

## Examples

### Example 1

**Input:** `tasks = ["A","A","A","B","B","B"]`, `n = 2`

**Output:** `8`

**Explanation:**
A -> B -> idle -> A -> B -> idle -> A -> B
There is at least 2 units of time between any two same tasks.

### Example 2

**Input:** `tasks = ["A","A","A","B","B","B"]`, `n = 0`

**Output:** `6`

**Explanation:** On this case any permutation of size 6 would work since n = 0.
["A","A","A","B","B","B"]
["A","B","A","B","A","B"]
["B","B","B","A","A","A"]
...
And so on.

### Example 3

**Input:** `tasks = ["A","A","A","A","A","A","B","C","D","E","F","G"]`, `n = 2`

**Output:** `16`

**Explanation:**
One possible solution is
A -> B -> C -> A -> D -> E -> A -> F -> G -> A -> idle -> idle -> A -> idle -> idle -> A

## Constraints

- `1 <= task.length <= 10^4`
- `tasks[i]` is an uppercase English letter.
- `0 <= n <= 100`

## Solutions

### Greedy Simulation

```python
class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        # Count each task's frequency without any imported counter.
        counts = {}
        for t in tasks:
            counts[t] = counts.get(t, 0) + 1

        remaining = list(counts.values())
        time = 0

        # Simulate the schedule one cooldown frame at a time.
        while any(c > 0 for c in remaining):
            # Greedily run the highest-frequency tasks first this round.
            remaining.sort(reverse=True)

            executed = 0
            # A round can run at most n + 1 distinct tasks before the most
            # frequent task is eligible to repeat.
            for i in range(n + 1):
                if i < len(remaining) and remaining[i] > 0:
                    remaining[i] -= 1
                    executed += 1

            # If tasks still remain, the unused slots in this round are idle;
            # otherwise the final round simply ends with no trailing idle time.
            if any(c > 0 for c in remaining):
                time += n + 1
            else:
                time += executed

        return time
```

#### Approach

The intuitive strategy mirrors how an optimal CPU would behave: at every cooldown
frame, run the tasks that still have the most copies left, because those are the
ones most likely to force idle time later. Each frame is `n + 1` slots wide, the
minimum gap before the most frequent task may repeat.

1. Count each task's frequency into a plain dictionary, then collect the counts
   into a `remaining` list.
2. Repeat until every count is zero. At the start of each round, sort `remaining`
   in descending order so the most-needed tasks come first.
3. Execute up to `n + 1` of them: decrement each chosen task's count and tally how
   many were actually executed this round.
4. If any tasks still remain after the round, the round must be padded to the full
   `n + 1` width (the unfilled slots are idle), so add `n + 1` to `time`. If
   nothing remains, the final round needs no trailing idle, so add only the number
   of tasks executed.
5. Return the accumulated `time`.

Sorting each round greedily keeps the schedule tight, and the idle accounting falls
out naturally from whether work is still pending.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(N * 26 log 26)`

Let `N` be the number of tasks. The simulation runs roughly `O(total_time)` rounds,
bounded by the schedule length which is `O(N)`. Each round sorts the `remaining`
list of at most 26 counts, costing `O(26 log 26)`, a constant. Multiplying gives
`O(N * 26 log 26)`, which is effectively linear in `N` with a constant factor.

##### Space Complexity: `O(1)`

The `counts` dictionary and `remaining` list hold at most 26 entries (uppercase
letters), independent of `N`.

#### Key Insights

- Running the highest-remaining-count tasks first each round is the greedy choice
  that minimizes forced idling.
- Each cooldown frame is naturally `n + 1` wide, which is why a round executes up to
  `n + 1` distinct tasks.
- The idle time is never placed explicitly; it emerges from padding non-final rounds
  to full width while letting the last round end early.
- A plain dictionary replaces any imported counter, and the 26-letter alphabet keeps
  every per-round operation constant.

### Max-Heap Simulation

```python
import heapq


class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        # Count each task's frequency without any imported counter.
        counts = {}
        for t in tasks:
            counts[t] = counts.get(t, 0) + 1

        # Negate counts to turn Python's min-heap into a max-heap.
        heap = [-c for c in counts.values()]
        heapq.heapify(heap)

        time = 0
        while heap:
            survivors = []
            executed = 0
            # One cooldown cycle is n + 1 slots wide; run up to n + 1 tasks.
            for _ in range(n + 1):
                if heap:
                    # Pop the most frequent remaining task and consume one copy.
                    count = -heapq.heappop(heap) - 1
                    executed += 1
                    if count > 0:
                        survivors.append(-count)

            # Return the still-pending tasks to the heap for the next cycle.
            for s in survivors:
                heapq.heappush(heap, s)

            # If work remains, pad this cycle to full width (the unused slots
            # are idle); otherwise the final cycle ends after the last task.
            if heap:
                time += n + 1
            else:
                time += executed

        return time
```

#### Approach

The greedy choice (always run the task with the most copies left) is exactly what
a max-heap gives in `O(log 26)` per pop. Each cooldown cycle is `n + 1` slots wide,
the minimum gap before the most frequent task may repeat, so each cycle pops up to
`n + 1` tasks, decrements them, and defers any survivors to the next cycle.

1. Count frequencies into a plain dictionary, then build a max-heap by negating
   the counts (Python's `heapq` is a min-heap).
2. For each cooldown cycle, attempt to pop up to `n + 1` tasks. For every pop,
   consume one copy and tally `executed`; if copies remain, stash the task in a
   temporary `survivors` list rather than pushing it back mid-cycle (which could
   let a task run twice inside one cooldown window).
3. Push every survivor back onto the heap after the cycle completes.
4. If the heap still holds work, the cycle must be padded to its full `n + 1`
   width (the unfilled slots are idle), so add `n + 1` to `time`. If nothing
   remains, the final cycle ends after its last task, so add only `executed`.

Deferring survivors until the cycle completes is what enforces the cooldown: a
task cannot reappear until `n + 1` slots have passed. Counting `executed` rather
than padding the final cycle is what avoids trailing idle time at the end.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(N log 26)`

Let `N` be the number of tasks. Every task copy is popped and possibly pushed
once across all cycles, and each heap operation costs `O(log 26)` since the heap
holds at most 26 distinct tasks. The total is `O(N log 26)`, effectively linear
in `N` with a small constant.

##### Space Complexity: `O(1)`

The heap and `survivors` list each hold at most 26 entries (uppercase letters),
independent of `N`.

#### Key Insights

- The heap automates the greedy "run the most frequent task first" rule, replacing
  the per-round sort of the array-based simulation.
- Survivors must be buffered and pushed back only after the full `n + 1` cycle,
  otherwise a task could be scheduled twice within a single cooldown window.
- Breaking out when both the heap and survivors are empty avoids counting trailing
  idle slots in the final, partial cycle.

### Greedy Math Formula

```python
class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        # Count each task's frequency without any imported counter.
        counts = {}
        for t in tasks:
            counts[t] = counts.get(t, 0) + 1

        max_freq = max(counts.values())
        # How many distinct tasks share that peak frequency.
        max_count = sum(1 for freq in counts.values() if freq == max_freq)

        # Frame built around the most frequent task: (max_freq - 1) full gaps of
        # width (n + 1), then the final block holding every peak task.
        frame = (max_freq - 1) * (n + 1) + max_count

        # If there are enough distinct tasks to fill every idle slot, no idling is
        # needed and the answer is simply the number of tasks.
        return max(len(tasks), frame)
```

#### Approach

The simulation can be collapsed into a closed-form formula because the schedule
length is dictated entirely by the most frequent task. Suppose the maximum frequency
is `max_freq`. Lay those occurrences out as anchors separated by cooldown gaps of
width `n`:

```
A . . . A . . . A
```

There are `max_freq - 1` gaps, each spanning `n + 1` slots (the task plus `n`
following slots), which accounts for `(max_freq - 1) * (n + 1)` units. The final
anchor block needs room for every task that also hits the peak frequency, so we add
`max_count`, the number of tasks tied for the maximum.

That gives the framed length `(max_freq - 1) * (n + 1) + max_count`. The idle slots
inside the gaps can be filled by other tasks. If there are so many other tasks that
they overflow the gaps, no idling is ever required and the answer is just the total
number of tasks. Taking the maximum of the two handles both regimes.

1. Count each task's frequency into a plain dictionary.
2. Find `max_freq` and `max_count` (how many tasks reach it).
3. Compute the frame `(max_freq - 1) * (n + 1) + max_count`.
4. Return `max(len(tasks), frame)`.

When the frame exceeds `len(tasks)`, the difference is exactly the number of forced
idle units; otherwise every slot is busy. This works because the most frequent task
fixes a rigid skeleton of anchors and gaps, and every other task either slots into a
gap or pushes the schedule out only when the total task count overflows the frame.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(N)`

Where `N` is the number of tasks. Counting frequencies is `O(N)`, and the remaining
work scans at most 26 distinct task counts, which is constant.

##### Space Complexity: `O(1)`

The frequency dictionary holds at most 26 entries (uppercase letters), independent
of `N`.

#### Key Insights

- The answer is governed entirely by the peak frequency and how many tasks tie for
  it; the exact identities of other tasks do not matter.
- `(max_freq - 1) * (n + 1)` measures the rigid skeleton imposed by cooldown; adding
  `max_count` accounts for the trailing block of all peak tasks.
- Taking `max(len(tasks), frame)` cleanly resolves the two cases: idle-bound (frame
  wins) versus task-bound (no idling needed).
- The formula collapses the round-by-round simulation into a single arithmetic
  expression with no loop over time at all.

## Comparison of Solutions

### Time Complexity

- **Greedy Simulation**: `O(N * 26 log 26)` because it runs roughly `O(N)` rounds,
  each sorting up to 26 counts.
- **Max-Heap Simulation**: `O(N log 26)` because every task copy is popped and
  pushed once, each heap operation costing `O(log 26)`.
- **Greedy Math Formula**: `O(N)` because it only counts frequencies once and then
  does constant arithmetic over at most 26 counts.

### Space Complexity

- **Greedy Simulation**: `O(1)`, using a 26-entry dictionary and list.
- **Max-Heap Simulation**: `O(1)`, using a 26-entry heap and survivors list.
- **Greedy Math Formula**: `O(1)`, using a 26-entry dictionary.

All three use constant auxiliary space; the difference is in time and conceptual
complexity.

### Trade-offs

- The greedy simulation directly models what the CPU does, which makes its
  correctness easy to see and easy to debug: you can print the schedule round by
  round. Its cost is the repeated sorting and the explicit time loop.
- The max-heap simulation replaces the per-round sort with a heap, automating the
  greedy choice in `O(log 26)` per operation. It is the natural data-structure
  refinement of the array simulation while still tracing the schedule cycle by cycle.
- The formula is a single expression with no loop over time, making it dramatically
  faster, but it requires the insight that the peak frequency alone determines the
  idle skeleton. That leap is harder to derive from scratch.

### When to Use Each

- **Greedy Simulation**: Useful when you want to verify behavior, visualize the
  actual schedule, or when the greedy formula's derivation is not yet obvious.
- **Max-Heap Simulation**: When you want the simulation's transparency but prefer a
  heap to express the greedy choice, a common interview-favored formulation.
- **Greedy Math Formula**: Preferred for production and for the constraint ceiling,
  where the closed form runs in a single linear pass with no simulation overhead.

### Optimization Notes

- The greedy simulation establishes the greedy principle (always run the most
  frequent remaining tasks first), which both the heap simulation and the formula
  encode in their own way.
- The max-heap simulation is the structural optimization of the simulation: a heap
  surfaces the most frequent task in `O(log 26)` instead of re-sorting each round.
- The formula is the key algorithmic optimization: recognizing that the most
  frequent task dictates the layout removes the need to simulate every time unit.
- All three solutions count frequencies with a plain dictionary, avoiding any
  imported counter while keeping the 26-letter alphabet's operations constant.

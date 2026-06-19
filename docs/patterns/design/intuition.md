# Data-Structure Design: Pattern Intuition Guide

> *"Design is not about inventing new structures — it is about composing old ones so each operation pays the price it promised."*

---

## The Situation That Calls for Design

Most problems hand you an input and ask for an answer. **Design problems hand you a contract.**

You are asked to implement a class — `MinStack`, `LRUCache`, `FreqStack` — that supports a fixed menu of operations. Alongside each operation comes a promise about its cost:

> *"All operations must run in O(1)."*
> *"`get` and `put` must each be O(1) on average."*
> *"`getMin` must be constant time even after many pushes and pops."*

A naive single structure usually satisfies *some* operations cheaply and others expensively. A plain stack gives O(1) `push` and `pop`, but `getMin` costs O(n) because you must scan. A plain array gives O(1) random access, but maintaining recency order costs O(n) on every touch.

**The craft is choosing and composing primitive structures so that every operation in the contract meets its guarantee — and keeping those structures in sync as the data changes.**

---

## The Core Insight

Work **backward from the required complexities** to the structures that can provide them.

Each primitive has a fixed set of operations it does cheaply:

| Structure | O(1) operations | What it cannot do cheaply |
|-----------|-----------------|---------------------------|
| Array / dynamic array | Index access, append/pop at end | Arbitrary insert/delete (O(n) shift) |
| Hash map | Lookup, insert, delete by key | Ordering, "next largest" |
| Doubly linked list | Insert/remove at a known node | Find by value (O(n) scan) |
| Stack | Push, pop, peek top | Access to non-top elements |
| Heap | Peek min/max O(1), push/pop O(log n) | Lookup by value |

Read the contract, then for each operation ask: *which primitive does this cheaply?* When no single primitive covers every operation, **combine two so the strengths overlap and the weaknesses cancel**.

The second, equally important half of the insight: **every operation must preserve the invariants that tie those structures together.** If a hash map and a linked list both describe the same data, then any mutation must update *both*, or the structures drift apart and later operations return wrong answers. The design is correct only as long as its invariants hold after *every* mutating call.

---

## Mental Model 1: The Auxiliary Structure

When one structure cannot answer a query cheaply, **carry a second structure that pre-computes the answer.**

A stack supports `push`/`pop`/`top` in O(1) but not `getMin`. So we keep a *second* stack whose top always holds the minimum of everything currently in the main stack.

```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.mins = []          # mins[-1] is min of stack

    def push(self, x):
        self.stack.append(x)
        self.mins.append(min(x, self.mins[-1] if self.mins else x))

    def pop(self):
        self.stack.pop()
        self.mins.pop()         # invariant: mins moves in lockstep

    def getMin(self):
        return self.mins[-1]    # O(1)
```

The invariant: **`mins` always has the same length as `stack`, and `mins[i]` is the minimum of `stack[0..i]`.** Every push and pop touches both stacks, so the invariant never breaks. The min you need is always sitting at the top, already computed.

---

## Mental Model 2: Hash Map + Doubly Linked List

When you need **O(1) lookup *and* O(1) ordering updates**, no single primitive suffices. Combine the two that each own one half.

This is the LRU cache. We need:
- `get(key)` in O(1) → a **hash map** for instant lookup
- mark a key as "most recently used" in O(1) → a **doubly linked list** where moving a node to the front is constant time

```
HEAD ⇄ [most recent] ⇄ ... ⇄ [least recent] ⇄ TAIL

hash map:  key ──► node in the list
```

The hash map maps each key to the *node object* inside the list. To touch a key: look it up in the map (O(1)), unlink the node, and splice it to the front (O(1), because a doubly linked list lets you remove a known node without scanning). To evict: drop the node just before `TAIL` and delete its key from the map.

The invariant: **the hash map and the list always describe the same set of keys.** Insert into one, insert into the other; delete from one, delete from the other.

---

## Mental Model 3: Amortized Analysis (Two Stacks as a Queue)

Sometimes an operation looks expensive in the worst case but is cheap *on average* over a sequence of calls. That is **amortized** cost, and it is a legitimate way to meet an O(1) contract.

A queue needs FIFO order; a stack gives LIFO. Use two stacks:

```python
class MyQueue:
    def __init__(self):
        self.inbox = []     # newest on top
        self.outbox = []    # oldest on top

    def push(self, x):
        self.inbox.append(x)

    def pop(self):
        if not self.outbox:                 # only refill when empty
            while self.inbox:
                self.outbox.append(self.inbox.pop())
        return self.outbox.pop()
```

A single `pop` can be O(n) when it triggers a transfer. But **each element is moved at most twice** in its lifetime: once from `inbox` to `outbox`, once out of `outbox`. Spread across all operations, the cost per call averages to O(1). The key discipline: **only refill `outbox` when it is empty**, so no element is ever transferred twice.

When a problem says "O(1) amortized," it is inviting exactly this kind of design.

---

## Mental Model 4: Layered / Indexed Structures

When a query depends on a *property* of the elements (their frequency, their priority, their bucket), **index your data by that property.**

The "maximum frequency stack" must pop the most frequent element, breaking ties by recency. Keep:
- a hash map `freq[x]` → how many times `x` is currently present
- a hash map `groups[f]` → a *stack* of the elements that have reached frequency `f`

```python
class FreqStack:
    def __init__(self):
        self.freq = {}
        self.groups = {}        # frequency -> stack of values
        self.maxfreq = 0

    def push(self, x):
        f = self.freq.get(x, 0) + 1
        self.freq[x] = f
        self.maxfreq = max(self.maxfreq, f)
        self.groups.setdefault(f, []).append(x)

    def pop(self):
        x = self.groups[self.maxfreq].pop()
        self.freq[x] -= 1
        if not self.groups[self.maxfreq]:
            self.maxfreq -= 1
        return x
```

The top of `groups[maxfreq]` is always the most-frequent, most-recent element — exactly what `pop` needs, in O(1). The stack inside each frequency layer preserves recency for free, and `maxfreq` is a cached pointer to the layer that matters.

---

## Pattern Recognition Signals

When you see these phrases, think **Data-Structure Design**:

### Signal: "Implement a class / design a structure"
> *"Design a data structure that supports the following operations..."*
> *"Implement the `LRUCache` class."*

**Action**: List the operations, write each one's complexity target next to it, then assign primitives.

### Signal: A complexity budget per operation
> *"All operations in O(1)."*
> *"`get` and `put` in O(1) average time."*
> *"`getMin` in constant time."*

**Action**: Work backward from each budget to a primitive that meets it; compose when one is not enough.

### Signal: A menu of named operations
> *"Support `push`, `pop`, `getMin`."*
> *"Support `insert`, `remove`, `getRandom`."*

**Action**: Find the operation that the obvious single structure handles *poorly* — that gap tells you which auxiliary structure to add.

---

## Worked Walkthrough: Min Stack

Operations and budget: `push` O(1), `pop` O(1), `top` O(1), `getMin` O(1).

A plain stack handles three of four; `getMin` is the gap. Add the auxiliary min-stack from Mental Model 1.

Trace `push(3), push(5), push(2), getMin(), pop(), getMin()`:

```
push 3   stack=[3]        mins=[3]
push 5   stack=[3,5]      mins=[3,3]   (min(5,3)=3)
push 2   stack=[3,5,2]    mins=[3,3,2] (min(2,3)=2)
getMin → mins[-1] = 2
pop      stack=[3,5]      mins=[3,3]
getMin → mins[-1] = 3     (the 2 left, and so did its min)
```

Because both stacks move together, `getMin` is always reading a value that was computed at push time. Nothing is recomputed.

---

## Worked Walkthrough: LRU Cache

Operations and budget: `get(key)` O(1), `put(key, value)` O(1), evict least-recently-used when at capacity.

From Mental Model 2: hash map (key → node) plus a doubly linked list ordered most-recent → least-recent.

Trace with capacity 2: `put(1,A), put(2,B), get(1), put(3,C)`:

```
put(1,A)  list: 1 ⇄ TAIL                  map: {1}
put(2,B)  list: 2 ⇄ 1 ⇄ TAIL              map: {1,2}
get(1)    → A; move 1 to front
          list: 1 ⇄ 2 ⇄ TAIL             map: {1,2}
put(3,C)  capacity full → evict tail (2)
          list: 3 ⇄ 1 ⇄ TAIL             map: {1,3}
```

Notice the discipline at `put(3,C)`: we evict from **both** structures. We unlink node `2` from the list *and* delete key `2` from the map. Skip either and the next `get(2)` would return a stale hit or a dangling node. **Every mutating operation touches every structure that mirrors the data.**

---

## Common Pitfalls

### Pitfall 1: Confusing Amortized with Worst-Case
A two-stack queue is O(1) *amortized*, not O(1) per call — a single `pop` can be O(n). If the contract demands O(1) *worst-case*, an amortized design does not satisfy it. Read the budget precisely.

### Pitfall 2: Structures Drifting Out of Sync
When two structures mirror the same data, a mutation that updates one but not the other leaves them inconsistent. The bug surfaces *later*, on a read that trusts the structure you forgot to update. Make it a rule: **every mutating operation updates every mirror.**

### Pitfall 3: Eviction and Ordering Bugs
In recency- or frequency-ordered designs, the subtle errors live in the edges: evicting the wrong end of the list, forgetting to refresh recency on `get`, or failing to decrement `maxfreq` when a frequency layer empties. Walk a small trace by hand through the boundary cases.

### Pitfall 4: Forgetting to Maintain Cached Helpers
Auxiliary values like the min-stack top or `maxfreq` are *derived state*. If you mutate the primary data without updating the helper, the helper lies. Treat the helper as part of the invariant, not an afterthought.

### Pitfall 5: Choosing a Structure That Cannot Meet the Budget
Reaching for an array when the contract needs O(1) middle-deletion, or a list when it needs O(1) lookup, dooms the design before you write a line. Match primitive to budget first.

---

## Practice Progression

Build mastery of design through this sequence:

1. **Min Stack** — Carry an auxiliary min-stack so `getMin` is O(1). The cleanest introduction to "a second structure pre-computes the hard query."

2. **Implement Queue using Stacks** — Two stacks give FIFO order; each element moves at most twice, so the cost is O(1) amortized. Learn to reason about amortized cost.

3. **LRU Cache** — Hash map for O(1) lookup plus a doubly linked list for O(1) recency updates. The canonical "compose two structures and keep them in sync" problem.

4. **Maximum Frequency Stack** — Frequency-indexed stacks, where elements are bucketed by how many times they appear and a cached `maxfreq` points at the live layer. Layered indexing in its purest form.

---

## The Unifying Principle

Design is **composition under a contract**.

You are given operations and their costs. You do not invent new structures; you assemble known ones so that each operation lands on a primitive that handles it cheaply — and you uphold the invariants that bind those primitives together through every mutation.

Two questions carry every design:

1. *Which primitive makes this operation cheap?*
2. *What must stay true after every change, and does every operation keep it true?*

*"A design is only as correct as its invariants — and an invariant is only as strong as the operation most likely to forget it."*

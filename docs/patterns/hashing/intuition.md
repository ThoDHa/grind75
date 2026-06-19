# Hashing & Frequency Counting: Pattern Intuition Guide

> *"A hash map is memory with an instant recall — it remembers everything you've seen so you never have to look twice."*

---

## The Situation That Calls for Hashing

Imagine you're a bouncer at a private event holding a thick guest list. Someone walks up. Should you let them in?

You could read the list top to bottom every time a guest arrives. With one guest, that's fine. With a thousand arrivals against a thousand names, you're scanning a million times.

**There's a better way.**

Before the doors open, you memorize the list — not as an ordered sequence, but as a *set of names you can recall instantly*. Now each arrival is a single question: *"Is this name on the list?"* The answer comes immediately, no scanning required.

**This is the essence of Hashing.**

You encounter this pattern whenever:
- You ask *"have I seen this before?"* — **membership**
- You ask *"is there another element that pairs with this one?"* — **complement lookup**
- You ask *"how many of each thing are there?"* — **counting**

The unifying move: instead of searching the data again and again, you build an index of what you've seen and query it in constant time.

---

## The Core Insight: Trading Space for O(1) Lookup

Brute force answers "is X here?" by walking the whole collection: O(n) per question, O(n²) over n questions. A hash map collapses that question to O(1) by spending memory.

The map (or set) is **an index of the past**. As you walk the data once, you record what you've seen. Every future question becomes a direct lookup instead of a scan.

| Without Hashing | With Hashing |
|-----------------|--------------|
| Each lookup: O(n) | Each lookup: O(1) average |
| n lookups → O(n²) | n lookups → O(n) |
| Zero extra memory | O(n) extra memory |

The trade is explicit: *you spend space to buy time.* When the array is unsorted and you cannot afford repeated scans, this is almost always the right bargain.

The key shift in thinking: *You're not searching the data — you're asking the data a question it has already answered.*

---

## The Mental Models

Hashing problems wear four faces. Recognizing the face tells you what structure to reach for and what question to ask it.

### Model 1: The Complement Search — "Have I seen target − x?"

You walk the array once. For each element `x`, you don't search for a matching partner ahead of you. Instead you ask the past: *"Did an earlier element equal what I still need?"*

If you need a pair summing to `target`, the partner of `x` is `target - x`. So before storing `x`, you check whether `target - x` is already in the map.

```python
seen = {}                      # value -> index
for i, x in enumerate(nums):
    need = target - x
    if need in seen:           # the partner arrived earlier
        return [seen[need], i]
    seen[x] = i                # remember x for future partners
```

**Why it works**: every pair has two members. By the time you reach the second member, the first is already recorded. You only ever look backward, and backward is O(1).

### Model 2: The Frequency Map — "How many of each?"

When the question is about *counts* rather than presence, the map stores `element -> count`. One pass builds the tally; comparisons become arithmetic on counts.

```python
from collections import Counter
freq = Counter(s)              # {'a': 3, 'b': 1, ...}
```

Anagrams, character budgets, and "can I build X from Y" questions all reduce to comparing two frequency maps or subtracting one from another.

### Model 3: The "Seen" Set — Membership

When you only care *whether* something appeared, not how many times, a set is leaner than a map. No values, just keys.

```python
seen = set()
for x in nums:
    if x in seen:              # duplicate found
        return True
    seen.add(x)
return False
```

A set answers a yes/no question. A map answers a how-many question. Pick the lighter tool for the job.

### Model 4: Boyer-Moore Voting — Counting Without a Map

There is one counting problem that needs **no hash structure at all**: finding a *strict majority* element (one appearing more than ⌊n/2⌋ times).

The trick treats the element as a candidate that survives a series of cancellations. Keep a candidate and a running count. Each matching element is a vote for the candidate; each differing element cancels one vote. When the count hits zero, adopt the next element as the new candidate.

```python
candidate, count = None, 0
for x in nums:
    if count == 0:
        candidate = x
    count += 1 if x == candidate else -1
return candidate
```

**Why it works**: a strict majority outnumbers *everything else combined*. Pairing each majority element against a non-majority element cancels both, but the majority has surplus votes that nothing can cancel. The survivor is the answer — in O(1) space.

This is a special case worth knowing: it shows that "counting" does not always mean "build a frequency map." When one element dominates, voting beats tallying.

---

## Pattern Recognition Signals

When you see these phrases, think **Hashing & Frequency Counting**:

### Signal: "Have I seen X before?"
> *"Find the first repeated element"*
> *"Detect if a value occurs twice"*

**Action**: Use a "seen" set. Check before insert.

### Signal: "Find a pair / group with a property"
> *"Two numbers that sum to target"*
> *"Indices i, j where nums[i] + nums[j] == k"*

**Action**: Complement lookup. Store seen values, query for the needed partner.

### Signal: "Count of each element" or "How many times..."
> *"Are these two strings anagrams?"*
> *"Most frequent element"*

**Action**: Build a frequency map, then compare or scan counts.

### Signal: "Is there a duplicate?" or "All unique?"
> *"Contains duplicate"*
> *"Are all rows distinct?"*

**Action**: Compare set size to length, or short-circuit with a seen-set.

### Signal: "Majority / appears more than half the time"
> *"Element that appears more than ⌊n/2⌋ times"*

**Action**: Boyer-Moore voting for O(1) space (or a frequency map if simplicity matters more).

---

## Worked Intuition Traces

### Trace 1: Complement Lookup — Two Sum

**Problem**: Return indices of two numbers that add up to `target`.
**Input**: `nums = [3, 2, 4]`, `target = 6`

```
┌──────────────────────────────────────────────────────────────────┐
│  seen = {}             target = 6                                  │
├──────────────────────────────────────────────────────────────────┤
│  i=0, x=3   need = 6-3 = 3   3 not in seen   → store {3: 0}        │
│                                                                    │
│  i=1, x=2   need = 6-2 = 4   4 not in seen   → store {3:0, 2:1}    │
│                                                                    │
│  i=2, x=4   need = 6-4 = 2   2 IS in seen!   → return [1, 2]       │
└──────────────────────────────────────────────────────────────────┘

Key observations:
• We never compared 3 with 4 directly — the complement check did it.
• Each element is looked at once; each lookup is O(1).
• Only the past is consulted, so no pair is ever counted twice.
```

### Trace 2: Frequency Map — Valid Anagram

**Problem**: Is `t` a rearrangement of `s`?
**Input**: `s = "anagram"`, `t = "nagaram"`

```
┌──────────────────────────────────────────────────────────────────┐
│  Build freq(s):  a:3  n:1  g:1  r:1  m:1                           │
│                                                                    │
│  Subtract each char of t:                                          │
│     n → a:3 n:0 g:1 r:1 m:1                                        │
│     a → a:2 n:0 g:1 r:1 m:1                                        │
│     g → a:2 n:0 g:0 r:1 m:1                                        │
│     a → a:1 n:0 g:0 r:1 m:1                                        │
│     r → a:1 n:0 g:0 r:0 m:1                                        │
│     a → a:0 n:0 g:0 r:0 m:1                                        │
│     m → a:0 n:0 g:0 r:0 m:0                                        │
│                                                                    │
│  All counts zero → anagram confirmed.                             │
└──────────────────────────────────────────────────────────────────┘

If any count went negative, or if the lengths differed, the answer
would be False. Counting reduces "same letters?" to "same tallies?"
```

---

## Common Pitfalls

### Pitfall 1: Mutating a Map While Iterating Over It

Adding or deleting keys during a `for key in map` loop raises a runtime error in most languages (and silently corrupts in some). If you must remove entries based on counts, iterate over a snapshot of the keys.

```python
for key in list(freq.keys()):   # snapshot first
    if freq[key] == 0:
        del freq[key]
```

### Pitfall 2: Counting When You Only Need Membership (or Vice Versa)

A set cannot answer "how many times?" and a frequency map is wasteful when you only need "yes/no." Match the structure to the question. Using `Counter` for a pure duplicate check works but allocates counts you never read.

### Pitfall 3: Equality and Hashing of Keys

A hash map can only find a key if that key hashes and compares equal to what you stored. Mutable types (lists in Python) are unhashable. Composite keys must be made hashable and canonical — for grouping anagrams, sort the characters or use a count tuple so `"abc"` and `"bca"` map to the same key. If your keys are custom objects, ensure their equality and hash definitions agree.

### Pitfall 4: Reaching for Hashing When Sorting or Two Pointers Fits Better

Hashing costs O(n) extra space and gives unordered results. When the input is already sorted, or when the problem asks for the *k* smallest, a contiguous range, or output in order, sorting plus two pointers is often cleaner and uses O(1) extra space. The strict-majority problem is the sharpest example: Boyer-Moore voting beats a frequency map on space. Reach for a map when the data is unordered and you need fast membership or counts; reach for sorting when order itself carries the answer.

---

## Practice Progression

Master hashing through this sequence of Grind75 problems:

1. **Two Sum** — the canonical complement lookup. Store seen values, query for `target - x`.
2. **Contains Duplicate** — the seen-set in its purest form. Check before insert, or compare set size to length.
3. **Valid Anagram** — build a frequency map of one string, subtract the other, verify all counts return to zero.
4. **Ransom Note** — frequency map as a budget. Count letters in the magazine, then subtract the note; if any count goes negative, you cannot build it. This is counter subtraction.
5. **Longest Palindrome** — frequency *parity* counting. Every character used in pairs contributes to the palindrome; at most one odd-count character sits in the center. Count, then sum the even portions.
6. **Majority Element** — frequency map for the straightforward solution, then Boyer-Moore voting for the O(1)-space refinement.

The arc moves from membership (Contains Duplicate) to complement lookup (Two Sum) to counting (Anagram, Ransom Note, Longest Palindrome) and finally to the space-free counting trick (Majority Element).

---

## The Unifying Principle

Hashing is about **answering questions about the past in constant time** by paying for memory.

Whether the question is *"have I seen this?"*, *"who completes this pair?"*, or *"how many of each?"*, the move is the same: walk the data once, record what matters in a structure you can query instantly, and let the lookup do the work a second scan would have done.

When the data is unordered and you find yourself wanting to search it again, that itch is the signal. Build the index. Ask the question. Move on.

> *"Don't search twice. Remember once, and recall instantly."*

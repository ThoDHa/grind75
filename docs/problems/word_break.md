# [Word Break](https://leetcode.com/problems/word-break/)

**Medium** | **30 minutes** | **Array, Hash Table, String, Dynamic Programming, Trie, Memoization**

**Pattern:** [DP 1D Linear](../patterns/dp_1d_linear/intuition.md), [Trie](../patterns/trie/intuition.md)

**Practice:** [`practice/word_break/solution.py`](../../practice/word_break/solution.py)

Given a string `s` and a dictionary of strings `wordDict`, return `true` if `s` can be segmented into a space-separated sequence of one or more dictionary words.

**Note** that the same word in the dictionary may be reused multiple times in the segmentation.

## Examples

### Example 1

**Input:** `s = "leetcode"`, `wordDict = ["leet","code"]`

**Output:** `true`

**Explanation:** Return true because `"leetcode"` can be segmented as `"leet code"`.

### Example 2

**Input:** `s = "applepenapple"`, `wordDict = ["apple","pen"]`

**Output:** `true`

**Explanation:** Return true because `"applepenapple"` can be segmented as `"apple pen apple"`.
Note that you are allowed to reuse a dictionary word.

### Example 3

**Input:** `s = "catsandog"`, `wordDict = ["cats","dog","sand","and","cat"]`

**Output:** `false`

## Constraints

- `1 <= s.length <= 300`
- `1 <= wordDict.length <= 1000`
- `1 <= wordDict[i].length <= 20`
- `s` and `wordDict[i]` consist of only lowercase English letters.
- All the strings of `wordDict` are **unique**.

## Solutions

### Brute Force Recursion

```python
class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        word_set = set(wordDict)

        def backtrack(start_index):
            # Base case: reached end of string
            if start_index == len(s):
                return True

            # Try all possible words starting from current index
            for end_index in range(start_index + 1, len(s) + 1):
                current_word = s[start_index:end_index]

                # If current word is valid and rest can be segmented
                if current_word in word_set and backtrack(end_index):
                    return True

            return False

        return backtrack(0)
```

#### Approach

This naive recursive approach explores all possible segmentations without memoization. While correct, it has exponential time complexity due to overlapping subproblems being solved multiple times.

1. From the current `start_index`, try every possible word boundary `end_index`.
2. If `s[start_index:end_index]` is a dictionary word, recurse on the remaining suffix.
3. Return `True` as soon as any branch reaches the end of the string.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(2^n)`

In the worst case, we might explore all possible ways to partition the string, leading to exponential time.

##### Space Complexity: `O(n)`

Space for the recursion stack, which can be up to n levels deep.

#### Key Insights

- Every prefix that matches a dictionary word spawns an independent subproblem on the remaining suffix.
- Without caching, the same suffix positions are re-explored along many different prefixes, which is the source of the exponential blowup.
- This formulation makes the recursive structure explicit, which is the foundation every faster approach optimizes.

#### Walkthrough

Let us watch the Brute Force Recursion run on Example 1: `s = "leetcode"`, `wordDict = ["leet","code"]`. First, `word_set` becomes `{"leet", "code"}`, then we call `backtrack(0)`. Each call asks the question "can `s[start_index:]` be segmented?" and tries every word boundary from the current index.

The recursion forms a call tree. Each call scans `end_index` from `start_index + 1` upward, slicing `current_word = s[start_index:end_index]`, and only recurses when that slice is in `word_set`:

```
backtrack(0)            s[0:] = "leetcode"
  end_index runs 1..8, slicing "l", "le", "lee", then "leet"
  "leet" is in word_set: recurse on the remaining suffix
  └─ backtrack(4)       s[4:] = "code"
       end_index runs 5..8, slicing "c", "co", "cod", then "code"
       "code" is in word_set: recurse on the remaining suffix
       └─ backtrack(8)  s[8:] = ""
            start_index == len(s), so return True   ← base case
       └─ returns True, so backtrack(4) returns True
  └─ returns True, so backtrack(0) returns True
```

Tracing how each call resolves and how the `True` propagates back up:

| Call | `s[start_index:]` | First valid word found | Recursive result | Returns |
| --- | --- | --- | --- | --- |
| `backtrack(0)` | `"leetcode"` | `"leet"` at `end_index = 4` | `backtrack(4)` is `True` | `True` |
| `backtrack(4)` | `"code"` | `"code"` at `end_index = 8` | `backtrack(8)` is `True` | `True` |
| `backtrack(8)` | `""` | (base case: `start_index == len(s)`) | none | `True` |

The deepest call hits the base case because `start_index` reached `len(s) = 8`, meaning the whole string was consumed exactly. That `True` flows back up: `backtrack(4)` returns `True` the moment its `"code"` branch succeeds, and `backtrack(0)` returns `True` the moment its `"leet"` branch succeeds. The final returned value is `True`, which matches the expected Output for Example 1.

### BFS

```python
from collections import deque

class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        word_set = set(wordDict)
        queue = deque([0])  # Start from index 0
        visited = set()     # Track visited indices to avoid cycles

        while queue:
            start_index = queue.popleft()

            # Skip if we've already processed this index
            if start_index in visited:
                continue
            visited.add(start_index)

            # Try all possible words starting from current index
            for end_index in range(start_index + 1, len(s) + 1):
                # If we reached the end of string, segmentation is possible
                if end_index == len(s) and s[start_index:end_index] in word_set:
                    return True

                # If current word is valid, add end_index to queue
                if s[start_index:end_index] in word_set:
                    queue.append(end_index)

        return False
```

#### Approach

This BFS approach treats the problem as finding a path from index 0 to index len(s) in a graph where:
- Each valid starting position is a node
- There's an edge from position i to position j if s[i:j] is in the dictionary

BFS explores all reachable positions level by level until it either finds a path to the end or exhausts all possibilities.

1. Start a queue holding only index `0` and a visited set to avoid revisiting positions.
2. Pop an index, and for every valid word starting there, enqueue the resulting end index.
3. If any path reaches `len(s)`, the string can be segmented.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n² + m × k)`

In the worst case, we visit each index once and try all possible word endings from each index.

##### Space Complexity: `O(n + m × k)`

Space for the queue, visited set, and word set.

#### Key Insights

- The visited set is essential: without it, the same index can be enqueued repeatedly and the search degenerates toward the exponential brute force.
- Reachability is all that matters here, so BFS and DFS are interchangeable for correctness; BFS naturally lends itself to recovering a shortest segmentation if one were needed.
- Each index is processed at most once, which bounds the work and mirrors the memoized formulations.

### Top-Down Memoization

```python
class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        word_set = set(wordDict)
        memo = {}

        def dp(start_index):
            # Base case: reached end of string
            if start_index == len(s):
                return True

            # Check if result is already computed
            if start_index in memo:
                return memo[start_index]

            # Try all possible words starting from current index
            for end_index in range(start_index + 1, len(s) + 1):
                current_word = s[start_index:end_index]

                # If current word is in dictionary and rest can be segmented
                if current_word in word_set and dp(end_index):
                    memo[start_index] = True
                    return True

            # No valid segmentation found from this index
            memo[start_index] = False
            return False

        return dp(0)
```

#### Approach

This top-down approach uses recursion with memoization. Starting from index 0, we try all possible words that can start at the current position. If we find a valid word in the dictionary, we recursively check if the remaining string can be segmented.

The memoization cache stores results for each starting index, preventing redundant computation of the same subproblems.

1. Define `dp(start_index)` as "can `s[start_index:]` be segmented?".
2. On entry, return the cached answer if this index was already computed.
3. Try each valid word at the current index and recurse on the remainder, caching the result before returning.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n² + m × k)`

Each unique starting index (n positions) is computed at most once. For each position, we try all possible ending positions (O(n)), and each dictionary lookup takes O(k) time.

##### Space Complexity: `O(n + m × k)`

O(n) for memoization cache and recursion stack, plus O(m × k) for the word set.

#### Key Insights

- Memoization converts the brute force's exponential tree into a linear set of distinct subproblems, one per starting index.
- It is the same recurrence as the bottom-up DP, only evaluated lazily and in suffix orientation rather than prefix orientation.
- The cache makes the overlapping-subproblems structure explicit, which is the defining property that makes dynamic programming applicable.

### Bottom-Up DP

```python
class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        # Convert to set for O(1) lookup
        word_set = set(wordDict)
        n = len(s)

        # dp[i] = True if s[0:i] can be segmented into dictionary words
        dp = [False] * (n + 1)
        dp[0] = True  # Base case: empty string can always be segmented

        # For each ending position i in string s
        for i in range(1, n + 1):
            # Try all possible starting positions j for the last word
            for j in range(i):
                # If s[0:j] can be segmented AND s[j:i] is in dictionary
                if dp[j] and s[j:i] in word_set:
                    dp[i] = True
                    break  # Found valid segmentation, no need to check further

        return dp[n]
```

#### Approach

This bottom-up DP solution builds up the answer for all prefixes of the string. For each position `i`, we check if there's any valid split where the prefix before position `j` can be segmented (dp[j] = True) and the substring from `j` to `i` is in the dictionary.

The key insight is that `dp[i]` represents whether the substring `s[0:i]` can be segmented. We can compute this by trying all possible positions `j < i` where we could place the last word boundary.

The recurrence relation is: `dp[i] = True` if there exists `j < i` such that `dp[j] = True` and `s[j:i]` is in the dictionary.

1. Initialize `dp[0] = True` because the empty prefix is trivially segmentable.
2. For each end position `i`, scan candidate split points `j` and check whether `dp[j]` holds and `s[j:i]` is a word.
3. Break on the first valid split, and return `dp[n]` as the final answer.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n² + m × k)`

Where n is the length of string s, m is the number of words in wordDict, and k is the average length of words. The nested loop takes O(n²), and each substring operation and dictionary lookup takes O(k) time. Converting wordDict to a set takes O(m × k).

##### Space Complexity: `O(n + m × k)`

O(n) for the DP array, plus O(m × k) for storing the word set.

#### Key Insights

- Iterating end positions in increasing order guarantees that every `dp[j]` the transition depends on is already finalized.
- The early `break` stops scanning split points as soon as `dp[i]` is established, since one valid segmentation is enough.
- The prefix-oriented state `dp[i]` (can `s[0:i]` be segmented) is the iterative mirror of the memoized suffix recurrence.

### Trie-Based DP

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False

class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        # Build Trie from word dictionary
        root = TrieNode()
        for word in wordDict:
            node = root
            for char in word:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
            node.is_word = True

        n = len(s)
        dp = [False] * (n + 1)
        dp[0] = True

        for i in range(n):
            # Only expand from positions we already know are reachable
            if not dp[i]:
                continue

            # Walk the Trie forward over s[i:], marking every word end reachable
            node = root
            for j in range(i, n):
                if s[j] not in node.children:
                    break  # No dictionary word continues past this character

                node = node.children[s[j]]

                if node.is_word:
                    dp[j + 1] = True

        return dp[n]
```

#### Approach

This approach builds a Trie (prefix tree) from the dictionary words, allowing for more efficient word matching. Instead of slicing and hashing every possible substring, we walk the Trie character by character and only continue while the current span remains a valid word prefix.

Starting from each reachable position `i`, we descend the Trie following `s[i], s[i+1], ...`. Whenever we land on a node that marks a complete word, the position just past it becomes reachable. We stop early the moment the next character leaves the Trie, since no dictionary word can extend that span.

1. Build the Trie once from every dictionary word.
2. For each reachable position `i` (where `dp[i]` is `True`), descend the Trie along the suffix `s[i:]`.
3. Mark `dp[j + 1] = True` at every node that completes a word, and break as soon as the path falls off the Trie.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n² + m × k)`

Building the Trie takes O(m × k). The DP portion is O(n²) in the worst case, but the forward Trie walk terminates as soon as the current span stops being a dictionary prefix, which prunes work in practice.

##### Space Complexity: `O(m × k + n)`

The Trie stores all characters from all words, plus the O(n) DP array.

#### Key Insights

- The Trie must be walked forward over `s[i:]` so the descent direction matches the order in which dictionary words were inserted.
- A single forward walk from position `i` discovers every word that starts at `i` at once, instead of testing each candidate length independently.
- The early break on a missing child is the real win: once the current span is not a dictionary prefix, no longer span can be a word either.

## Comparison of Solutions

### Time Complexity

- **Brute Force Recursion**: `O(2^n)` - Without memoization, overlapping subproblems are re-solved, leading to exponential exploration of partitions.
- **BFS**: `O(n² + m×k)` - Each index is visited once and all word endings from it are tried, with O(m×k) for the word set.
- **Top-Down Memoization**: `O(n² + m×k)` - Each of n starting indices is computed once, trying O(n) endings with O(k) lookups, plus O(m×k) to build the set.
- **Bottom-Up DP**: `O(n² + m×k)` - The nested loop over positions is O(n²); each substring slice and lookup costs O(k), and building the word set takes O(m×k).
- **Trie-Based DP**: `O(n² + m×k)` - Building the Trie takes O(m×k) and the DP portion is O(n²) worst case, though the Trie enables early termination.

### Space Complexity

- **Brute Force Recursion**: `O(n)` - Space for the recursion stack, up to n levels deep.
- **BFS**: `O(n + m×k)` - Space for the queue, visited set, and word set.
- **Top-Down Memoization**: `O(n + m×k)` - O(n) for the memo cache and recursion stack, plus O(m×k) for the word set.
- **Bottom-Up DP**: `O(n + m×k)` - O(n) for the DP array plus O(m×k) for the word set.
- **Trie-Based DP**: `O(m×k + n)` - The Trie stores all characters from all words, plus the O(n) DP array.

### Trade-offs

- **Brute Force Recursion**: Simple to understand, but exponential time makes it impractical for real inputs.
- **BFS**: Offers an alternative graph perspective, but carries extra queue overhead.
- **Top-Down Memoization**: Intuitive recursion that only computes the states it needs, at the cost of recursion overhead.
- **Bottom-Up DP**: Iterative with clear logic and optimal complexity, though it checks all substrings.
- **Trie-Based DP**: Can provide early termination when the dictionary shares common prefixes, but has a more complex implementation.

### When to Use Each

- **Brute Force Recursion**: Only for understanding the problem or very small inputs.
- **BFS**: When modeling as a graph problem or when you need to find the actual segmentation path.
- **Top-Down Memoization**: When recursive thinking feels more natural or for problems requiring path reconstruction.
- **Bottom-Up DP (Recommended)**: Best for interviews: optimal time complexity with clear iterative logic.
- **Trie-Based DP**: For optimization when the dictionary is large and has many common prefixes.

### Optimization Notes

- Bottom-Up DP is the recommended solution: it achieves the optimal `O(n² + m×k)` complexity with straightforward iterative logic and is easy to reason about under interview pressure.
- Converting `wordDict` to a set is the single most important optimization across every approach, turning O(m×k) list scans into O(k) average-case lookups.
- The bottom-up loop can break as soon as any valid split is found for position `i`, avoiding redundant work once `dp[i]` is established.
- Avoid the brute-force recursion without memoization: its `O(2^n)` blowup comes purely from re-solving overlapping subproblems, which both DP variants eliminate.

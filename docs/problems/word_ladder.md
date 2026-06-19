# [Word Ladder](https://leetcode.com/problems/word-ladder/)

**Hard** | **45 minutes** | **Hash Table, String, Breadth-First Search**

**Pattern:** [Shortest Path](../patterns/shortest_path/intuition.md)

**Practice:** [`practice/word_ladder/solution.py`](../../practice/word_ladder/solution.py)

A **transformation sequence** from word `beginWord` to word `endWord` using a dictionary `wordList` is a sequence of words `beginWord -> s1 -> s2 -> ... -> sk` such that:

- Every adjacent pair of words differs by a single letter.
- Every `si` for `1 <= i <= k` is in `wordList`. Note that `beginWord` does not need to be in `wordList`.
- `sk == endWord`

Given two words, `beginWord` and `endWord`, and a dictionary `wordList`, return *the **number of words** in the **shortest transformation sequence** from* `beginWord` *to* `endWord`*, or* `0` *if no such sequence exists.*

## Examples

### Example 1

**Input:** `beginWord = "hit"`, `endWord = "cog"`, `wordList = ["hot","dot","dog","lot","log","cog"]`

**Output:** `5`

**Explanation:** One shortest transformation sequence is `"hit" -> "hot" -> "dot" -> "dog" -> "cog"`, which is 5 words long.

### Example 2

**Input:** `beginWord = "hit"`, `endWord = "cog"`, `wordList = ["hot","dot","dog","lot","log"]`

**Output:** `0`

**Explanation:** The endWord `"cog"` is not in wordList, therefore there is no valid transformation sequence.

## Constraints

- `1 <= beginWord.length <= 10`
- `endWord.length == beginWord.length`
- `1 <= wordList.length <= 5000`
- `wordList[i].length == beginWord.length`
- `beginWord`, `endWord`, and `wordList[i]` consist of lowercase English letters.
- `beginWord != endWord`
- All the strings in `wordList` are **unique**.

## Solutions

### BFS with Word-by-Word Comparison

```python
from collections import deque
from typing import List

class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        # If endWord is absent, no transformation can ever reach it.
        if endWord not in wordList:
            return 0

        # Set membership is O(1); the list scan above is the only linear check.
        word_set = set(wordList)

        # Queue holds (word, words_used_so_far); beginWord counts as the first word.
        queue = deque([(beginWord, 1)])
        visited = {beginWord}

        while queue:
            current_word, length = queue.popleft()

            # Try every one-letter change at every position.
            for i in range(len(current_word)):
                for c in "abcdefghijklmnopqrstuvwxyz":
                    if c == current_word[i]:
                        continue

                    new_word = current_word[:i] + c + current_word[i + 1:]

                    if new_word == endWord:
                        return length + 1

                    if new_word in word_set and new_word not in visited:
                        visited.add(new_word)
                        queue.append((new_word, length + 1))

        return 0
```

#### Approach

This solution models the problem as a shortest-path search in an unweighted graph:

1. Each word is a node, and two words share an edge when they differ by exactly one letter.
2. BFS explores the graph level by level, so the first time it reaches `endWord` it has used the fewest possible transformations.
3. For the word at the front of the queue, generate every one-letter variation by replacing each character position with each of the 26 lowercase letters.
4. A generated word is a valid neighbor when it appears in `word_set` and has not been visited. Mark it visited as soon as it is enqueued to prevent revisits.

Because BFS expands all words reachable in one step before any reachable in two, the level at which `endWord` first appears is the shortest transformation length.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(M² × N)`

`M` is the word length and `N` is the number of words. Each of the `N` words is dequeued at most once. For each word we try `M` positions across 26 letters, and building each candidate string with slicing costs `O(M)`. The `26` is a constant, leaving `O(M² × N)`.

##### Space Complexity: `O(M × N)`

The `word_set`, `visited` set, and queue each hold up to `N` words of length `M`, giving `O(M × N)`.

#### Key Insights

- BFS is the natural fit for shortest paths in unweighted graphs because it discovers nodes in order of distance.
- Marking a word visited at enqueue time, not dequeue time, avoids inserting the same word multiple times.
- Generating candidates directly (no preprocessing) keeps the logic simple, at the cost of producing words that may not exist in the dictionary.

### BFS with Pattern Matching

```python
from collections import deque, defaultdict
from typing import List

class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        if endWord not in wordList:
            return 0

        # Group words by wildcard pattern: "hot" -> "*ot", "h*t", "ho*".
        # Words sharing a pattern are exactly one transformation apart.
        pattern_dict = defaultdict(list)

        all_words = wordList + [beginWord]
        for word in all_words:
            for i in range(len(word)):
                pattern = word[:i] + "*" + word[i + 1:]
                pattern_dict[pattern].append(word)

        queue = deque([(beginWord, 1)])
        visited = {beginWord}

        while queue:
            current_word, length = queue.popleft()

            for i in range(len(current_word)):
                pattern = current_word[:i] + "*" + current_word[i + 1:]

                for neighbor in pattern_dict[pattern]:
                    if neighbor == endWord:
                        return length + 1

                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, length + 1))

        return 0
```

#### Approach

This approach precomputes adjacency instead of regenerating neighbors on the fly:

1. For every word, build `M` wildcard patterns by replacing one character at a time with `*`, and group words under each pattern in `pattern_dict`.
2. Two words that share a pattern differ by exactly one letter, so the pattern map encodes the graph's edges.
3. During BFS, look up the current word's patterns and visit every word recorded under them.
4. The first time `endWord` is encountered, return the accumulated length plus one.

By precomputing patterns, the search only ever touches words that actually exist in the dictionary, rather than the full 26-letter expansion at every step.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(M² × N)`

Preprocessing builds `M` patterns per word, each costing `O(M)` to slice, so the pattern dictionary is built in `O(M² × N)`. BFS then visits each word and pattern bucket once, bounded by the same order.

##### Space Complexity: `O(M² × N)`

The pattern dictionary stores `M` patterns per word, each of length `M`, giving `O(M² × N)` in addition to the queue and visited set.

#### Key Insights

- Wildcard patterns turn neighbor discovery into a hash lookup, avoiding the generation of words that are not in the dictionary.
- The tradeoff is higher memory: the pattern map is the dominant space cost.
- Including `beginWord` in the pattern map lets the search start from it even though it need not be in `wordList`.

### DFS with Memoization

```python
from typing import List

class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        if endWord not in wordList:
            return 0

        word_set = set(wordList)
        memo = {}

        def is_one_diff(word1: str, word2: str) -> bool:
            diff_count = 0
            for i in range(len(word1)):
                if word1[i] != word2[i]:
                    diff_count += 1
                    if diff_count > 1:
                        return False
            return diff_count == 1

        def dfs(current_word: str, target_word: str, visited: set) -> float:
            if current_word == target_word:
                return 1

            if (current_word, target_word) in memo:
                return memo[(current_word, target_word)]

            min_length = float("inf")

            for word in word_set:
                if word not in visited and is_one_diff(current_word, word):
                    visited.add(word)
                    result = dfs(word, target_word, visited)
                    if result != float("inf"):
                        min_length = min(min_length, 1 + result)
                    visited.remove(word)

            memo[(current_word, target_word)] = min_length
            return min_length

        result = dfs(beginWord, endWord, {beginWord})
        return result if result != float("inf") else 0
```

#### Approach

This recursive approach explores transformation paths depth-first and caches results:

1. From the current word, scan the dictionary for every word that differs by exactly one character.
2. Recurse into each such neighbor, tracking visited words to avoid cycles on the active path.
3. Combine the best result from any neighbor: the shortest path through this word is one plus the shortest path from its best neighbor.
4. Memoize results per `(current_word, target_word)` pair so repeated subproblems are not recomputed.

DFS is included for contrast. It returns the correct answer, but because depth-first search does not visit nodes in distance order, it may explore long paths before short ones and cannot stop at the first arrival the way BFS does.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(N! × M²)` worst case

Without distance-ordered pruning, DFS can branch into many partial paths. Memoization caches `(current, target)` results but the path-dependent `visited` set limits its effectiveness, so the worst case stays exponential.

##### Space Complexity: `O(N × M + recursion depth)`

The memo cache holds up to `O(N)` entries keyed by word pairs, and the recursion stack can grow as deep as the longest explored path.

#### Key Insights

- DFS reaches the correct answer but is the wrong tool for shortest paths, since it lacks BFS's level-by-level guarantee.
- The `is_one_diff` helper short-circuits once two mismatches are found, so each comparison stops early.
- Memoization keyed on the word pair helps, but path-dependent visited state means it cannot fully tame the exponential blow-up.

### Bidirectional BFS

```python
from typing import List

class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        word_set = set(wordList)
        if endWord not in word_set:
            return 0

        # Two frontiers grow toward each other; visited spans both.
        front = {beginWord}
        back = {endWord}
        visited = {beginWord, endWord}
        m = len(beginWord)
        steps = 1

        while front and back:
            # Always expand the smaller frontier to minimize branching.
            if len(front) > len(back):
                front, back = back, front

            next_front = set()

            for word in front:
                for i in range(m):
                    for c in "abcdefghijklmnopqrstuvwxyz":
                        if c == word[i]:
                            continue

                        neighbor = word[:i] + c + word[i + 1:]

                        # The frontiers meet: this neighbor closes the path.
                        if neighbor in back:
                            return steps + 1

                        if neighbor in word_set and neighbor not in visited:
                            visited.add(neighbor)
                            next_front.add(neighbor)

            front = next_front
            steps += 1

        return 0
```

#### Approach

Bidirectional BFS searches inward from both ends at once:

1. Maintain a `front` set starting at `beginWord` and a `back` set starting at `endWord`, plus a shared `visited` set.
2. On each iteration, expand whichever frontier is smaller so the branching factor stays low.
3. For each word in the active frontier, generate its one-letter variations. If any variation already lies in the opposite frontier, the two searches have met and the answer is `steps + 1`.
4. Otherwise add valid, unvisited variations to the next frontier and increment the step count.

Meeting in the middle halves the effective search depth, which is the dominant factor when the branching factor is high.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(M² × N)`

The worst-case bound matches plain BFS: each word is expanded once, with `M` positions, 26 letters, and `O(M)` slicing per candidate. In practice the meet-in-the-middle search explores far fewer nodes.

##### Space Complexity: `O(M × N)`

The two frontiers and the `visited` set together hold up to `N` words of length `M`, giving `O(M × N)`.

#### Key Insights

- Searching from both ends shrinks the explored space from roughly `b^d` to `2 × b^(d/2)`, where `b` is the branching factor and `d` the depth.
- Always expanding the smaller frontier keeps each step's work minimal and balances the two searches.
- A path is found the moment a generated neighbor appears in the opposite frontier, so the two halves never need to fully meet on a shared node.

## Comparison of Solutions

### Time Complexity

- **BFS with Word-by-Word Comparison**: `O(M² × N)` - each of `N` words tries `M` positions across 26 letters, and each string build costs `O(M)`.
- **BFS with Pattern Matching**: `O(M² × N)` - preprocessing builds all `M`-length patterns in `O(M² × N)`, and BFS traversal stays within the same order.
- **DFS with Memoization**: `O(N! × M²)` worst case - depth-first search can explore exponentially many paths despite memoization.
- **Bidirectional BFS**: `O(M² × N)` - same worst-case bound, but typically much faster in practice from the reduced search space.

### Space Complexity

- **BFS with Word-by-Word Comparison**: `O(M × N)` - for the word set, visited set, and BFS queue.
- **BFS with Pattern Matching**: `O(M² × N)` - the pattern dictionary stores `M` patterns per word, each of length `M`.
- **DFS with Memoization**: `O(N × M + recursion depth)` - for the memoization cache plus a recursion stack that can grow deep.
- **Bidirectional BFS**: `O(M × N)` - for the two frontiers and the shared visited set; in practice less than unidirectional BFS.

### Trade-offs

- **BFS with Word-by-Word Comparison**: Clear and optimal, but generates candidate words that may not exist in the dictionary.
- **BFS with Pattern Matching**: Avoids invalid candidates, at the cost of higher space usage and a preprocessing pass.
- **DFS with Memoization**: Useful for contrast, but performs poorly and does not visit words in distance order.
- **Bidirectional BFS**: Often the fastest in practice, but the dual-frontier bookkeeping is more involved.

### When to Use Each

- **BFS with Word-by-Word Comparison (Recommended)**: The default interview answer - clear, optimal, and correct on every case.
- **BFS with Pattern Matching**: When the word list is large and avoiding invalid candidates matters more than memory.
- **DFS with Memoization**: For understanding why depth-first search is the wrong tool for shortest paths.
- **Bidirectional BFS**: For very large search spaces where the meet-in-the-middle speedup is worth the extra complexity.

### Optimization Notes

- Convert `wordList` to a set for `O(1)` membership checks, and return early when `endWord` is absent to skip all further work.
- Mark words visited at the moment they are enqueued (or added to a frontier) so the same word is never processed twice.
- For very large search spaces, Bidirectional BFS is the strongest optimization, expanding from both ends and always growing the smaller frontier.
- Avoid plain DFS for this problem: it does not find the shortest path first, so its worst case degrades toward `O(N! × M²)` despite memoization.

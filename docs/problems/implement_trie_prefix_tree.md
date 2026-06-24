# [Implement Trie (Prefix Tree)](https://leetcode.com/problems/implement-trie-prefix-tree/)

**Medium** | **30 minutes** | **Hash Table, String, Design, Trie**

**Pattern:** [Trie](../patterns/trie/intuition.md)

**Practice:** [`practice/implement_trie_prefix_tree/solution.py`](../../practice/implement_trie_prefix_tree/solution.py)

A trie (pronounced as "try") or prefix tree is a tree data structure used to efficiently store and retrieve keys in a dataset of strings. There are various applications of this data structure, such as autocomplete and spellchecker.

Implement the Trie class:

- `Trie()` Initializes the trie object.
- `void insert(String word)` Inserts the string `word` into the trie.
- `boolean search(String word)` Returns `true` if the string `word` is in the trie (i.e., was inserted before), and `false` otherwise.
- `boolean startsWith(String prefix)` Returns `true` if there is a previously inserted string `word` that has the prefix `prefix`, and `false` otherwise.

## Examples

### Example 1

**Input:**

```
["Trie", "insert", "search", "search", "startsWith", "insert", "search"]
[[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]]
```

**Output:**

```
[null, null, true, false, true, null, true]
```

**Explanation:**

```
Trie trie = new Trie();
trie.insert("apple");
trie.search("apple");   // return True
trie.search("app");     // return False
trie.startsWith("app"); // return True
trie.insert("app");
trie.search("app");     // return True
```

## Constraints

- `1 <= word.length, prefix.length <= 2000`
- `word` and `prefix` consist only of lowercase English letters.
- At most `3 * 10^4` calls in total will be made to `insert`, `search`, and `startsWith`.

## Solutions

### Brute Force

```python
class Trie:

    def __init__(self):
        # Just remember every inserted word verbatim.
        self.words: list = []

    def insert(self, word: str) -> None:
        self.words.append(word)

    def search(self, word: str) -> bool:
        # A word is present only if it was inserted exactly.
        for stored in self.words:
            if stored == word:
                return True
        return False

    def startsWith(self, prefix: str) -> bool:
        # Any stored word beginning with prefix satisfies the query.
        for stored in self.words:
            if len(stored) >= len(prefix) and stored[: len(prefix)] == prefix:
                return True
        return False


# Your Trie object will be instantiated and used as follows:
# obj = Trie()
# obj.insert(word)
# param_2 = obj.search(word)
# param_3 = obj.startsWith(prefix)
```

#### Approach

Before reaching for any tree structure, the most direct idea is to store every
inserted word in a list and answer each query by scanning that list. No shared
prefixes, no nodes, just a literal record of what was inserted.

1. `insert` appends the word to a running list.
2. `search` scans the list for an entry equal to `word`, returning `True` on an
   exact match.
3. `startsWith` scans the list for any entry whose first `len(prefix)` characters
   equal `prefix`.

This is correct but slow: every query rescans the entire collection and compares
full strings, ignoring the prefix-sharing that makes a trie efficient.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(N × L)` per query

`search` and `startsWith` each compare against all `N` stored words, and each
comparison touches up to `L` characters, so a single query costs `O(N × L)`.
`insert` is `O(1)` amortized.

##### Space Complexity: `O(total characters)`

Every inserted word is kept in full with no prefix sharing, so storage is the sum
of all word lengths.

#### Key Insights

- This is the baseline you write before knowing what a trie is: keep the data,
  scan on demand.
- It wastes the structure inherent in the problem; repeated prefixes are stored
  and compared over and over instead of being shared.
- The linear scan per query is exactly what a trie removes by walking one node per
  character regardless of how many words are stored.

### Dictionary Children

```python
class Trie:

    def __init__(self):
        # Each node is a dict of child character -> child node.
        # The sentinel key "$" marks the end of a complete word.
        self.root: dict = {}

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node["$"] = True

    def search(self, word: str) -> bool:
        node = self._find(word)
        return node is not None and "$" in node

    def startsWith(self, prefix: str) -> bool:
        return self._find(prefix) is not None

    def _find(self, s: str) -> dict | None:
        # Walk down the trie following s; return the node reached or None.
        node = self.root
        for ch in s:
            if ch not in node:
                return None
            node = node[ch]
        return node


# Your Trie object will be instantiated and used as follows:
# obj = Trie()
# obj.insert(word)
# param_2 = obj.search(word)
# param_3 = obj.startsWith(prefix)
```

#### Approach

A trie stores strings character by character along tree paths, so shared
prefixes share nodes. Representing each node as a dictionary mapping a character
to its child node keeps the implementation compact while giving constant-time
child access.

1. Each node is a `dict`. A child entry maps a character to the next node; a
   special sentinel key `"$"` flags that a complete word ends at this node.
2. `insert` walks the characters of `word`, creating missing child dicts via
   `setdefault`, then sets the sentinel on the final node.
3. `search` walks the word with the `_find` helper; it returns `True` only when
   the path exists and the terminal node carries the `"$"` sentinel.
4. `startsWith` reuses `_find`; reaching any node along the prefix path is enough,
   regardless of whether a word ends there.

The sentinel distinguishes a full word from a mere prefix, which is what makes
`search("app")` return `False` until `"app"` is explicitly inserted.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(L)` per operation

`insert`, `search`, and `startsWith` each traverse one node per character of the
input string of length `L`, performing constant-time dictionary work at each
step.

##### Space Complexity: `O(total characters)`

In the worst case, with no shared prefixes, each inserted character creates a new
node, so storage is proportional to the sum of all inserted word lengths. Shared
prefixes reduce this in practice.

#### Key Insights

- A dictionary per node gives `O(1)` child lookup over the 26-letter alphabet
  without preallocating fixed-size arrays.
- The `"$"` sentinel cleanly separates "a word ends here" from "this is only a
  prefix," which is the crux of correct `search` versus `startsWith` behavior.
- `setdefault` collapses the "create child if absent, then descend" pattern into
  a single expression.
- Factoring the shared descent into `_find` removes duplication between `search`
  and `startsWith`.

### Fixed Array Children

```python
class TrieNode:

    def __init__(self):
        # One slot per lowercase letter; None means no child along that edge.
        self.children: list = [None] * 26
        # Marks whether a complete word ends at this node.
        self.is_end: bool = False


class Trie:

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            index = ord(ch) - ord("a")
            if node.children[index] is None:
                node.children[index] = TrieNode()
            node = node.children[index]
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self._find(word)
        return node is not None and node.is_end

    def startsWith(self, prefix: str) -> bool:
        return self._find(prefix) is not None

    def _find(self, s: str) -> "TrieNode | None":
        # Walk down the trie following s; return the node reached or None.
        node = self.root
        for ch in s:
            index = ord(ch) - ord("a")
            if node.children[index] is None:
                return None
            node = node.children[index]
        return node


# Your Trie object will be instantiated and used as follows:
# obj = Trie()
# obj.insert(word)
# param_2 = obj.search(word)
# param_3 = obj.startsWith(prefix)
```

#### Approach

This variant stores each node's children in a fixed-size list of 26 slots, one
per lowercase letter, instead of a dictionary. The letter `ch` maps to index
`ord(ch) - ord("a")`, and a dedicated `is_end` boolean replaces the sentinel
key.

1. Each `TrieNode` holds a 26-element list initialized to `None` and an `is_end`
   flag that is `False` until a word terminates there.
2. `insert` converts each character to its slot index, creating a child node when
   the slot is empty, then marks the final node as a word end.
3. `search` walks the word via the `_find` helper and checks that the reached
   node has `is_end` set.
4. `startsWith` reuses `_find`; any reachable node along the prefix path suffices.

Indexing into a contiguous array is the fastest possible child lookup, which is
why this layout is common in performance-sensitive trie implementations.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(L)` per operation

`insert`, `search`, and `startsWith` each visit one node per character of the
input string of length `L`, with constant-time array indexing at each step.

##### Space Complexity: `O(26 × number of nodes)`

Every node allocates a full 26-slot array regardless of how many children it
actually has, so memory is proportional to the node count times the alphabet
size. This is wasteful for sparse tries but bounded and predictable.

#### Key Insights

- Array indexing by `ord(ch) - ord("a")` gives the tightest constant-factor child
  lookup, avoiding hashing entirely.
- A separate `is_end` flag plays the same role as the dictionary sentinel,
  distinguishing a stored word from a mere prefix.
- The fixed alphabet size is what makes the array layout viable; it relies on the
  constraint that inputs contain only lowercase English letters.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(N × L)` per `search`/`startsWith` query - scans all `N` stored words, comparing up to `L` characters each
- **Dictionary Children**: `O(L)` per operation, with constant-time hashed child lookup at each character
- **Fixed Array Children**: `O(L)` per operation, with constant-time array indexing at each character

### Space Complexity

- **Brute Force**: `O(total characters)` - stores every word in full with no prefix sharing
- **Dictionary Children**: `O(total characters)` - each node stores only the children it actually has
- **Fixed Array Children**: `O(26 × number of nodes)` - each node reserves a full 26-slot array even when mostly empty

### Trade-offs

- **Brute Force** is trivial to write and uses no tree at all, but each query rescans the entire collection, which fails the call-volume constraints at scale
- **Dictionary Children** is memory-efficient for sparse tries and adapts to any character set without changes, at the cost of hashing overhead per lookup
- **Fixed Array Children** offers the fastest possible child access through direct indexing, but wastes memory on empty slots and is tied to a fixed alphabet

### When to Use Each

- **Brute Force**: Only as a conceptual baseline; the per-query scan is too slow for the problem's call volume
- **Dictionary Children**: The default choice when the alphabet is large or unknown, or when tries are sparse and memory matters
- **Fixed Array Children**: When the alphabet is small and fixed (such as lowercase English letters) and raw lookup speed is the priority

### Optimization Notes

- The trie's whole point is replacing the Brute Force per-query scan with a walk of one node per character, making query cost depend on the query length `L` rather than the number of stored words `N`
- Both trie layouts share the same `O(L)` time complexity; the real distinction is the constant factor on lookups versus the memory footprint per node
- The array layout trades memory for speed, which pays off in hot paths over a small fixed alphabet but becomes prohibitive for Unicode-scale character sets
- The dictionary layout generalizes for free to any character set, making it the safer default unless profiling shows child lookup is a bottleneck

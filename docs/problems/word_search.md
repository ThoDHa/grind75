# [Word Search](https://leetcode.com/problems/word-search/)

**Medium** | **30 minutes** | **Array, Backtracking, Matrix**

**Pattern:** [Graph Traversal](../patterns/graph/intuition.md), [Backtracking](../patterns/backtracking_exploration/intuition.md)

**Practice:** [`practice/word_search/solution.py`](https://github.com/ThoDHa/grind75/blob/main/practice/word_search/solution.py)

Given an `m x n` grid of characters `board` and a string `word`, return `true` if `word` exists in the grid.

The word can be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once.

## Examples

### Example 1

![Word Search](assets/word_search_example1.jpg)

**Input:** `board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]`, `word = "ABCCED"`

**Output:** `true`

### Example 2

![Word Search](assets/word_search_example2.jpg)

**Input:** `board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]`, `word = "SEE"`

**Output:** `true`

### Example 3

![Word Search](assets/word_search_example3.jpg)

**Input:** `board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]]`, `word = "ABCB"`

**Output:** `false`

## Constraints

- `m == board.length`
- `n = board[i].length`
- `1 <= m, n <= 6`
- `1 <= word.length <= 15`
- `board` and `word` consists of only lowercase and uppercase English letters.

## Follow up

Could you use search pruning to make your solution faster with a larger `board`?

## Solutions

### DFS Backtracking

```python
class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        rows, cols = len(board), len(board[0])

        def dfs(r: int, c: int, i: int) -> bool:
            # Matched every character: the word exists.
            if i == len(word):
                return True
            # Out of bounds or the cell does not match the needed letter.
            if (r < 0 or r >= rows or c < 0 or c >= cols or
                    board[r][c] != word[i]):
                return False

            # Mark this cell used so the same letter is not reused on this path.
            saved = board[r][c]
            board[r][c] = "#"

            found = (dfs(r + 1, c, i + 1) or
                     dfs(r - 1, c, i + 1) or
                     dfs(r, c + 1, i + 1) or
                     dfs(r, c - 1, i + 1))

            # Restore the cell for other search paths (backtrack).
            board[r][c] = saved
            return found

        # Try starting the search from every cell.
        for r in range(rows):
            for c in range(cols):
                if dfs(r, c, 0):
                    return True
        return False
```

#### Approach

Each path that spells `word` is a self-avoiding walk through the grid, so we
explore those walks with depth-first search and undo our choices on the way back
up (backtracking). The index `i` tracks how many characters of `word` we have
matched so far along the current path.

1. From every cell, launch a DFS that tries to match `word[i]` at the current
   cell.
2. If `i` has reached `len(word)`, every character matched and we return `True`.
3. If the cell is off the board or its letter is not `word[i]`, this path fails.
4. Otherwise, temporarily overwrite the cell with a sentinel (`"#"`) so it cannot
   be reused later on the same path, then recurse into the four neighbors for
   `word[i + 1]`.
5. Restore the original letter before returning so sibling and ancestor searches
   can use that cell freely. This restoration is the backtracking step.

Overwriting the cell in place serves as an O(1) visited marker that is scoped to
the current path, which is exactly what "the same letter cell may not be used
more than once" requires.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n × 4^L)`

Let `L` be the length of `word`. Each of the `m × n` starting cells can branch
into up to four directions at every step, and a path has up to `L` steps. The
first step has four choices and each subsequent step has at most three (we never
walk straight back), so the bound is `O(m × n × 4^L)`. The matching-letter check
prunes most branches in practice, but this is the worst case.

##### Space Complexity: `O(L)`

The recursion depth is bounded by the word length, since each frame matches one
additional character. We mutate the board in place rather than allocating a
separate visited matrix, so no extra grid-sized storage is used.

#### Key Insights

- Mutating the cell to a sentinel and restoring it gives a per-path visited mark
  in O(1) space, avoiding a separate boolean grid.
- The letter-match check at the top of `dfs` prunes aggressively: a branch dies
  the moment a cell does not match the next required character.
- Restoring `board[r][c]` before returning is essential; skipping it would leak
  the `"#"` marker into other search paths and produce wrong answers.
- Checking `i == len(word)` before the bounds check lets the final character
  match succeed even when it sits on the board edge.
- For the follow-up, search pruning (for example, counting letter frequencies in
  the board versus the word, or reversing the word to start from the rarer end)
  cuts wasted exploration on larger boards.

### DFS with Visited Set

```python
class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        rows, cols = len(board), len(board[0])
        visited = set()

        def dfs(r: int, c: int, i: int) -> bool:
            # Matched every character: the word exists.
            if i == len(word):
                return True
            # Out of bounds, already on this path, or wrong letter.
            if (r < 0 or r >= rows or c < 0 or c >= cols or
                    (r, c) in visited or board[r][c] != word[i]):
                return False

            # Record the cell as used for the current path.
            visited.add((r, c))

            found = (dfs(r + 1, c, i + 1) or
                     dfs(r - 1, c, i + 1) or
                     dfs(r, c + 1, i + 1) or
                     dfs(r, c - 1, i + 1))

            # Release the cell so other paths may use it (backtrack).
            visited.remove((r, c))
            return found

        for r in range(rows):
            for c in range(cols):
                if dfs(r, c, 0):
                    return True
        return False
```

#### Approach

This is the same depth-first backtracking search, but it tracks used cells in an
explicit `set` of `(row, col)` coordinates rather than mutating the board. Keeping
the visited state separate from the data is often clearer and is the right move
when the input must not be modified, even temporarily.

1. From every cell, launch a DFS that tries to match `word[i]` at the current
   cell.
2. If `i` has reached `len(word)`, every character matched and we return `True`.
3. If the cell is off the board, already in `visited`, or its letter is not
   `word[i]`, this path fails.
4. Otherwise, add `(r, c)` to `visited`, recurse into the four neighbors for
   `word[i + 1]`, and remove `(r, c)` on the way back up.

The `set` membership check replaces the sentinel overwrite as the "used on this
path" test, so the board is never altered.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n × 4^L)`

Identical to the in-place variant. Each of the `m × n` starting cells branches
into up to four directions per step over a path of up to `L` steps, giving
`O(m × n × 4^L)` in the worst case before letter-mismatch pruning trims branches.

##### Space Complexity: `O(L)`

The recursion stack is bounded by `L`, and the `visited` set holds at most `L`
coordinates at once because entries are removed on backtrack. This is a constant
factor more memory than the in-place approach but the same asymptotic bound.

#### Key Insights

- A separate `visited` set keeps the input immutable, which matters when the
  board is shared, read-only, or accessed concurrently.
- Adding and removing the coordinate must bracket the recursive calls exactly,
  mirroring the choose/unchoose structure of backtracking.
- The set never exceeds `L` entries, so the extra space is proportional to the
  word length, not the board size.

### DFS with Frequency Pruning

```python
from collections import Counter


class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        rows, cols = len(board), len(board[0])

        # Fast fail: the board must contain enough of every letter in word.
        board_counts = Counter(ch for row in board for ch in row)
        word_counts = Counter(word)
        for ch, need in word_counts.items():
            if board_counts[ch] < need:
                return False

        # Start from the rarer end so the first letter has fewer launch points.
        if word_counts[word[-1]] < word_counts[word[0]]:
            word = word[::-1]

        def dfs(r: int, c: int, i: int) -> bool:
            if i == len(word):
                return True
            if (r < 0 or r >= rows or c < 0 or c >= cols or
                    board[r][c] != word[i]):
                return False

            saved = board[r][c]
            board[r][c] = "#"

            found = (dfs(r + 1, c, i + 1) or
                     dfs(r - 1, c, i + 1) or
                     dfs(r, c + 1, i + 1) or
                     dfs(r, c - 1, i + 1))

            board[r][c] = saved
            return found

        for r in range(rows):
            for c in range(cols):
                if dfs(r, c, 0):
                    return True
        return False
```

#### Approach

This answers the follow-up by adding two cheap prunes around the same in-place
DFS. Neither prune changes the set of reachable answers; they only avoid work the
plain search would eventually waste.

1. Build a letter-frequency table of the board and of `word`. If the board lacks
   enough copies of any required letter, no path can exist, so return `False`
   immediately without any DFS.
2. Compare how often `word`'s first and last letters appear in `word` itself, and
   reverse `word` when the last letter is rarer. Searching from the rarer end
   means fewer cells qualify as starting points, which prunes the top of the
   search tree where branching is most expensive.
3. Run the in-place sentinel DFS exactly as before.

The `Counter` here only powers an optional precheck and the symmetric reversal
decision; the core search is hand-written, so the algorithm does not depend on a
library to do its real work.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m × n × 4^L)`

The worst-case bound is unchanged because the prunes can fail to eliminate
anything (for example, a uniform board). The frequency precheck costs
`O(m × n + L)`, which is dominated by the search. In practice the prunes can turn
a near-timeout into an instant answer on adversarial inputs.

##### Space Complexity: `O(L + Σ)`

Recursion depth is `O(L)` as before. The two counters add `O(Σ)` space, where `Σ`
is the alphabet size (at most 52 here), so the extra storage is effectively
constant.

#### Key Insights

- The letter-count precheck rejects impossible words in linear time before any
  recursion, which is the cheapest possible prune.
- Starting from the rarer end of the word shrinks the number of DFS launch points
  and is a classic backtracking optimization for symmetric search.
- The prunes are heuristics layered on top of the base algorithm: they speed up
  common adversarial cases without affecting correctness or the worst-case bound.

## Comparison of Solutions

### Time Complexity

- **DFS Backtracking**: `O(m × n × 4^L)` - up to four branches per step over an
  `L`-length path from each of `m × n` starts.
- **DFS with Visited Set**: `O(m × n × 4^L)` - same search tree, with a set
  lookup replacing the sentinel check.
- **DFS with Frequency Pruning**: `O(m × n × 4^L)` - same worst case, with prunes
  that often help in practice.

### Space Complexity

- **DFS Backtracking**: `O(L)` - recursion depth only; the board doubles as the
  visited marker.
- **DFS with Visited Set**: `O(L)` - recursion depth plus a set of at most `L`
  coordinates.
- **DFS with Frequency Pruning**: `O(L + Σ)` - recursion depth plus two
  fixed-alphabet counters.

### Trade-offs

- **DFS Backtracking** uses the least memory but mutates the board mid-search
  (restoring it before returning), which is unacceptable if the input is
  read-only or shared.
- **DFS with Visited Set** leaves the input untouched at the cost of a small
  auxiliary set and slightly slower membership checks.
- **DFS with Frequency Pruning** adds setup cost and code for a large speedup on
  adversarial boards, without improving the asymptotic bound.

### When to Use Each

- **DFS Backtracking**: The default interview answer when mutating the board
  temporarily is allowed.
- **DFS with Visited Set**: When the board must stay immutable, or when separating
  state from data makes the code clearer.
- **DFS with Frequency Pruning**: The follow-up answer for larger boards or when
  many queries run against the same grid (Recommended when inputs are
  adversarial).

### Optimization Notes

- The sentinel `"#"` works only because it is guaranteed not to appear in `word`;
  for arbitrary alphabets, prefer the visited set.
- Checking `i == len(word)` before the bounds check lets a final character on the
  board edge match correctly.
- The frequency precheck and rarer-end reversal are independent prunes; either can
  be applied alone, and both leave correctness intact.

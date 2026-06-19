# [First Bad Version](https://leetcode.com/problems/first-bad-version/)

**Easy** | **15 minutes** | **Binary Search**

**Pattern:** [Binary Search](../patterns/binary_search/intuition.md)

**Practice:** [`practice/first_bad_version/solution.py`](../../practice/first_bad_version/solution.py)

You are a product manager and currently leading a team to develop a new product. Unfortunately, the latest version of your product fails the quality check. Since each version is developed based on the previous version, all the versions after a bad version are also bad.

Suppose you have n versions [1, 2, ..., n] and you want to find out the first bad one, which causes all the following ones to be bad.

You are given an API `bool isBadVersion(version)` which returns whether `version` is bad. Implement a function to find the first bad version. You should minimize the number of calls to the API.

## Examples

### Example 1

**Input:** `n = 5`, `bad = 4`
**Output:** `4`
**Explanation:**
call isBadVersion(3) -> `false`
call isBadVersion(5) -> `true`
call isBadVersion(4) -> `true`
Then `4` is the first bad version.

### Example 2

**Input:** `n = 1`, `bad = 1`
**Output:** `1`

## Constraints

- `1 <= bad <= n <= 2³¹ - 1`

## Solutions

### Linear Scan

```python
# The isBadVersion API is already defined for you.
# def isBadVersion(version: int) -> bool:

class Solution:
    def firstBadVersion(self, n: int) -> int:
        for version in range(1, n + 1):
            if isBadVersion(version):
                return version
        return -1
```

#### Approach

The most direct reading of the problem: walk the versions in order and return
the first one the API reports as bad. Because every version after a bad version
is also bad, the first `True` the scan encounters is the boundary we want.

1. Iterate `version` from `1` to `n`.
2. Call `isBadVersion(version)` on each.
3. Return the first `version` for which the API returns `True`.

The constraints guarantee at least one bad version exists, so the loop always
returns before falling through; the trailing `return -1` only guards against an
empty range.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

In the worst case the bad boundary sits at version `n`, so the scan makes `n`
API calls. With `n` as large as `2³¹ - 1`, that is billions of calls, which is
exactly what the problem asks us to avoid.

##### Space Complexity: `O(1)`

Only a single loop variable is tracked regardless of input size.

#### Key Insights

- This is the baseline that proves correctness: the first `True` is the answer.
- It maximizes API calls rather than minimizing them, so it fails the problem's
  optimization goal and exists mainly as a reference point.
- It would also time out on the upper end of the constraints.

### Binary Search

```python
# The isBadVersion API is already defined for you.
# def isBadVersion(version: int) -> bool:

class Solution:
    def firstBadVersion(self, n: int) -> int:
        lo, hi = 1, n
        while lo < hi:
            mid = lo + (hi - lo) // 2
            if isBadVersion(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo
```

#### Approach

The version sequence is monotonic: once versions go bad they stay bad, so the
`isBadVersion` results form `False, False, ..., False, True, True, ..., True`.
That is a sorted boolean array, and finding the first `True` is a textbook
binary search for the left boundary.

1. Maintain a half-open search on `[lo, hi]`, starting at `lo = 1`, `hi = n`.
2. While `lo < hi`, compute `mid = lo + (hi - lo) // 2`.
3. If `mid` is bad, the answer is `mid` or earlier, so set `hi = mid` (keep
   `mid` in the candidate range).
4. If `mid` is good, the answer is strictly after `mid`, so set `lo = mid + 1`.
5. When `lo == hi` the range has collapsed onto the first bad version; return it.

The invariant is that the first bad version always lies in `[lo, hi]`. Each
iteration shrinks the range while preserving that invariant, and because the
bad version is guaranteed to exist, the range converges onto it rather than past
it.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(log n)`

Each iteration halves the candidate range, so the loop runs at most `⌈log₂ n⌉`
times and makes that many API calls. This is optimal: distinguishing the
boundary requires at least logarithmically many queries.

##### Space Complexity: `O(1)`

Only the `lo`, `hi`, and `mid` integers are stored.

#### Key Insights

- Computing `mid = lo + (hi - lo) // 2` avoids the overflow that `(lo + hi) // 2`
  could cause when `n` approaches `2³¹ - 1` in fixed-width integer languages.
- Setting `hi = mid` (not `mid - 1`) is essential: `mid` itself may be the
  answer, so it must stay inside the range.
- The `lo < hi` loop condition with a collapsing range removes the need for a
  separate "found it" check; convergence is the answer.

### Bisect

```python
import bisect

# The isBadVersion API is already defined for you.
# def isBadVersion(version: int) -> bool:

class Solution:
    def firstBadVersion(self, n: int) -> int:
        return bisect.bisect_left(range(n + 1), True, lo=1, key=isBadVersion)
```

#### Approach

`bisect.bisect_left` already performs the left-boundary binary search. Treating
the versions as a virtual sorted sequence whose key is `isBadVersion`, the
predicate maps to `False < True`, so the leftmost insertion point of `True` is
the first bad version.

1. Use `range(n + 1)` as the implicit array of version numbers (index equals
   version).
2. Pass `key=isBadVersion` so `bisect` compares on the boolean each version maps
   to.
3. Restrict the search to versions `1..n` with `lo=1`.
4. Return the insertion point, which is the first version whose key is `True`.

The `range` is lazy, so no array is materialized; `bisect` evaluates the key
only on the `O(log n)` midpoints it probes.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(log n)`

`bisect_left` runs a binary search and therefore calls the key on `O(log n)`
versions, matching the hand-written approach.

##### Space Complexity: `O(1)`

`range` is a lazy sequence and `bisect` keeps only a constant amount of state.

#### Key Insights

- The `key` parameter on `bisect` functions (Python 3.10+) lets a binary search
  run over a predicate without building a parallel array.
- It expresses the same logic as the hand-written search in one line, but relies
  on the standard library to do the boundary work.
- `lo=1` keeps version `0` (which does not exist) out of the search space.

## Comparison of Solutions

### Time Complexity

- **Linear Scan**: `O(n)` - one API call per version up to the boundary.
- **Binary Search**: `O(log n)` - halves the range each step.
- **Bisect**: `O(log n)` - the same binary search inside the standard library.

### Space Complexity

- **Linear Scan**: `O(1)` - a single loop counter.
- **Binary Search**: `O(1)` - three integer pointers.
- **Bisect**: `O(1)` - a lazy `range` and constant `bisect` state.

### Trade-offs

- Linear Scan is trivial to reason about but makes the maximum number of API
  calls, exactly what the problem forbids at scale.
- Binary Search adds the small mental overhead of boundary handling in exchange
  for the optimal call count and no library dependency.
- Bisect is the most concise but hides the boundary logic behind a stdlib call
  and requires Python 3.10+ for the `key` argument.

### When to Use Each

- **Linear Scan**: Only to confirm correctness or when `n` is tiny; never for
  the real constraints.
- **Binary Search**: The right call for interviews and production; it is optimal
  and dependency-free (Recommended).
- **Bisect**: When you want the shortest idiomatic code and a modern Python
  runtime is guaranteed.

### Optimization Notes

- Compute `mid` as `lo + (hi - lo) // 2` rather than `(lo + hi) // 2` to avoid
  integer overflow in fixed-width integer languages.
- Updating `hi = mid` (inclusive) instead of `hi = mid - 1` is what makes the
  search find the first bad version instead of overshooting it.
- All logarithmic approaches make the same number of API calls; choose between
  them on readability and runtime version, not performance.

# [Time Based Key-Value Store](https://leetcode.com/problems/time-based-key-value-store/)

**Medium** | **35 minutes** | **Hash Table, String, Binary Search, Design**

**Pattern:** [Binary Search](../patterns/binary_search/intuition.md)

**Practice:** [`practice/time_based_key_value_store/solution.py`](https://github.com/ThoDHa/grind75/blob/main/practice/time_based_key_value_store/solution.py)

Design a time-based key-value data structure that can store multiple values for the same key at different time stamps and retrieve the key's value at a certain timestamp.

Implement the `TimeMap` class:

- `TimeMap()` Initializes the object of the data structure.
- `void set(String key, String value, int timestamp)` Stores the key `key` with the value `value` at the given time `timestamp`.
- `String get(String key, int timestamp)` Returns a value such that `set` was called previously, with `timestamp_prev <= timestamp`. If there are multiple such values, it returns the value associated with the largest `timestamp_prev`. If there are no values, it returns `""`.

## Examples

### Example 1

**Input:**

```
["TimeMap", "set", "get", "get", "set", "get", "get"]
[[], ["foo", "bar", 1], ["foo", 1], ["foo", 3], ["foo", "bar2", 4], ["foo", 4], ["foo", 5]]
```

**Output:**

```
[null, null, "bar", "bar", null, "bar2", "bar2"]
```

**Explanation:**

```
TimeMap timeMap = new TimeMap();
timeMap.set("foo", "bar", 1);  // store the key "foo" and value "bar" along with timestamp = 1.
timeMap.get("foo", 1);         // return "bar"
timeMap.get("foo", 3);         // return "bar", since there is no value corresponding to foo at timestamp 3 and timestamp 2, then the only value is at timestamp 1 is "bar".
timeMap.set("foo", "bar2", 4); // store the key "foo" and value "bar2" along with timestamp = 4.
timeMap.get("foo", 4);         // return "bar2"
timeMap.get("foo", 5);         // return "bar2"
```

## Constraints

- `1 <= key.length, value.length <= 100`
- `key` and `value` consist of lowercase English letters and digits.
- `1 <= timestamp <= 10^7`
- All the timestamps `timestamp` of `set` are strictly increasing.
- At most `2 * 10^5` calls will be made to `set` and `get`.

## Solutions

### Linear Scan

```python
class TimeMap:

    def __init__(self):
        # key -> list of (timestamp, value), appended in ascending time order.
        self.store: dict[str, list[tuple[int, str]]] = {}

    def set(self, key: str, value: str, timestamp: int) -> None:
        # Timestamps for set are strictly increasing, so append keeps order.
        # setdefault initializes an empty history the first time a key is seen.
        self.store.setdefault(key, []).append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        if key not in self.store:
            return ""
        history = self.store[key]
        # Walk backward and return the first entry not exceeding the query.
        for ts, value in reversed(history):
            if ts <= timestamp:
                return value
        return ""


# Your TimeMap object will be instantiated and used as follows:
# obj = TimeMap()
# obj.set(key, value, timestamp)
# param_2 = obj.get(key, timestamp)
```

#### Approach

Each key accumulates a history of `(timestamp, value)` entries. Because the
problem guarantees that `set` is called with strictly increasing timestamps, the
history for any key is already sorted by time, so the most recent valid value is
the last entry whose timestamp does not exceed the query.

1. Store, per key, a list of `(timestamp, value)` pairs in insertion order.
2. On `set`, append the pair; the increasing-timestamp guarantee keeps the list
   sorted without extra work.
3. On `get`, return `""` immediately if the key was never written.
4. Otherwise scan the history from newest to oldest and return the first value whose
   timestamp is `<=` the query. If no entry qualifies, return `""`.

This brute-force scan uses no library helpers: just a backward walk over the list.

#### Time and Space Complexity Analysis

##### Time Complexity

- **set**: `O(1)` amortized, a constant-time append.
- **get**: `O(n)` where `n` is the number of values stored for that key, since the
  backward scan may inspect every entry before finding (or failing to find) a match.

##### Space Complexity: `O(n)`

Across all keys, every `set` stores one `(timestamp, value)` pair, so total storage
is linear in the number of `set` calls.

#### Key Insights

- The strictly increasing timestamp guarantee means the history is sorted on
  insertion, so `set` stays `O(1)` and no re-sorting is ever required.
- Scanning backward returns the largest qualifying timestamp first, so the very
  first match is the answer.
- `setdefault(key, [])` initializes a key's history on first `set` without any
  imports, keeping this solution dependency-free.

### Manual Binary Search

```python
from collections import defaultdict


class TimeMap:

    def __init__(self):
        # key -> list of (timestamp, value), appended in ascending time order.
        self.store: dict[str, list[tuple[int, str]]] = defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        # Timestamps for set are strictly increasing, so append keeps order.
        self.store[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        if key not in self.store:
            return ""
        history = self.store[key]

        # Hand-written binary search for the rightmost timestamp <= query.
        # `lo` ends as the count of entries with timestamp <= query.
        lo, hi = 0, len(history)
        while lo < hi:
            mid = lo + (hi - lo) // 2
            if history[mid][0] <= timestamp:
                lo = mid + 1
            else:
                hi = mid

        if lo == 0:
            return ""
        return history[lo - 1][1]


# Your TimeMap object will be instantiated and used as follows:
# obj = TimeMap()
# obj.set(key, value, timestamp)
# param_2 = obj.get(key, timestamp)
```

#### Approach

The storage and `set` logic are identical to the Linear Scan: each key keeps a list of
`(timestamp, value)` pairs that stays sorted thanks to the increasing-timestamp
guarantee.

The improvement is in `get`. Instead of a linear backward walk, a hand-written
binary search finds the first index whose timestamp is strictly greater than the
query. That index equals the number of entries with timestamp `<=` the query, so the
entry just before it (`lo - 1`) holds the largest qualifying timestamp. If `lo` is
`0`, no entry qualifies and the answer is `""`.

#### Time and Space Complexity Analysis

##### Time Complexity

- **set**: `O(1)` amortized, a constant-time append.
- **get**: `O(log n)` where `n` is the number of values stored for that key,
  dominated by the binary search.

##### Space Complexity: `O(n)`

Across all keys, every `set` stores one `(timestamp, value)` pair, so total storage
is linear in the number of `set` calls.

#### Key Insights

- Searching for the first timestamp strictly greater than the query lands on the
  count of qualifying entries, so `lo - 1` is the rightmost valid index.
- Handling `lo == 0` covers the "query precedes every stored timestamp" case
  cleanly.
- Using `lo + (hi - lo) // 2` for the midpoint avoids integer overflow and keeps the
  bound-tracking search correct as the window narrows.

### Binary Search with bisect

```python
import bisect
from collections import defaultdict


class TimeMap:

    def __init__(self):
        # Per key, keep timestamps and values in two parallel lists. Both stay
        # sorted by time because set is called with strictly increasing stamps.
        self.times: dict[str, list[int]] = defaultdict(list)
        self.values: dict[str, list[str]] = defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        # Strictly increasing timestamps mean a plain append keeps times sorted.
        self.times[key].append(timestamp)
        self.values[key].append(value)

    def get(self, key: str, timestamp: int) -> str:
        if key not in self.times:
            return ""

        # bisect_right returns the count of timestamps <= query, so the entry
        # just before it (idx - 1) holds the largest qualifying timestamp.
        idx = bisect.bisect_right(self.times[key], timestamp)
        if idx == 0:
            return ""
        return self.values[key][idx - 1]


# Your TimeMap object will be instantiated and used as follows:
# obj = TimeMap()
# obj.set(key, value, timestamp)
# param_2 = obj.get(key, timestamp)
```

#### Approach

The storage and `set` logic mirror the previous approaches: each key keeps its history
sorted by time thanks to the increasing-timestamp guarantee. Here the timestamps live in
their own list so they can be passed straight to `bisect`, with the values kept in a
parallel list at matching indices.

The `get` logic is the same idea as the Manual Binary Search, with the search delegated
to `bisect.bisect_right`. Calling it on the sorted timestamp list returns the insertion
point just past every timestamp that is `<=` the query, which equals the number of
qualifying entries. The value just before that index (`idx - 1`) is therefore the one
with the largest timestamp not exceeding the query. When `idx` is `0`, no entry
qualifies and the answer is `""`.

#### Time and Space Complexity Analysis

##### Time Complexity

- **set**: `O(1)` amortized, two constant-time appends.
- **get**: `O(log n)` where `n` is the number of values stored for that key,
  dominated by the `bisect_right` call.

##### Space Complexity: `O(n)`

Across all keys, every `set` stores one timestamp and one value, so total storage is
linear in the number of `set` calls.

#### Key Insights

- `bisect_right` returns exactly the count of qualifying timestamps, so `idx - 1` is the
  rightmost valid index with no manual bound tracking.
- Splitting timestamps and values into parallel lists lets `bisect` operate on a plain
  list of integers without a key function or extra unpacking.
- This is the idiomatic Python form: the standard library performs the search that the
  Manual Binary Search approach spells out by hand.

## Comparison of Solutions

### Time Complexity

- **Linear Scan**: `set` is `O(1)`; `get` is `O(n)` per key, since it may inspect
  every stored version.
- **Manual Binary Search**: `set` is `O(1)`; `get` is `O(log n)` per key, since each
  step halves the candidate range.
- **Binary Search with bisect**: `set` is `O(1)`; `get` is `O(log n)` per key, with the
  halving handled by `bisect_right`.

### Space Complexity

- **Linear Scan**: `O(n)` total across all keys.
- **Manual Binary Search**: `O(n)` total across all keys, identical storage.
- **Binary Search with bisect**: `O(n)` total across all keys, split into parallel
  timestamp and value lists.

### Trade-offs

- The linear scan is trivial to write and verify: append on `set`, walk backward on
  `get`, with no index arithmetic.
- The manual binary search is slightly more involved but keeps `get` fast even when a
  single key accumulates a long version history.
- The bisect version is the same speed as the manual search while removing the loop and
  off-by-one bookkeeping entirely.

### When to Use Each

- **Linear Scan**: Fine when keys hold only a few versions or when `get` is called
  rarely relative to `set`.
- **Manual Binary Search**: Useful when the search must be understood or ported to a
  language without a standard binary-search helper.
- **Binary Search with bisect**: Preferred in Python for the full constraint range (up
  to `2 * 10^5` calls), since it is the shortest correct form and the standard choice.

### Optimization Notes

- All three solutions rely on the strictly increasing timestamp guarantee to keep the
  per-key history sorted on insertion, which is what makes `set` constant time.
- The only algorithmic difference is the `get` lookup; the storage shape is otherwise a
  free choice.
- A single list of `(timestamp, value)` tuples (used by the first two approaches) and
  parallel timestamp/value lists (used by the bisect approach) are equivalent in cost;
  the parallel layout exists only so `bisect` can search the timestamps directly.

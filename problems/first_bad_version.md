# [First Bad Version](https://leetcode.com/problems/first-bad-version/)

Easy - 15 minutes - Binary Search

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

`- 1 <= bad <= n <= 2³¹ - 1`

## Solution

```python
# The isBadVersion API is already defined for you.
# def isBadVersion(version: int) -> bool:

class Solution:
    def firstBadVersion(self, n: int) -> int:
        if n == 0:
            return 0
        start = 0
        stop = n
        while(start < stop):
            middle = start + (stop-start)//2
            if isBadVersion(middle):
                stop = middle
            else:
                start = middle+1
        return stop
```

### Approach

This solution uses binary search to efficiently find the first bad version. Binary search is ideal for this problem because:

1. We have a sorted range of versions `[1, 2, ..., n]`
2. All versions after a bad version are also bad (creating a clear boundary)
3. We need to minimize API calls, and binary search reduces the search space by half in each iteration

The algorithm works as follows:

- Initialize `start` to `0` and `stop` to `n`
- In each iteration, compute the middle point using `middle = start + (stop-start)//2` to avoid integer overflow
- If the middle version is bad (`isBadVersion(middle) == True`), move the `stop` pointer to `middle` since we need to look for potentially earlier bad versions
- If the middle version is good, move the `start` pointer to `middle + 1` since the first bad version must be after this point
- Continue until `start` and `stop` converge, at which point `stop` will indicate the first bad version

### Time and Space Complexity Analysis

#### Time Complexity: `O(log n)`

The binary search algorithm reduces the search space by half in each iteration. With `n` versions, the maximum number of iterations is `log n`, resulting in logarithmic time complexity. This is optimal for this problem as it minimizes the number of API calls to `isBadVersion`.

#### Space Complexity: `O(1)`

The solution uses only a constant amount of extra space regardless of the input size, as it only needs to store a few variables (`start`, `stop`, and `middle`).

### Key Insights

- Binary search is the optimal approach for this problem because it minimizes API calls
- The formula `middle = start + (stop-start)//2` prevents integer overflow that could occur with the simpler `(start + stop) // 2`
- The solution correctly handles edge cases (like when the first version is bad)
- This is a classic example of finding a boundary in a sorted array with a boolean condition
- The algorithm converges to the first bad version because of how we update the pointers: when we find a bad version, we continue searching left (by setting `stop = middle`) but never exclude that version from consideration

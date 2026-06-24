"""Insert Interval — https://leetcode.com/problems/insert-interval/

Write-up & approaches: ../../docs/problems/insert_interval.md

Given a sorted list of non-overlapping intervals and a new interval, insert the
new interval and merge any overlaps so the result stays sorted and disjoint.

  uv run python insert_interval/solution.py   # debug one case (see CASE below)
  uv run pytest insert_interval/              # run the test sets
"""

from typing import List

from harness import NotSolved, pick_case


class Solution:
    def insert(
        self, intervals: List[List[int]], newInterval: List[int]
    ) -> List[List[int]]:
        """State the time and space complexity of your approach, and explain why.

        Time:  O(?):
        Space: O(?):
        """
        merge: List[List[int]] = []
        i = 0
        n = len(intervals)
        while i < n and intervals[i][1] < newInterval[0]:
            merge.append(intervals[i])
            i += 1
        while i < n and intervals[i][0] <= newInterval[1]:
            newInterval[0] = min(newInterval[0], intervals[i][0])
            newInterval[1] = max(newInterval[1], intervals[i][1])
            i += 1
        merge.append(newInterval)
        while i < n:
            merge.append(intervals[i])
            i += 1
        return merge


if __name__ == "__main__":
    # Debug playground: set a breakpoint in insert above, then run this file.
    # Pick a case by id (ids are in cases.json / cases_full.json).
    CASE = "example_1"
    case = pick_case(__file__, CASE)
    result = Solution().insert(*case["args"])
    print(f"case {case['id']}: args = {case['args']}")
    print(f"expected: {case['expected']}")
    print(f"got:      {result}")

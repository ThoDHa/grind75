# [Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/)

**Medium** | **30 minutes** | **Array, Dynamic Programming**

**Pattern:** [DP Knapsack/Subset](../patterns/dp_knapsack_subset/intuition.md)

**Practice:** [`practice/partition_equal_subset_sum/solution.py`](https://github.com/ThoDHa/grind75/blob/main/practice/partition_equal_subset_sum/solution.py)

Given an integer array `nums`, return `true` if you can partition the array into two subsets such that the sum of the elements in both subsets is equal.

## Examples

### Example 1

**Input:** `nums = [1,5,11,5]`

**Output:** `true`

**Explanation:** The array can be partitioned as `[1, 5, 5]` and `[11]`.

### Example 2

**Input:** `nums = [1,2,3,5]`

**Output:** `false`

**Explanation:** The array cannot be partitioned into equal sum subsets.

## Constraints

- `1 <= nums.length <= 200`
- `1 <= nums[i] <= 100`

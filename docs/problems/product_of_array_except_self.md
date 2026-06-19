# [Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/)

**Medium** | **30 minutes** | **Array, Prefix Sum**

**Pattern:** [Prefix Sum](../patterns/prefix_sum/intuition.md)

**Practice:** [`practice/product_of_array_except_self/solution.py`](../../practice/product_of_array_except_self/solution.py)

Given an integer array `nums`, return an array `answer` such that `answer[i]` is
equal to the product of all the elements of `nums` except `nums[i]`.

The product of any prefix or suffix of `nums` is guaranteed to fit in a 32-bit
integer.

You must write an algorithm that runs in `O(n)` time and without using the
division operation.

## Examples

### Example 1

**Input:** `nums = [1,2,3,4]`

**Output:** `[24,12,8,6]`

**Explanation:** `answer[0] = 2*3*4 = 24`, `answer[1] = 1*3*4 = 12`,
`answer[2] = 1*2*4 = 8`, and `answer[3] = 1*2*3 = 6`.

### Example 2

**Input:** `nums = [-1,1,0,-3,3]`

**Output:** `[0,0,9,0,0]`

**Explanation:** Every position except index `2` includes the zero in its
product, so it becomes `0`. Index `2` is the product of the remaining elements,
`(-1)*1*(-3)*3 = 9`.

## Constraints

- `2 <= nums.length <= 10^5`
- `-30 <= nums[i] <= 30`
- The product of any prefix or suffix of `nums` is guaranteed to fit in a 32-bit integer.

## Follow-up

Can you solve the problem in `O(1)` extra space complexity? (The output array does not count as extra space for space complexity analysis.)

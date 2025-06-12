# [Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/)

Easy - 20 minutes - Array

You are given an array `prices` where `prices[i]` is the price of a given stock on the
`i`th day.

You want to maximize your profit by choosing a single day to buy one stock and
choosing a different day in the future to sell that stock.

Return the maximum profit you can achieve from this transaction. If you cannot
achieve any profit, return `0`.

## Examples

### Example 1

**Input:** `prices = [7,1,5,3,6,4]`

**Output:** `5`

**Explanation:** Buy on day 2 (price = `1`) and sell on day 5 (price = `6`), profit = `6-1 = 5`.
Note that buying on day 2 and selling on day 1 is not allowed because you must buy before you sell.

### Example 2

**Input:** `prices = [7,6,4,3,1]`

**Output:** `0`

**Explanation:** In this case, no transactions are done and the max profit = `0`.

## Constraints

- `1 <= prices.length <= 10^5`
- `0 <= prices[i] <= 10^4`

## Solution

```python
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        maxProfit = 0
        lowest = 100000
        for price in prices:
            profit = price - lowest
            maxProfit = max(profit, maxProfit)
            lowest = min(price, lowest)
        return maxProfit

```

### Approach

This solution uses a one-pass algorithm to find the maximum profit. As we iterate through the array of prices:

1. We track the lowest stock price we've seen so far (`lowest`)
2. For each price, we calculate the potential profit if we sold at that price
3. We update our maximum profit if the current potential profit is higher
4. We update our lowest price if we find a new lowest

This approach works because to maximize profit, we need to buy at the lowest price and sell at the highest price that comes after it. By tracking the lowest price seen so far and calculating the profit at each step, we effectively consider all possible buying opportunities up to the current day.

### Time and Space Complexity Analysis

#### Time Complexity: `O(n)`

We only need a single pass through the array of prices. Each price is processed in constant time with simple comparison and arithmetic operations.

#### Space Complexity: `O(1)`

The solution uses only two variables (`maxProfit` and `lowest`) regardless of the input size, resulting in constant space complexity.

### Key Insights

- The key insight is that we don't need to try all possible buy/sell combinations (which would be O(n²))
- Instead, we can track the minimum price seen so far and calculate the maximum profit in a single pass
- This approach elegantly handles cases where no profit is possible by initializing `maxProfit` to `0`
- The algorithm naturally enforces the constraint that we must buy before selling by maintaining the lowest price seen up to the current point

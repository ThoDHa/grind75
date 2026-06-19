# [Coin Change](https://leetcode.com/problems/coin-change/)

**Medium** | **25 minutes** | **Dynamic Programming**

**Pattern:** [DP Knapsack/Subset](../patterns/dp_knapsack_subset/intuition.md)

**Practice:** [`practice/coin_change/solution.py`](../../practice/coin_change/solution.py)

You are given an integer array `coins` representing coins of different denominations and an integer `amount` representing a total amount of money.

Return the fewest number of coins that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return `-1`.

You may assume that you have an infinite number of each kind of coin.

## Examples

### Example 1

**Input:** `coins = [1,3,4]`, `amount = 6`

**Output:** `2`

**Explanation:** The answer is `2` because `6 = 3 + 3`.

### Example 2

**Input:** `coins = [2]`, `amount = 3`

**Output:** `-1`

### Example 3

**Input:** `coins = [1]`, `amount = 0`

**Output:** `0`

## Constraints

- `1 <= coins.length <= 12`
- `1 <= coins[i] <= 2^31 - 1`
- `0 <= amount <= 10^4`

## Solutions

### Brute Force Recursion

```python
class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        def backtrack(remaining_amount):
            # Base cases
            if remaining_amount == 0:
                return 0
            if remaining_amount < 0:
                return -1

            min_coins = float('inf')

            # Try each coin denomination
            for coin in coins:
                # Recursively solve for remaining amount
                result = backtrack(remaining_amount - coin)

                # If it's possible to make the remaining amount
                if result != -1:
                    min_coins = min(min_coins, 1 + result)

            return -1 if min_coins == float('inf') else min_coins

        return backtrack(amount)
```

#### Approach

This is a naive recursive approach without memoization. It explores all possible combinations of coins by trying each coin at each step and recursively solving the remaining amount.

While conceptually simple, this approach has exponential time complexity due to overlapping subproblems being solved multiple times.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(coins.length^amount)`

In the worst case, we make `coins.length` recursive calls for each level, and the depth can go up to `amount`.

##### Space Complexity: `O(amount)`

Space for the recursion stack, which can be up to `amount` levels deep.

#### Key Insights

- The recurrence is simple: the minimum coins for amount `x` is `1 + min(backtrack(x - coin))` over all coins `c` that keep `x - coin` non-negative.
- It exposes the optimal substructure of the problem, which every faster approach exploits.
- Without caching, the same remaining amounts are recomputed exponentially many times, so this is only viable for tiny inputs.

### BFS

```python
from collections import deque

class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        if amount == 0:
            return 0

        # BFS to find minimum steps (coins) to reach target amount
        queue = deque([0])  # Start with amount 0
        visited = {0}       # Track visited amounts to avoid cycles
        steps = 0           # Number of coins used so far

        while queue:
            steps += 1
            # Process all amounts reachable with current number of coins
            for _ in range(len(queue)):
                current_amount = queue.popleft()

                # Try adding each coin denomination
                for coin in coins:
                    new_amount = current_amount + coin

                    # If we reached the target amount
                    if new_amount == amount:
                        return steps

                    # If this amount is valid and not visited yet
                    if new_amount < amount and new_amount not in visited:
                        visited.add(new_amount)
                        queue.append(new_amount)

        return -1  # Target amount is unreachable
```

#### Approach

This BFS approach treats the problem as finding the shortest path from amount 0 to the target amount, where each coin represents an edge with weight 1. We use level-by-level BFS where each level represents using one more coin.

The key insight is that BFS naturally finds the minimum number of steps (coins) to reach any amount, since it explores all possibilities with fewer coins before exploring those with more coins.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(amount × coins.length)`

In the worst case, we visit each amount from 0 to `amount - 1`, and for each amount we try all coins.

##### Space Complexity: `O(amount)`

Space for the queue and visited set, both of which can contain up to `amount` elements.

#### Key Insights

- Modeling each reachable amount as a graph node turns "fewest coins" into "shortest path," which BFS solves directly.
- Because every edge has unit weight, the first level at which we hit the target amount is guaranteed to be optimal.
- The `visited` set is essential: without it, the same amounts would be enqueued repeatedly and the search would degrade badly.

### Top-Down Memoization

```python
class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        # Memoization cache to store computed results
        memo = {}

        def dp(remaining_amount):
            # Base cases
            if remaining_amount == 0:
                return 0
            if remaining_amount < 0:
                return -1

            # Check if result is already computed
            if remaining_amount in memo:
                return memo[remaining_amount]

            min_coins = float('inf')

            # Try each coin denomination
            for coin in coins:
                # Recursively solve for remaining amount after using this coin
                result = dp(remaining_amount - coin)

                # If it's possible to make the remaining amount
                if result != -1:
                    min_coins = min(min_coins, 1 + result)

            # Store result in memo: -1 if impossible, otherwise minimum coins
            memo[remaining_amount] = -1 if min_coins == float('inf') else min_coins
            return memo[remaining_amount]

        return dp(amount)
```

#### Approach

This top-down approach uses recursion with memoization. We start from the target amount and recursively try using each coin, asking "what's the minimum coins needed for the remaining amount?"

The recursive relation is the same: for amount `x`, try each coin `c` and take the minimum of `1 + dp(x - c)` for all valid coins. Memoization prevents recomputing the same subproblems multiple times.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(amount × coins.length)`

Each unique amount from 0 to `amount` is computed exactly once, and for each amount we try all coins.

##### Space Complexity: `O(amount)`

Space for the memoization table plus recursion stack depth (worst case O(amount)).

#### Key Insights

- Memoization keeps the natural recursive framing of the brute force while collapsing the exponential blow-up to one computation per distinct remaining amount.
- It only evaluates the subproblems actually reachable from the target, so it can skip amounts that bottom-up would still compute.
- Deep recursion can approach `amount` stack frames, so for very large amounts an iterative formulation avoids recursion-limit risk.

### Bottom-Up DP

```python
class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        # dp[i] represents the minimum coins needed to make amount i
        # Initialize with amount + 1 (impossible value) for all amounts
        dp = [amount + 1] * (amount + 1)
        dp[0] = 0  # Base case: 0 coins needed to make amount 0

        # For each amount from 1 to target amount
        for current_amount in range(1, amount + 1):
            # Try each coin denomination
            for coin in coins:
                # If this coin can be used (coin <= current_amount)
                if coin <= current_amount:
                    # Update minimum coins needed for current_amount
                    # Either keep existing value or use (1 + coins for remaining amount)
                    dp[current_amount] = min(dp[current_amount],
                                           1 + dp[current_amount - coin])

        # Return result: -1 if impossible, otherwise minimum coins needed
        return dp[amount] if dp[amount] != amount + 1 else -1
```

#### Approach

This bottom-up dynamic programming solution builds the answer for all amounts from 0 to the target amount. For each amount, we try using each coin denomination and choose the combination that requires the fewest total coins.

The key insight is that to make amount `i`, we can use any coin `c` (where `c <= i`) and then optimally make the remaining amount `i - c`. This gives us the recurrence relation: `dp[i] = min(dp[i], 1 + dp[i - c])` for all valid coins `c`.

We initialize all values to `amount + 1` (an impossible value) so we can easily detect unreachable amounts. The base case `dp[0] = 0` means zero coins are needed to make amount 0.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(amount × coins.length)`

We iterate through each amount from 1 to `amount` (O(amount)) and for each amount, we check all coin denominations (O(coins.length)).

##### Space Complexity: `O(amount)`

We use a DP array of size `amount + 1` to store the minimum coins needed for each amount.

#### Key Insights

- This is the classic unbounded-knapsack minimization pattern: unlimited copies of each item (coin), optimizing the count for a target capacity (amount).
- Initializing every entry to the sentinel `amount + 1` exceeds any valid answer yet avoids overflow, so an unreachable amount is detected cleanly by checking against the sentinel at the end.
- Being iterative, it carries no recursion overhead and no stack-depth risk, which makes it the most robust choice for large amounts.

## Comparison of Solutions

### Time Complexity

- **Brute Force Recursion**: `O(coins.length^amount)` - exponential, making `coins.length` recursive calls per level to a depth of `amount`.
- **BFS**: `O(amount × coins.length)` - visits each amount once and tries all coins from it, like a shortest-path search.
- **Top-Down Memoization**: `O(amount × coins.length)` - each unique amount is computed once via memoization, trying all coins per amount.
- **Bottom-Up DP**: `O(amount × coins.length)` - iterates every amount from 1 to target and checks all coin denominations for each.

### Space Complexity

- **Brute Force Recursion**: `O(amount)` - recursion stack up to `amount` levels deep.
- **BFS**: `O(amount)` - queue and visited set, each holding up to `amount` elements.
- **Top-Down Memoization**: `O(amount)` - memoization table plus recursion stack depth up to `amount`.
- **Bottom-Up DP**: `O(amount)` - a single DP array of size `amount + 1`.

### Trade-offs

- **Brute Force Recursion**: Simplest to understand, but exponential time makes it impractical for large inputs.
- **BFS**: Models the problem cleanly as a shortest-path search, but adds queue and visited-set overhead.
- **Top-Down Memoization**: Intuitive recursion that only computes the subproblems actually required, at the cost of recursion overhead and stack space.
- **Bottom-Up DP**: Iterative with clear logic and optimal complexity, but builds every subproblem even when some are not needed.

### When to Use Each

- **Brute Force Recursion**: Only for understanding the problem or very small inputs. Demonstrates the need for optimization.
- **BFS**: When you want to model the problem as a graph shortest path problem. Good for educational purposes.
- **Top-Down Memoization**: When recursive thinking feels more natural or when you only need to compute specific subproblems.
- **Bottom-Up DP (Recommended)**: Best for interviews and production code. Clear, efficient, and iterative.

### Optimization Notes

- The Bottom-Up DP solution is the recommended choice for interviews and production: it is iterative, optimal at `O(amount × coins.length)`, and free of recursion overhead.
- Initialize the DP array with `amount + 1` as a sentinel "impossible" value; it exceeds any valid answer yet avoids overflow, letting you detect unreachable amounts cleanly at the end.
- Both DP approaches share the same complexity, so prefer bottom-up unless recursive framing is clearer; reserve BFS for when a shortest-path mental model helps and avoid plain brute-force recursion for anything but tiny inputs.

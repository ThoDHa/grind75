# [Climbing Stairs](https://leetcode.com/problems/climbing-stairs/)

Easy - 15 minutes - Dynamic Programming

You are climbing a staircase. It takes `n` steps to reach the top.

Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

## Examples

### Example 1

**Input:** `n = 2`

**Output:** `2`

**Explanation:** There are two ways to climb to the top.

1. 1 step + 1 step
2. 2 steps

### Example 2

**Input:** `n = 3`

**Output:** `3`

**Explanation:** There are three ways to climb to the top.

1. 1 step + 1 step + 1 step
2. 1 step + 2 steps
3. 2 steps + 1 step

## Constraints

- `1 <= n <= 45`

## Solutions

### Solution 1: Dynamic Programming with Tabulation

```python
class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 1:
            return 1
        
        # Create array to store number of ways to reach each step
        dp = [0] * (n + 1)
        dp[0] = dp[1] = 1
        
        # Fill dp array using recurrence relation
        for i in range(2, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]
            
        return dp[n]
```

#### Approach

This solution uses bottom-up dynamic programming with tabulation to solve the climbing stairs problem:

1. We create a DP array where `dp[i]` represents the number of ways to climb to the ith step
2. Base cases: `dp[0] = dp[1] = 1` (there's only one way to reach steps 0 and 1)
3. For steps 2 through n, we apply the recurrence relation: `dp[i] = dp[i-1] + dp[i-2]`
4. This relation captures that to reach step i, we can either:
   - Take a single step from step i-1
   - Take a double step from step i-2

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

- We iterate through the array once from 2 to n
- Each iteration involves constant time operations

##### Space Complexity: `O(n)`

- We use an array of size n+1 to store the intermediate results

#### Key Insights

- This problem follows the Fibonacci sequence pattern
- The dynamic programming approach breaks down the problem into simpler subproblems
- By storing results of subproblems, we avoid redundant calculations

### Solution 2: Space-Optimized Dynamic Programming

```python
class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 1:
            return 1
        
        # Initialize first two numbers in the sequence
        prev, curr = 1, 1
        
        # Calculate subsequent numbers using only two variables
        for i in range(2, n + 1):
            temp = curr
            curr = prev + curr
            prev = temp
            
        return curr
```

#### Approach

This solution optimizes the space usage of the dynamic programming approach:

1. We observe that at any step, we only need the previous two values in the sequence
2. Instead of using an array to store all intermediate results, we use two variables
3. We iteratively update these variables as we move up the staircase
4. This maintains the same logic as Solution 1 but uses O(1) space

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

- We still need to iterate through each step from 2 to n once

##### Space Complexity: `O(1)`

- We use only a constant amount of extra space regardless of input size

#### Key Insights

- When a DP solution only depends on a fixed number of previous states, we can optimize space usage
- This approach is particularly useful for large inputs where memory might be a concern
- The solution maintains the elegance of the DP approach while being more efficient

### Solution 3: Math Formula (Closed-form Solution)

```python
class Solution:
    def climbStairs(self, n: int) -> int:
        import math
        
        # Fibonacci closed form formula (Binet's formula)
        sqrt5 = math.sqrt(5)
        fibn = ((1 + sqrt5) / 2) ** (n + 1) - ((1 - sqrt5) / 2) ** (n + 1)
        return int(fibn / sqrt5)
```

#### Approach

This solution uses the closed-form expression for the Fibonacci sequence (Binet's formula):

1. Since the climbing stairs problem follows the Fibonacci sequence where F(n) = ways to climb n stairs
2. We can use the mathematical closed-form solution: F(n) = (φⁿ - (1-φ)ⁿ)/√5
3. Where φ is the golden ratio (1 + √5)/2

#### Time and Space Complexity Analysis

##### Time Complexity: `O(1)`

- The calculation is done in constant time regardless of n
- However, for very large n, there might be precision issues

##### Space Complexity: `O(1)`

- Only a constant amount of variables are used

#### Key Insights

- Recognizing the problem follows the Fibonacci sequence unlocks a mathematical solution
- This approach is theoretically the most efficient but may face floating-point precision issues
- It's more of a mathematical curiosity than a practical solution for very large n

## Comparison of Solutions

### Time Complexity

- **Solution 1 (DP with Tabulation)**: `O(n)` - Linear time to build the DP table
- **Solution 2 (Space-Optimized DP)**: `O(n)` - Same linear time requirement
- **Solution 3 (Math Formula)**: `O(1)` - Constant time calculation

### Space Complexity

- **Solution 1 (DP with Tabulation)**: `O(n)` - Requires an array of size n+1
- **Solution 2 (Space-Optimized DP)**: `O(1)` - Uses only a constant amount of extra space
- **Solution 3 (Math Formula)**: `O(1)` - Uses only a constant amount of extra space

### Trade-offs

- **Solution 1** is intuitive and good for educational purposes, but uses more space
- **Solution 2** provides the best balance of simplicity and efficiency for most cases
- **Solution 3** is theoretically most efficient but can have numerical precision issues

### When to Use Each

- **Solution 1**: When teaching DP concepts or when space is not a concern
- **Solution 2**: In most practical scenarios - efficient and easy to understand
- **Solution 3**: When absolute performance is critical and n is within the range of floating-point precision

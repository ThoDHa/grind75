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

## Solutions

### Brute Force

```python
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        result = []

        # For each position, multiply every other element
        for i in range(n):
            product = 1
            for j in range(n):
                if j != i:
                    product *= nums[j]
            result.append(product)

        return result
```

#### Approach

The brute force approach directly implements the problem definition:

1. For each index `i`, start a running product of `1`.
2. Walk the whole array, multiplying in every element except `nums[i]`.
3. Append that product to the result.

It is correct and easy to read, but it recomputes overlapping products for every position, which makes it too slow for large arrays.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n^2)`

For each of the `n` elements, we iterate through all `n` elements to compute the product.

##### Space Complexity: `O(1)`

Only a single running-product variable is used, not counting the output array.

#### Key Insights

- It mirrors the problem statement literally, which makes it the natural first attempt.
- The repeated inner pass wastes work: the product of "everything before `i`" and "everything after `i`" is recomputed from scratch each time.

### Prefix and Suffix Arrays

```python
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)

        # prefix[i] = product of all elements before index i
        prefix = [1] * n
        for i in range(1, n):
            prefix[i] = prefix[i - 1] * nums[i - 1]

        # suffix[i] = product of all elements after index i
        suffix = [1] * n
        for i in range(n - 2, -1, -1):
            suffix[i] = suffix[i + 1] * nums[i + 1]

        # result[i] = prefix[i] * suffix[i]
        result = []
        for i in range(n):
            result.append(prefix[i] * suffix[i])

        return result
```

#### Approach

The product of all elements except `nums[i]` equals the product of everything to its left times the product of everything to its right. Build those two pieces explicitly:

1. **Prefix array**: `prefix[i]` holds the product of all elements before index `i`. Seed `prefix[0] = 1` and roll forward.
2. **Suffix array**: `suffix[i]` holds the product of all elements after index `i`. Seed `suffix[n-1] = 1` and roll backward.
3. **Combine**: `result[i] = prefix[i] * suffix[i]`.

Seeding the boundaries with `1` (the multiplicative identity) makes the first and last positions fall out correctly without special cases.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Three separate linear passes: build the prefix array, build the suffix array, and combine them.

##### Space Complexity: `O(n)`

Two auxiliary arrays of size `n` hold the prefix and suffix products, in addition to the output array.

#### Key Insights

- The decomposition `answer[i] = (product of the left) * (product of the right)` is the heart of the problem and avoids division entirely.
- Initializing both arrays to `1` handles the empty-prefix and empty-suffix edge positions cleanly.

### Constant-Space Prefix and Suffix

```python
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        result = [1] * n

        # Pass 1: store prefix products directly in the result array
        # result[i] becomes the product of all elements before index i
        for i in range(1, n):
            result[i] = result[i - 1] * nums[i - 1]

        # Pass 2: fold in suffix products using a single running variable
        suffix_product = 1
        for i in range(n - 1, -1, -1):
            result[i] *= suffix_product
            suffix_product *= nums[i]

        return result
```

#### Approach

This is the prefix/suffix idea with the auxiliary arrays removed:

1. **Pass 1**: Store the prefix products directly in the output array, so `result[i]` becomes the product of everything before `i`.
2. **Pass 2**: Sweep right to left with one running `suffix_product` variable, multiplying each `result[i]` by the product of everything after `i`, then folding `nums[i]` into the running suffix.

The output array doubles as the prefix store, and the suffix only ever needs a single scalar, so no extra arrays are required.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Two linear passes through the array.

##### Space Complexity: `O(1)`

Only the scalar `suffix_product` is extra; the output array does not count toward space complexity.

#### Key Insights

- Reusing the output array to hold prefix products is the key trick that collapses `O(n)` auxiliary space to `O(1)`.
- A suffix only needs to be remembered as a single accumulating scalar, never as a full array.
- This meets every stated constraint: `O(n)` time, no division, and `O(1)` extra space.

### Division Method

```python
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)

        # Total product of all non-zero elements, plus zero bookkeeping
        total_product = 1
        zero_count = 0
        zero_index = -1

        for i, num in enumerate(nums):
            if num == 0:
                zero_count += 1
                zero_index = i
                if zero_count > 1:
                    # Two or more zeros: every product is 0
                    return [0] * n
            else:
                total_product *= num

        result = []
        if zero_count == 1:
            # Only the zero position gets the product of the others
            for i in range(n):
                result.append(total_product if i == zero_index else 0)
        else:
            # No zeros: divide the total product by each element
            for num in nums:
                result.append(total_product // num)

        return result
```

#### Approach

If division were allowed, the answer at each position is simply the total product divided by the current element. The complication is zeros, which make division undefined, so they are handled separately:

1. Compute the product of all non-zero elements while counting zeros.
2. **Two or more zeros**: every position's product includes a zero, so return all zeros.
3. **Exactly one zero**: only the zero position is non-zero (the product of the others); every other position is `0`.
4. **No zeros**: divide the total product by each element.

This approach violates the problem's explicit "no division" rule, so it is included for contrast rather than as a submission.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

One pass to accumulate the product and count zeros, then one pass to build the result.

##### Space Complexity: `O(1)`

Only a few scalars for the product, the zero count, and the zero index.

#### Key Insights

- Division reduces the problem to one total product, but the zero edge cases are fragile and easy to get wrong.
- The problem forbids division precisely to push toward the prefix/suffix technique, which generalizes to non-invertible operations.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(n^2)` - for each of the `n` elements, iterate through all `n` elements to compute the product.
- **Prefix and Suffix Arrays**: `O(n)` - three linear passes to build prefix, build suffix, and combine.
- **Constant-Space Prefix and Suffix**: `O(n)` - two linear passes through the array.
- **Division Method**: `O(n)` - one pass for the total product and zero count, one pass to build the result.

### Space Complexity

- **Brute Force**: `O(1)` - a single running-product variable, not counting the output array.
- **Prefix and Suffix Arrays**: `O(n)` - two extra arrays of size `n` for the prefix and suffix products.
- **Constant-Space Prefix and Suffix**: `O(1)` - only a single `suffix_product` scalar; the output array does not count.
- **Division Method**: `O(1)` - a few scalars for the product, zero count, and zero index.

### Trade-offs

- **Brute Force**: simplest to write, but quadratic time makes it impractical for large inputs.
- **Prefix and Suffix Arrays**: clear and easy to reason about, at the cost of `O(n)` auxiliary space.
- **Constant-Space Prefix and Suffix**: optimal space while staying linear, at the cost of being slightly less obvious.
- **Division Method**: intuitive when division is allowed, but it breaks the problem constraint and needs careful zero handling.

### When to Use Each

- **Brute Force**: only for understanding the problem or for very small arrays.
- **Prefix and Suffix Arrays**: a good stepping stone for learning the technique before optimizing space.
- **Constant-Space Prefix and Suffix** (recommended): best for interviews; it satisfies every constraint with optimal complexity.
- **Division Method**: only if the no-division constraint is explicitly lifted and zeros are handled carefully.

### Optimization Notes

- The recommended answer is Constant-Space Prefix and Suffix: it meets the `O(n)` time and no-division constraints while reaching `O(1)` extra space by reusing the output array.
- The core technique is storing prefix products in the output array on the first pass, then folding in a single running suffix product on the reverse pass.
- Seed prefix and suffix values to `1` (the multiplicative identity) so boundary positions multiply out correctly; a common pitfall is initializing with the wrong identity.
- The Division Method is disqualified by the explicit no-division rule and introduces fragile zero-handling logic; avoid it unless the constraint is lifted.

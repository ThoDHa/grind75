# [Add Binary](https://leetcode.com/problems/add-binary/)

Easy - 15 minutes - Math, String, Bit Manipulation

Given two binary strings `a` and `b`, return their sum as a binary string.

## Examples

### Example 1

**Input:** `a = "11", b = "1"`

**Output:** `"100"`

### Example 2

**Input:** `a = "1010", b = "1011"`

**Output:** `"10101"`

## Constraints

- `1 <= a.length, b.length <= 10^4`
- `a` and `b` consist only of `'0'` or `'1'` characters.
- Each string does not contain leading zeros except for the zero itself.

## Solutions

### Solution 1: Three-Phase Iterative Approach

```python
def addBinary(self, a: str, b: str) -> str:
    return_value: str = ""
    carry_over = 0
    while len(a) and len(b):
        x = a[-1]
        y = b[-1]
        a = a[:-1]
        b = b[:-1]
        temp = int(x) + int(y) + int(carry_over)
        if temp == 3:
            return_value = "1" + return_value
            carry_over = 1
        elif temp == 2:
            return_value = "0" + return_value
            carry_over = 1
        elif temp == 1:
            return_value = "1" + return_value
            carry_over = 0
        else:
            return_value = "0" + return_value
            carry_over = 0
    while len(a):
        x = a[-1]
        a = a[:-1]
        temp = int(x) + carry_over
        if temp == 3:
            return_value = "1" + return_value
            carry_over = 1
        elif temp == 2:
            return_value = "0" + return_value
            carry_over = 1
        elif temp == 1:
            return_value = "1" + return_value
            carry_over = 0
        else:
            return_value = "0" + return_value
            carry_over = 0
    while len(b):
        x = b[-1]
        b = b[:-1]
        temp = int(x) + carry_over
        if temp == 3:
            return_value = "1" + return_value
            carry_over = 1
        elif temp == 2:
            return_value = "0" + return_value
            carry_over = 1
        elif temp == 1:
            return_value = "1" + return_value
            carry_over = 0
        else:
            return_value = "0" + return_value
            carry_over = 0
    if carry_over == 1:
        return_value = "1" + return_value
    return return_value
```

#### Solution 1: Approach

This solution processes the binary addition in three phases: first, it handles bits from both strings simultaneously, then it processes any remaining bits from string `a`, and finally any remaining bits from string `b`. In each phase, it explicitly handles each possible sum case (0, 1, 2, or 3) to determine the current bit and carry.

#### Solution 1: Time and Space Complexity Analysis

##### Time Complexity: `O(max(n, m))`

We process each bit position once across the three loops.

##### Space Complexity: `O(max(n, m))`

The space needed for the result string, which is at most max(n, m) + 1 bits.

#### Solution 1: Key Insights

- Uses explicit logic for different possible bit combinations
- Processes strings from right to left by removing the last character in each iteration
- Handles the carry at the end after all digits are processed

### Solution 2: Bit-by-bit Computation

```python
def addBinary(self, a: str, b: str) -> str:
    result = ""
    carry = 0
    
    # Make sure a and b have the same length by padding with zeros
    a = a.zfill(max(len(a), len(b)))
    b = b.zfill(max(len(a), len(b)))
    
    # Iterate from right to left
    for i in range(len(a) - 1, -1, -1):
        bit_sum = int(a[i]) + int(b[i]) + carry
        result = str(bit_sum % 2) + result
        carry = bit_sum // 2
    
    # Add the final carry if needed
    if carry:
        result = '1' + result
        
    return result
```

#### Solution 2: Approach

This solution simulates the binary addition process we do by hand, going from right to left. For each position, we add the corresponding bits from both numbers and the carry from the previous step. The result bit is the sum modulo 2, and the new carry is the integer division of the sum by 2.

#### Solution 2: Time and Space Complexity Analysis

##### Time Complexity: `O(max(n, m))`

We process each bit position once, where n and m are the lengths of the input strings.

##### Space Complexity: `O(max(n, m))`

We create a new string to store the result, which has at most max(n, m) + 1 bits.

#### Solution 2: Key Insights

- Simulates the binary addition process bit-by-bit
- Uses modulo operation to determine the current bit value
- Uses integer division to determine the carry bit

### Solution 3: Using Built-in Functions

```python
def addBinary(self, a: str, b: str) -> str:
    # Convert binary strings to integers, add them, then convert back to binary
    sum_int = int(a, 2) + int(b, 2)
    # Remove '0b' prefix from binary representation
    return bin(sum_int)[2:]
```

#### Solution 3: Approach

This solution leverages Python's built-in functions to convert binary strings to integers, perform the addition, and then convert the result back to a binary string.

#### Solution 3: Time and Space Complexity Analysis

##### Time Complexity: `O(n + m)`

Converting the strings to integers and back to binary takes linear time.

##### Space Complexity: `O(1)` for computation, `O(max(n, m))` for output

The space needed for computation is constant, but the output size is proportional to the input sizes.

#### Solution 3: Key Insights

- Takes advantage of Python's built-in conversion functions
- Very concise solution
- May not work for extremely large binary numbers due to potential integer overflow in some languages (but works in Python due to arbitrary precision integers)

### Solution 4: Single-Loop Iterative Approach

```python
def addBinary(self, a: str, b: str) -> str:
    result = ""
    carry = 0
    i, j = len(a) - 1, len(b) - 1
    
    # Process both strings until we reach the end of both
    while i >= 0 or j >= 0 or carry:
        # Get current bits (0 if we've reached the end of the string)
        bit_a = int(a[i]) if i >= 0 else 0
        bit_b = int(b[j]) if j >= 0 else 0
        
        # Compute sum and carry
        current_sum = bit_a + bit_b + carry
        result = str(current_sum % 2) + result
        carry = current_sum // 2
        
        # Move to the next bits
        i -= 1
        j -= 1
    
    return result
```

#### Solution 4: Approach

This iterative solution explicitly tracks indices for both strings and processes them in a single loop. It handles strings of different lengths and carries without padding or multiple loops.

#### Solution 4: Time and Space Complexity Analysis

##### Time Complexity: `O(max(n, m))`

We process each bit position once in a single pass.

##### Space Complexity: `O(max(n, m))`

The space needed for the result string, which is at most max(n, m) + 1 bits.

#### Solution 4: Key Insights

- Handles both strings in a single loop
- Works efficiently for strings of different lengths
- Avoids unnecessary string padding or multiple loops

## Solution Comparisons

### Time and Space Complexity Comparison

| Solution | Time Complexity | Space Complexity |
|----------|----------------|------------------|
| Solution 1: Three-Phase Iterative | O(max(n, m)) | O(max(n, m)) |
| Solution 2: Bit-by-bit Computation | O(max(n, m)) | O(max(n, m)) |
| Solution 3: Built-in Functions | O(n + m) | O(max(n, m)) |
| Solution 4: Single-Loop Iterative | O(max(n, m)) | O(max(n, m)) |

### Solution Trade-offs

#### Solution 1: Three-Phase Iterative

- **Pros**: Explicitly handles all cases, follows a logical three-phase approach
- **Cons**: Contains repetitive code across the three phases, uses string slicing which can be inefficient, more verbose than other solutions

#### Solution 2: Bit-by-bit Computation

- **Pros**: Clean implementation, uses mathematical approach for bit manipulation
- **Cons**: Requires padding input strings which creates additional memory overhead

#### Solution 3: Built-in Functions

- **Pros**: Extremely concise and readable, leverages language features effectively
- **Cons**: Obscures the binary addition algorithm, may not work for extremely large inputs in languages with fixed-size integers

#### Solution 4: Single-Loop Iterative

- **Pros**: Efficient single loop implementation, no string padding needed, clean index-based approach
- **Cons**: Slightly more complex pointer management than padding-based solutions

### When to Use Each Solution

- **Use Solution 1** when you need explicit handling of each bit combination and prefer a step-by-step approach.
- **Use Solution 2** when you want a clean mathematical approach and input size isn't a concern.
- **Use Solution 3** when working in Python and want the most concise, readable code.
- **Use Solution 4** when you need an efficient solution that works well for strings of different lengths.

### Overall Recommendation

Solution 4 (Single-Loop Iterative) offers the best balance of efficiency and readability. It avoids the repetition in Solution 1, the padding overhead in Solution 2, and the potential limitations of Solution 3.

For interviews, Solution 4 demonstrates good understanding of the problem while being concise. Solution 3 might be preferred if you want to show knowledge of built-in functions, but be prepared to explain a manual approach as well.

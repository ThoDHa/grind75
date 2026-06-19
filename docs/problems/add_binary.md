# [Add Binary](https://leetcode.com/problems/add-binary/)

**Easy** | **15 minutes** | **Math, String, Bit Manipulation**

**Pattern:** [Simulation](../patterns/simulation/intuition.md)

**Practice:** [`practice/add_binary/solution.py`](../../practice/add_binary/solution.py)

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

### Three-Phase Iterative Approach

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

#### Approach

This solution processes the binary addition in three phases: first, it handles bits from both strings simultaneously, then it processes any remaining bits from string `a`, and finally any remaining bits from string `b`. In each phase, it explicitly handles each possible sum case (0, 1, 2, or 3) to determine the current bit and carry.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(max(n, m))`

We process each bit position once across the three loops.

##### Space Complexity: `O(max(n, m))`

The space needed for the result string, which is at most max(n, m) + 1 bits.

#### Key Insights

- Uses explicit logic for different possible bit combinations
- Processes strings from right to left by removing the last character in each iteration
- Handles the carry at the end after all digits are processed

### Bit-by-bit Computation

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

#### Approach

This solution simulates the binary addition process we do by hand, going from right to left. For each position, we add the corresponding bits from both numbers and the carry from the previous step. The result bit is the sum modulo 2, and the new carry is the integer division of the sum by 2.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(max(n, m))`

We process each bit position once, where n and m are the lengths of the input strings.

##### Space Complexity: `O(max(n, m))`

We create a new string to store the result, which has at most max(n, m) + 1 bits.

#### Key Insights

- Simulates the binary addition process bit-by-bit
- Uses modulo operation to determine the current bit value
- Uses integer division to determine the carry bit

### Single-Loop Iterative Approach

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

#### Approach

This iterative solution explicitly tracks indices for both strings and processes them in a single loop. It handles strings of different lengths and carries without padding or multiple loops.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(max(n, m))`

We process each bit position once in a single pass.

##### Space Complexity: `O(max(n, m))`

The space needed for the result string, which is at most max(n, m) + 1 bits.

#### Key Insights

- Handles both strings in a single loop
- Works efficiently for strings of different lengths
- Avoids unnecessary string padding or multiple loops

### Bit Manipulation

```python
def addBinary(self, a: str, b: str) -> str:
    # Parse the inputs into integers for the bitwise work
    x = int(a, 2)
    y = int(b, 2)

    # Add using only bitwise operations: XOR is the sum ignoring carries,
    # and (x & y) << 1 is the carry that must be propagated. Repeat until
    # there is no carry left to fold back in.
    while y:
        sum_without_carry = x ^ y
        carry = (x & y) << 1
        x = sum_without_carry
        y = carry

    # Strip the '0b' prefix to return the binary string
    return bin(x)[2:]
```

#### Approach

This solution performs the addition using the classic carry-propagation loop
built entirely from bitwise operators. The XOR of two values gives their sum at
each bit position while ignoring any carries, and the AND of the two values
(shifted left by one) gives exactly the carry bits. Folding the carry back in
repeatedly, the carry eventually becomes zero and `x` holds the final sum.

Being honest about the boundaries: `int(a, 2)` and `bin(...)` are still used for
input parsing and output formatting, so the I/O is not bitwise. The arithmetic
itself, however, never uses `+`: every bit of the sum is produced purely with
XOR, AND, and shift.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(max(n, m))`

Each iteration clears at least one carry bit, and the number of bits is bounded
by max(n, m) + 1, so the loop runs a number of times proportional to the input
length.

##### Space Complexity: `O(1)` for computation, `O(max(n, m))` for output

The arithmetic uses a constant number of integer variables, while the output
string is proportional to the input sizes.

#### Key Insights

- XOR computes the sum of two bits without their carry
- `(x & y) << 1` isolates and positions the carry for the next round
- The loop terminates because every pass pushes carries further left until they
  fall off entirely
- Demonstrates how addition can be expressed without the `+` operator

### Using Built-in Functions

```python
def addBinary(self, a: str, b: str) -> str:
    # Convert binary strings to integers, add them, then convert back to binary
    sum_int = int(a, 2) + int(b, 2)
    # Remove '0b' prefix from binary representation
    return bin(sum_int)[2:]
```

#### Approach

This solution leverages Python's built-in functions to convert binary strings to integers, perform the addition, and then convert the result back to a binary string.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n + m)`

Converting the strings to integers and back to binary takes linear time.

##### Space Complexity: `O(1)` for computation, `O(max(n, m))` for output

The space needed for computation is constant, but the output size is proportional to the input sizes.

#### Key Insights

- Takes advantage of Python's built-in conversion functions
- Very concise solution
- May not work for extremely large binary numbers due to potential integer overflow in some languages (but works in Python due to arbitrary precision integers)

## Comparison of Solutions

### Time Complexity

- **Three-Phase**: `O(max(n, m))` - Processes each bit position once across three phases
- **Bit-by-bit**: `O(max(n, m))` - Single loop over padded strings
- **Single-Loop**: `O(max(n, m))` - One-pass approach with index tracking
- **Bit Manipulation**: `O(max(n, m))` - Carry-propagation loop clears one carry bit per pass
- **Built-in Functions**: `O(n + m)` - Linear time for conversion operations

### Space Complexity

- **Three-Phase**: `O(max(n, m))` - Result string size
- **Bit-by-bit**: `O(max(n, m))` - Padded strings and result
- **Single-Loop**: `O(max(n, m))` - Result string only
- **Bit Manipulation**: `O(max(n, m))` for output, `O(1)` for computation
- **Built-in Functions**: `O(max(n, m))` for output, `O(1)` for computation

### Trade-offs

- The three-phase iterative approach has explicit logic but requires three separate loops
- The bit-by-bit computation is more elegant with padding but still requires a separate step
- The single-loop iterative approach offers the best balance of readability and efficiency with a single loop
- The bit manipulation approach expresses addition without the `+` operator, which is instructive, but still relies on `int()`/`bin()` for parsing and formatting
- Using built-in functions is extremely concise but may not work in languages without arbitrary precision integers

### When to Use Each

- **Three-Phase Iterative**: When clarity and explicit handling of each case is preferred
- **Bit-by-bit Computation**: When a more structured approach with consistent string lengths is desired
- **Single-Loop Iterative**: For most practical applications - best balance of efficiency and readability
- **Bit Manipulation**: When demonstrating how addition reduces to XOR and carry shifts, or in settings that favor bitwise reasoning
- **Built-in Functions**: When code brevity is paramount and language supports large integers

### Optimization Notes

- All solutions have the same time complexity for this problem, but with different constants
- The single-loop iterative approach avoids unnecessary string operations present in the three-phase iterative and bit-by-bit approaches
- The single-loop iterative approach demonstrates how to handle asymmetric inputs efficiently without padding
- Using built-in functions leverages built-in functionality but may have hidden overhead

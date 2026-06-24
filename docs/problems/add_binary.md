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

### Brute Force

```python
class Solution:
    def addBinary(self, a: str, b: str) -> str:
        i, j = len(a) - 1, len(b) - 1
        carry = 0
        result = []

        # Walk both strings from the least significant bit, exactly like
        # adding by hand on paper. Treat a missing digit as 0.
        while i >= 0 or j >= 0 or carry:
            total = carry
            if i >= 0:
                total += 1 if a[i] == "1" else 0
                i -= 1
            if j >= 0:
                total += 1 if b[j] == "1" else 0
                j -= 1
            # total is 0, 1, 2, or 3: the bit is its parity, the carry its half
            result.append("1" if total % 2 == 1 else "0")
            carry = total // 2

        # Bits were collected least-significant first, so reverse them
        return "".join(reversed(result))
```

#### Approach

The most intuitive idea is to mimic the column addition we learned for decimal numbers, only in base two. Starting from the rightmost bit of each string, we add the two digits plus any carry from the column to the right, write down the parity bit, and pass the carry leftward.

1. Set two indices `i` and `j` at the last character of `a` and `b`, and a `carry` of `0`.
2. Loop while either index is still in range or a carry remains. Each pass compares characters to `"1"` directly to add `0` or `1`, never converting the whole string to a number.
3. The current bit is `total % 2` and the next carry is `total // 2`, since `total` is at most `3`.
4. Bits are appended least-significant first, so reverse the collected list and join it into the result string.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(max(n, m))`

Each loop iteration consumes one bit position from the longer string (plus at most one extra pass for a trailing carry), so the work is linear in the longer input.

##### Space Complexity: `O(max(n, m))`

The result list holds at most `max(n, m) + 1` bits before it is joined into the output string.

#### Key Insights

- Mirrors pencil-and-paper addition: add a column, write the parity, carry the rest.
- Compares characters directly against `"1"`, so it never leans on `int(s, 2)` or `bin()` to do the arithmetic.
- Appending to a list and reversing once at the end avoids the quadratic cost of repeated string prepending.

### Bit-by-bit Computation

```python
class Solution:
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
class Solution:
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
class Solution:
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
class Solution:
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

- **Brute Force**: `O(max(n, m))` - One pass over the longer string, plus at most one carry pass
- **Bit-by-bit**: `O(max(n, m))` - Single loop over padded strings
- **Single-Loop**: `O(max(n, m))` - One-pass approach with index tracking
- **Bit Manipulation**: `O(max(n, m))` - Carry-propagation loop clears one carry bit per pass
- **Built-in Functions**: `O(n + m)` - Linear time for conversion operations

### Space Complexity

- **Brute Force**: `O(max(n, m))` - Result list size
- **Bit-by-bit**: `O(max(n, m))` - Padded strings and result
- **Single-Loop**: `O(max(n, m))` - Result string only
- **Bit Manipulation**: `O(max(n, m))` for output, `O(1)` for computation
- **Built-in Functions**: `O(max(n, m))` for output, `O(1)` for computation

### Trade-offs

- The brute force mirrors pencil-and-paper addition and stays library-free, comparing characters directly instead of parsing numbers, at the cost of an explicit reverse at the end
- The bit-by-bit computation is more uniform with padding but pays for the padding step and repeated string prepending
- The single-loop iterative approach offers the best balance of readability and efficiency, dropping the padding while still avoiding the brute force's reverse
- The bit manipulation approach expresses addition without the `+` operator, which is instructive, but still relies on `int()`/`bin()` for parsing and formatting
- Using built-in functions is extremely concise but defers the entire core task to `int(a, 2)` and `bin()`, and may not work in languages without arbitrary precision integers

### When to Use Each

- **Brute Force**: When learning the problem, or when a library-free, from-scratch baseline is required
- **Bit-by-bit Computation**: When a uniform approach with consistent string lengths is desired
- **Single-Loop Iterative**: For most practical applications - best balance of efficiency and readability
- **Bit Manipulation**: When demonstrating how addition reduces to XOR and carry shifts, or in settings that favor bitwise reasoning
- **Built-in Functions**: When code brevity is paramount and the language supports large integers

### Optimization Notes

- All solutions share the same linear time complexity for this problem, but with different constants
- The single-loop iterative approach avoids unnecessary string operations present in the brute force and bit-by-bit approaches
- The single-loop iterative approach demonstrates how to handle asymmetric inputs efficiently without padding
- The built-in approach leverages Python's arbitrary-precision integers but offloads the core arithmetic the problem is meant to teach

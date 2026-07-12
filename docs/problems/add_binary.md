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

#### Walkthrough

Let us watch the brute force run on Example 1: `a = "11"`, `b = "1"`, expected Output `"100"`.

We start with `i = 1` (last index of `a`), `j = 0` (last index of `b`), `carry = 0`, and an empty `result = []`. Each pass adds the in-range bits plus the carry into `total`, appends `total % 2` as the new bit, and keeps `total // 2` as the next `carry`.

| Step | bit `a[i]` | bit `b[j]` | `carry` in | `total` | appended bit | `carry` out | `result` after |
|------|------------|------------|------------|---------|--------------|-------------|----------------|
| 1 | `a[1]` = `1` | `b[0]` = `1` | `0` | `2` | `0` | `1` | `["0"]` |
| 2 | `a[0]` = `1` | none (`j` < 0) | `1` | `2` | `0` | `1` | `["0", "0"]` |
| 3 | none (`i` < 0) | none (`j` < 0) | `1` | `1` | `1` | `0` | `["0", "0", "1"]` |

After step 1, `i` drops to `0` and `j` drops to `-1`. After step 2, `i` drops to `-1`. By step 3 both indices are out of range, but `carry` is still `1`, so the loop runs once more to flush it: `total = 1`, which writes the final `1` bit and clears the carry to `0`. Now `i < 0`, `j < 0`, and `carry == 0`, so the loop stops.

The bits were collected least-significant first, so `result` holds `["0", "0", "1"]`. Reversing and joining gives `"100"`, which matches the expected Output `"100"`.

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

##### Time Complexity: `O(max(n, m)^2)`

The loop visits each bit position once, but `result = str(bit_sum % 2) + result` copies the entire result string on every iteration. Prepending to a string of growing length `1, 2, ..., max(n, m)` sums to quadratic work overall. Collecting bits in a list and reversing once at the end (as the brute force does) would bring this down to `O(max(n, m))`.

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

##### Time Complexity: `O(max(n, m)^2)`

The single pass visits each bit position once, but `result = str(current_sum % 2) + result` rebuilds the result string on every iteration, so the total work is quadratic in the longer input. Appending to a list and reversing once at the end would restore the linear bound.

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

##### Time Complexity: `O(max(n, m)^2)` worst case

The loop can run up to max(n, m) + 1 times (a carry can ripple one position per
pass, as in `0b111...1 + 1`), and each XOR, AND, and shift on Python's
arbitrary-precision integers costs `O(max(n, m))` bit operations when the values
span up to 10^4 bits. The worst case is therefore quadratic in the input length,
even though typical inputs resolve in far fewer passes.

##### Space Complexity: `O(max(n, m))`

Only a constant number of integer variables are used, but each holds an
arbitrary-precision integer of up to max(n, m) + 1 bits, and the output string
is proportional to the input sizes as well.

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

- **Brute Force**: `O(max(n, m))` - One pass over the longer string, plus at most one carry pass; list append keeps each step `O(1)`
- **Bit-by-bit**: `O(max(n, m)^2)` - Single loop over padded strings, but string prepending copies the result on every iteration
- **Single-Loop**: `O(max(n, m)^2)` - One pass with index tracking, but the same string prepending makes each step linear in the result built so far
- **Bit Manipulation**: `O(max(n, m)^2)` worst case - Up to max(n, m) carry-propagation passes, each doing `O(max(n, m))`-bit integer operations
- **Built-in Functions**: `O(n + m)` - Linear time for conversion operations

### Space Complexity

- **Brute Force**: `O(max(n, m))` - Result list size
- **Bit-by-bit**: `O(max(n, m))` - Padded strings and result
- **Single-Loop**: `O(max(n, m))` - Result string only
- **Bit Manipulation**: `O(max(n, m))` - The arbitrary-precision integers hold one bit per input bit, plus the output string
- **Built-in Functions**: `O(max(n, m))` for output, `O(1)` for computation

### Trade-offs

- The brute force mirrors pencil-and-paper addition and stays library-free, comparing characters directly instead of parsing numbers; its list-append-then-reverse pattern is what keeps it linear
- The bit-by-bit computation is more uniform with padding but pays for the padding step and, more importantly, the quadratic cost of repeated string prepending
- The single-loop iterative approach drops the padding and the final reverse, but its string prepending makes it quadratic; converting it to list append would combine the best of both
- The bit manipulation approach expresses addition without the `+` operator, which is instructive, but it still relies on `int()`/`bin()` for parsing and formatting and is worst-case quadratic on huge inputs
- Using built-in functions is extremely concise but defers the entire core task to `int(a, 2)` and `bin()`, and may not work in languages without arbitrary precision integers

### When to Use Each

- **Brute Force**: When learning the problem, or when a library-free, from-scratch baseline is required; it is also the only from-scratch version here with a linear bound
- **Bit-by-bit Computation**: When a uniform approach with consistent string lengths is desired and inputs are small enough that the quadratic prepending does not matter
- **Single-Loop Iterative**: When readability matters more than the asymptotic bound; switch the result to a list to make it linear for large inputs
- **Bit Manipulation**: When demonstrating how addition reduces to XOR and carry shifts, or in settings that favor bitwise reasoning
- **Built-in Functions**: When code brevity is paramount and the language supports large integers

### Optimization Notes

- Only the brute force and built-in approaches are truly linear here; the two string-prepending versions and the bit-manipulation loop are quadratic in the worst case
- Replacing `result = bit + result` with `result.append(bit)` plus one final reverse-join is the single change that makes the bit-by-bit and single-loop versions linear
- The single-loop iterative approach demonstrates how to handle asymmetric inputs without padding
- The built-in approach leverages Python's arbitrary-precision integers but offloads the core arithmetic the problem is meant to teach

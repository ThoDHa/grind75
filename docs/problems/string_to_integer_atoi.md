# [String to Integer (atoi)](https://leetcode.com/problems/string-to-integer-atoi/)

**Medium** | **30 minutes** | **String**

**Pattern:** [Simulation](../patterns/simulation/intuition.md)

**Practice:** [`practice/string_to_integer_atoi/solution.py`](../../practice/string_to_integer_atoi/solution.py)

Implement the `myAtoi(string s)` function, which converts a string to a 32-bit signed integer (similar to C/C++'s `atoi` function).

The algorithm for `myAtoi(string s)` is as follows:

1. Read in and ignore any leading whitespace.
2. Check if the next character (if not already at the end of the string) is `'-'` or `'+'`. Read this character in if it is either. This determines if the final result is negative or positive respectively. Assume the result is positive if neither is present.
3. Read in next the characters until the next non-digit character or the end of the input is reached. The rest of the string is ignored.
4. Convert these digits into an integer (i.e. "123" -> 123, "0032" -> 32). If no digits were read, then the integer is 0. Change the sign as necessary (from step 2).
5. If the integer is out of the 32-bit signed integer range `[-2^31, 2^31 - 1]`, then clamp the integer so that it remains in the range. Specifically, integers less than `-2^31` should be clamped to `-2^31`, and integers greater than `2^31 - 1` should be clamped to `2^31 - 1`.
6. Return the integer as the final result.

**Note:**
- Only the space character `' '` is considered a whitespace character.
- Do not ignore any characters other than the leading whitespace or the rest of the string after the digits.

## Examples

### Example 1

**Input:** s = `"42"`

**Output:** `42`

**Explanation:** The underlined characters are what is read in, the caret is the current reader position.

```
Step 1: "42" (no characters read because there is no leading whitespace)
         ^
Step 2: "42" (no characters read because there is neither a '-' nor '+')
         ^
Step 3: "42" (characters "42" are read in)
           ^
```

The parsed integer is 42.
Since 42 is in the range `[-2^31, 2^31 - 1]`, the final result is 42.

### Example 2

**Input:** s = `"   -42"`

**Output:** `-42`

**Explanation:**

```
Step 1: "   -42" (leading whitespace is read and ignored)
            ^
Step 2: "   -42" ('-' is read, so the result should be negative)
             ^
Step 3: "   -42" (characters "42" are read in)
               ^
```

The parsed integer is -42.
Since -42 is in the range `[-2^31, 2^31 - 1]`, the final result is -42.

### Example 3

**Input:** s = `"4193 with words"`

**Output:** `4193`

**Explanation:**

```
Step 1: "4193 with words" (no characters read because there is no leading whitespace)
         ^
Step 2: "4193 with words" (no characters read because there is neither a '-' nor '+')
         ^
Step 3: "4193 with words" (characters "4193" are read in; reading stops because the next character is a non-digit)
             ^
```

The parsed integer is 4193.
Since 4193 is in the range `[-2^31, 2^31 - 1]`, the final result is 4193.

## Constraints

- `0 <= s.length <= 200`
- `s` consists of English letters (lower-case and upper-case), digits (0-9), `' '`, `'+'`, `'-'`, and `'.'`.

## Solutions

### Manual Parsing

```python
class Solution:
    def myAtoi(self, s: str) -> int:
        """
        Step-by-step manual parsing approach
        """
        if not s:
            return 0

        INT_MAX = 2**31 - 1
        INT_MIN = -2**31

        i = 0
        n = len(s)

        # Step 1: Skip leading whitespace
        while i < n and s[i] == ' ':
            i += 1

        if i == n:  # Only whitespace
            return 0

        # Step 2: Determine sign
        sign = 1
        if s[i] in '+-':
            if s[i] == '-':
                sign = -1
            i += 1

        # Step 3: Build number digit by digit
        result = 0
        while i < n and s[i].isdigit():
            digit = ord(s[i]) - ord('0')  # Convert char to int

            # Check overflow before updating result
            if result > (INT_MAX - digit) // 10:
                return INT_MAX if sign == 1 else INT_MIN

            result = result * 10 + digit
            i += 1

        return sign * result
```

#### Approach

This solution provides a **step-by-step manual implementation** that closely follows the problem specification. It demonstrates explicit character-to-digit conversion using ASCII values and shows clear separation of each parsing step. This approach is most educational for understanding the underlying mechanics.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Single pass through the string with constant time operations per character.

##### Space Complexity: `O(1)`

Uses only a few variables regardless of input size.

#### Key Insights

- Converting a character to its digit with `ord(s[i]) - ord('0')` avoids any library call and makes the digit extraction explicit.
- Skipping leading spaces, reading the sign, and reading digits are three separate phases that must run in this exact order: a sign that appears after a digit (or after a space following a sign) terminates parsing rather than restarting it.
- The overflow guard `result > (INT_MAX - digit) // 10` is checked before the multiply, so the running total never leaves the 32-bit range even momentarily.

### State Machine

```python
class Solution:
    def myAtoi(self, s: str) -> int:
        """
        State machine approach with explicit state transitions
        """
        # Define constants
        INT_MAX = 2**31 - 1
        INT_MIN = -2**31

        # State variables
        index = 0
        sign = 1
        result = 0

        # Step 1: Skip leading whitespaces
        while index < len(s) and s[index] == ' ':
            index += 1

        # Check if we've reached end of string
        if index >= len(s):
            return 0

        # Step 2: Handle sign
        if s[index] == '+':
            sign = 1
            index += 1
        elif s[index] == '-':
            sign = -1
            index += 1

        # Step 3: Convert digits and handle overflow
        while index < len(s) and s[index].isdigit():
            digit = int(s[index])

            # Check for overflow before adding the digit
            if result > INT_MAX // 10 or (result == INT_MAX // 10 and digit > INT_MAX % 10):
                return INT_MAX if sign == 1 else INT_MIN

            result = result * 10 + digit
            index += 1

        return sign * result
```

#### Approach

This solution implements a **state machine** that processes the string character by character, following the exact algorithm specification. It handles each step explicitly: skip whitespace, parse sign, convert digits while checking for overflow. The key insight is checking for overflow before performing the multiplication to prevent integer overflow during computation.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

We process each character in the string at most once, where n is the length of the string.

##### Space Complexity: `O(1)`

Uses only constant extra space for variables regardless of input size.

#### Key Insights

- Splitting the overflow test into `result > INT_MAX // 10` and the boundary case `result == INT_MAX // 10 and digit > INT_MAX % 10` mirrors how a fixed-width integer would overflow, while keeping every intermediate value inside Python ints that never actually overflow.
- The single shared clamp `INT_MAX if sign == 1 else INT_MIN` works because `2^31 - 1` and `-2^31` are the only two saturation targets, selected purely by the sign captured earlier.
- Each character is visited at most once and the state (`sign`, `result`, `index`) fully determines the next transition, which is what makes this a state machine rather than backtracking.

### Strip and Parse

```python
class Solution:
    def myAtoi(self, s: str) -> int:
        """
        Strip leading spaces, scan the sign and digits, then convert
        """
        INT_MAX = 2**31 - 1
        INT_MIN = -2**31

        s = s.lstrip(' ')
        if not s:
            return 0

        sign = 1
        idx = 0
        if s[0] == '-':
            sign = -1
            idx = 1
        elif s[0] == '+':
            idx = 1

        digits = ''
        while idx < len(s) and s[idx].isdigit():
            digits += s[idx]
            idx += 1

        if not digits:
            return 0

        result = sign * int(digits)
        return max(INT_MIN, min(INT_MAX, result))
```

#### Approach

This solution keeps the explicit phase structure of the manual parser but offloads the final numeric conversion to Python's `int()`. It uses `lstrip(' ')` to drop leading spaces (only the space character, matching the specification), reads an optional sign, then collects the consecutive digit run into a substring. Conversion and clamping happen once at the end rather than per character.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

`lstrip` and the digit scan each run linearly in the string length, and `int()` is linear in the number of digits collected.

##### Space Complexity: `O(n)`

The accumulated `digits` substring can grow to the length of the input in the worst case, unlike the running-integer approaches that use constant space.

#### Key Insights

- Restricting the strip to the literal space character (`lstrip(' ')`) is essential: `str.strip()` with no argument would also remove tabs and newlines, which the specification forbids.
- Building the digit substring lets Python's arbitrary-precision `int()` parse any length safely, so the only overflow handling needed is a final `max`/`min` clamp.
- Returning early when `digits` is empty covers the "sign only" and "leading non-digit" cases without special-casing them.

### Regular Expression

```python
import re

class Solution:
    def myAtoi(self, s: str) -> int:
        """
        Regular expression approach for pattern matching
        """
        INT_MAX = 2**31 - 1
        INT_MIN = -2**31

        # Regular expression to match the atoi pattern
        # ^ - start of string, \s* - zero or more whitespaces
        # [+-]? - optional sign, \d+ - one or more digits
        match = re.match(r'^\s*([+-]?\d+)', s)

        if not match:
            return 0

        # Extract the matched number string
        num_str = match.group(1)
        result = int(num_str)

        # Clamp to 32-bit signed integer range
        return max(INT_MIN, min(INT_MAX, result))
```

#### Approach

This solution uses **regular expressions** to extract the valid integer pattern from the string in one step. The regex `^\s*([+-]?\d+)` matches leading whitespace, optional sign, and digits. This approach is more concise but relies on Python's built-in `int()` function for conversion and manual clamping for overflow.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Regular expression matching is linear in string length, and `int()` conversion is also linear.

##### Space Complexity: `O(1)`

Uses constant extra space (the regex compilation is cached by Python).

#### Key Insights

- The pattern `^\s*([+-]?\d+)` encodes the entire parsing grammar (leading whitespace, optional sign, digit run) in one expression, so `int()` only ever receives a well-formed token.
- A missing match (empty string, sign with no digits, leading letters) returns `None`, which maps directly to the required `0` result.
- One caveat: `\s` matches all whitespace, not just the space character; this is acceptable only because the constraints restrict whitespace in `s` to the space character. A hand-written parser does not depend on that assumption.

## Comparison of Solutions

### Time Complexity

- **Manual Parsing**: `O(n)` - Character-by-character processing
- **State Machine**: `O(n)` - Single pass with explicit state handling
- **Strip and Parse**: `O(n)` - Linear strip and digit scan plus `int()` conversion
- **Regular Expression**: `O(n)` - Pattern matching plus conversion

### Space Complexity

- **Manual Parsing**: `O(1)` - Constant space usage
- **State Machine**: `O(1)` - Constant space usage
- **Strip and Parse**: `O(n)` - Accumulates the digit substring before conversion
- **Regular Expression**: `O(1)` - Constant space (regex cached)

### Trade-offs

- **Manual Parsing**: Code clarity is good and edge case handling is very explicit, with best-in-class performance and good maintainability. It has the highest learning value and requires no dependencies.
- **State Machine**: Code clarity is good and edge case handling is explicit, with best-in-class performance and good maintainability. Learning value is high and it requires no dependencies.
- **Strip and Parse**: Code clarity is good and the phase structure stays explicit, but it leans on `int()` for the conversion and uses `O(n)` space for the digit substring. It avoids manual overflow arithmetic in favor of a final clamp.
- **Regular Expression**: Code clarity is excellent and maintainability is excellent, but edge case handling is implicit (relying on the regex plus `int()`). Performance is good with some regex overhead, learning value is medium, and it depends on the `re` module.

### When to Use Each

- **Manual Parsing**: Best for learning/teaching the underlying concepts and when you need full control over every step
- **State Machine**: Best for production code (recommended): robust, efficient, and handles all edge cases explicitly
- **Strip and Parse**: When you want explicit phases but prefer to delegate the numeric conversion and overflow clamping to the language
- **Regular Expression**: When code brevity and readability are prioritized over micro-optimizations

### Optimization Notes

- The **State Machine** solution is the recommended choice for production: it runs in `O(n)` time and `O(1)` space, requires no external dependencies, and handles every parsing state (whitespace, sign, digits, overflow) explicitly.
- Key implementation detail: check for overflow *before* performing the multiplication `result * 10 + digit`. Comparing against `INT_MAX // 10` and `INT_MAX % 10` prevents the intermediate value from exceeding the 32-bit range, then clamp to `INT_MAX` or `INT_MIN` based on the sign.
- The **Strip and Parse** and **Regular Expression** approaches offload the numeric conversion (and, for the regex, the edge case handling) to Python's `int()`. They are concise but use `O(n)` space for the digit token, hide the parsing mechanics, and depend on the language for overflow-free arithmetic before the final clamp.
- Common pitfall: the many edge cases (empty string, only whitespace, only a sign, non-digit interruptions, and overflow) make this problem tricky; the task tests faithful implementation of an exact specification rather than algorithmic creativity, so each step must follow the stated order precisely.

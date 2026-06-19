# [Valid Palindrome](https://leetcode.com/problems/valid-palindrome)

**Easy** | **15 minutes** | **String**

**Pattern:** [Two Pointers](../patterns/two_pointers/intuition.md)

**Practice:** [`practice/valid_palindrome/solution.py`](../../practice/valid_palindrome/solution.py)

A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and
removing all non-alphanumeric characters, it reads the same forward and backward.
Alphanumeric characters include letters and numbers.

Given a string `s`, return `true` if it is a palindrome, or `false` otherwise.

## Examples

### Example 1

**Input:** `s = "A man, a plan, a canal: Panama"`

**Output:** `true`

**Explanation:** `"amanaplanacanalpanama"` is a palindrome.

### Example 2

**Input:** `s = "race a car"`

**Output:** `false`

**Explanation:** `"raceacar"` is not a palindrome.

### Example 3

**Input:** `s = " "`

**Output:** `true`

**Explanation:** `s` is an empty string `""` after removing non-alphanumeric characters.
Since an empty string reads the same forward and backward, it is a palindrome.

## Constraints

- `1 <= s.length <= 2 * 10^5`
- `s` consists only of printable ASCII characters.

## Solutions

### Filter then Two Pointers

```python
class Solution:
    def isPalindrome(self, s: str) -> bool:
        filtered = [c.lower() for c in s if c.isalnum()]
        left, right = 0, len(filtered) - 1
        while left < right:
            if filtered[left] != filtered[right]:
                return False
            left += 1
            right -= 1
        return True
```

#### Approach

The most direct way to read the problem is to do exactly what it describes:
first build the cleaned form of the string, then check whether that cleaned form
reads the same forward and backward.

1. Walk the input once, keeping only the characters for which `isalnum()` is
   true and converting each to lowercase. Collect them into a list `filtered`.
2. Place a `left` pointer at the start of `filtered` and a `right` pointer at the
   end.
3. While `left < right`, compare the two characters. If they differ, the cleaned
   string is not a palindrome, so return `False`.
4. Move `left` inward and `right` inward and repeat.
5. If the pointers meet without a mismatch, every mirrored pair agreed, so return
   `True`.

Separating the cleaning step from the comparison step keeps each phase simple at
the cost of an extra pass and an `O(n)` buffer.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Building `filtered` visits each of the `n` characters once, and the two-pointer
scan visits each surviving character at most once, so the work is linear.

##### Space Complexity: `O(n)`

The `filtered` list can hold up to `n` characters when every character is
alphanumeric.

#### Key Insights

- Cleaning first turns the messy original string into a uniform sequence, so the
  palindrome check has no special cases for punctuation or capitalization.
- The two-pointer comparison needs no string reversal; it simply walks from both
  ends toward the middle.

### Two Pointers with Inline Filtering

```python
class Solution:
    def isPalindrome(self, s: str) -> bool:
        left, right = 0, len(s) - 1
        while left < right:
            while left < right and not s[left].isalnum():
                left += 1
            while left < right and not s[right].isalnum():
                right -= 1
            if s[left].lower() != s[right].lower():
                return False
            left += 1
            right -= 1
        return True
```

#### Approach

This refinement removes the auxiliary buffer by filtering on the fly. Instead of
materializing a cleaned string, the pointers skip past non-alphanumeric
characters as they advance.

1. Start `left` at index `0` and `right` at the last index of the original
   string `s`.
2. While `left < right`, first advance `left` rightward past any character that
   is not alphanumeric, and advance `right` leftward past any such character.
   Each inner loop keeps the `left < right` guard so the pointers never cross.
3. Compare `s[left].lower()` with `s[right].lower()`. If they differ, return
   `False`.
4. Move both pointers one step inward and continue.
5. When the pointers meet or cross, every alphanumeric pair matched, so return
   `True`.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Each pointer only ever moves toward the other, so across the whole run every
character is examined a constant number of times.

##### Space Complexity: `O(1)`

Only the two integer pointers are stored; no copy of the input is made.

#### Key Insights

- Skipping non-alphanumeric characters inline avoids the separate cleaning pass
  and the `O(n)` buffer it requires.
- The inner `while` loops must retain the `left < right` condition; otherwise a
  string of only punctuation could advance a pointer past the other and index out
  of bounds.
- Lowercasing a single character during the comparison keeps the original string
  untouched.

### Filter and Reverse

```python
class Solution:
    def isPalindrome(self, s: str) -> bool:
        cleaned = "".join(c.lower() for c in s if c.isalnum())
        return cleaned == cleaned[::-1]
```

#### Approach

When clarity matters more than memory, Python's slicing makes the palindrome
check a single expression.

1. Use a generator expression to keep only alphanumeric characters and lowercase
   each one, joining them into the string `cleaned`.
2. Build the reverse of `cleaned` with the slice `cleaned[::-1]`.
3. Return whether `cleaned` equals its reverse.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

Cleaning the string and producing its reverse each touch every character once.

##### Space Complexity: `O(n)`

Both `cleaned` and its reversed slice are new strings whose size grows with the
input.

#### Key Insights

- Slice reversal expresses the palindrome test declaratively, trading the
  in-place comparison for readability.
- The generator expression filters and lowercases in one pass before `join`
  assembles the result.

### Builtin Filter and Reverse

```python
class Solution:
    def isPalindrome(self, s: str) -> bool:
        cleaned = "".join(filter(str.isalnum, s)).lower()
        return cleaned == cleaned[::-1]
```

#### Approach

This is the most library-driven form. It delegates the filtering to the built-in
`filter` and lowercases the whole result at once.

1. Pass the unbound method `str.isalnum` and the string `s` to `filter`, which
   yields only the alphanumeric characters.
2. Join those characters and call `.lower()` once on the assembled string to get
   `cleaned`.
3. Return whether `cleaned` equals its reverse `cleaned[::-1]`.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

`filter`, `join`, `lower`, and the reversal each process the characters a
constant number of times.

##### Space Complexity: `O(n)`

The joined string and its reversed copy both scale with the input length.

#### Key Insights

- Lowercasing the joined string once is slightly cheaper than lowercasing each
  character individually, since the conversion happens in a single C-level call.
- Passing `str.isalnum` directly to `filter` avoids writing an explicit lambda or
  comprehension while keeping the intent clear.

## Comparison of Solutions

### Time Complexity

- **Filter then Two Pointers**: `O(n)` - one cleaning pass plus a linear scan.
- **Two Pointers with Inline Filtering**: `O(n)` - each pointer advances monotonically.
- **Filter and Reverse**: `O(n)` - cleaning and reversal are both linear.
- **Builtin Filter and Reverse**: `O(n)` - built-in passes are each linear.

### Space Complexity

- **Filter then Two Pointers**: `O(n)` - stores the cleaned characters.
- **Two Pointers with Inline Filtering**: `O(1)` - only two index pointers.
- **Filter and Reverse**: `O(n)` - builds a cleaned string and its reverse.
- **Builtin Filter and Reverse**: `O(n)` - builds a cleaned string and its reverse.

### Trade-offs

- Filtering first keeps each phase easy to follow but pays for an `O(n)` buffer.
- Inline filtering reaches `O(1)` space at the cost of two nested skip loops that
  must guard against the pointers crossing.
- The reverse-based forms are the shortest to read but copy the input twice.

### When to Use Each

- **Two Pointers with Inline Filtering**: Preferred when space matters or the
  string is very large, since it allocates nothing beyond two integers.
- **Filter then Two Pointers**: A good teaching form that separates cleaning from
  checking without relying on slice tricks.
- **Filter and Reverse** / **Builtin Filter and Reverse**: Best for quick,
  readable code where the extra `O(n)` memory is acceptable.

### Optimization Notes

- The inline two-pointer approach processes the input in place and never builds a
  cleaned copy, making it the most memory-efficient option.
- In the inline approach, retaining the `left < right` guard inside both skip
  loops is essential to avoid indexing past the end on all-punctuation input.
- The builtin form lowercases the joined string once rather than per character,
  shifting that work into a single optimized call.

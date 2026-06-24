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

### Brute Force

```python
class Solution:
    def isPalindrome(self, s: str) -> bool:
        cleaned = []
        for c in s:
            o = ord(c)
            if ord("0") <= o <= ord("9") or ord("a") <= o <= ord("z"):
                cleaned.append(c)
            elif ord("A") <= o <= ord("Z"):
                # Convert uppercase to lowercase by hand: 'A' and 'a' differ by 32
                cleaned.append(chr(o + (ord("a") - ord("A"))))
        n = len(cleaned)
        for i in range(n // 2):
            if cleaned[i] != cleaned[n - 1 - i]:
                return False
        return True
```

#### Approach

The problem hinges on two rules: which characters count as alphanumeric, and how
to fold uppercase onto lowercase. The most self-derivable solution spells both
rules out by hand instead of leaning on `str.isalnum` or `str.lower`, then checks
the result by comparing mirrored positions.

1. Walk the input once. For each character, take its code point with `ord`.
2. Keep it only when its code point falls inside the digit range `'0'..'9'` or
   the lowercase range `'a'..'z'`. If it falls inside the uppercase range
   `'A'..'Z'`, shift it down by `ord('a') - ord('A')` (32) to lowercase it before
   keeping it. Discard everything else.
3. Compare `cleaned[i]` with `cleaned[n - 1 - i]` for the first half of the
   cleaned list. Any mismatch means it is not a palindrome, so return `False`.
4. If every mirrored pair agrees, return `True`.

Defining the character classes through explicit code-point ranges is the core
lesson here; the rest is the same mirror comparison every palindrome check uses.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

The cleaning pass touches each of the `n` characters once, and the mirror
comparison walks at most half the cleaned list, so the work is linear.

##### Space Complexity: `O(n)`

The `cleaned` list can hold up to `n` characters when every character is
alphanumeric.

#### Key Insights

- Spelling out the alphanumeric test and the case fold with raw `ord` arithmetic
  shows exactly what `isalnum` and `lower` do under the hood.
- Comparing index `i` against `n - 1 - i` checks both ends at once without a
  second pointer or a reversed copy.
- Only the first half needs checking; the middle character of an odd-length
  string mirrors itself.

#### Walkthrough

Trace the Brute Force solution on Example 1, `s = "A man, a plan, a canal: Panama"`.

First, the cleaning pass walks every character once. Each letter is kept (and
lowercased if it was uppercase) while spaces, commas, and the colon are dropped.
`'A'` has code point `65`, inside the uppercase range, so it is shifted down by
`32` to `'a'`; the spaces and punctuation fail every range test and are discarded.
After this pass, `cleaned` holds:

`['a','m','a','n','a','p','l','a','n','a','c','a','n','a','l','p','a','n','a','m','a']`

That is the string `amanaplanacanalpanama`, so `n = 21`.

Next, the mirror comparison checks `cleaned[i]` against `cleaned[n - 1 - i]` for
`i` from `0` up to `n // 2 - 1`, that is `i = 0..9`:

| `i` | `cleaned[i]` | `n - 1 - i` | `cleaned[n - 1 - i]` | Match? |
|-----|--------------|-------------|----------------------|--------|
| 0   | `a`          | 20          | `a`                  | yes    |
| 1   | `m`          | 19          | `m`                  | yes    |
| 2   | `a`          | 18          | `a`                  | yes    |
| 3   | `n`          | 17          | `n`                  | yes    |
| 4   | `a`          | 16          | `a`                  | yes    |
| 5   | `p`          | 15          | `p`                  | yes    |
| 6   | `l`          | 14          | `l`                  | yes    |
| 7   | `a`          | 13          | `a`                  | yes    |
| 8   | `n`          | 12          | `n`                  | yes    |
| 9   | `a`          | 11          | `a`                  | yes    |

Every mirrored pair agrees. The loop stops at `i = 10` because `21 // 2 == 10`,
and index `10` (the middle `c`) mirrors itself, so it needs no check. No mismatch
ever fired, so the function returns `True`, which matches the expected Output for
Example 1.

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

- **Brute Force**: `O(n)` - a hand-written cleaning pass plus a half-length mirror scan.
- **Filter then Two Pointers**: `O(n)` - one cleaning pass plus a linear scan.
- **Two Pointers with Inline Filtering**: `O(n)` - each pointer advances monotonically.
- **Filter and Reverse**: `O(n)` - cleaning and reversal are both linear.
- **Builtin Filter and Reverse**: `O(n)` - built-in passes are each linear.

### Space Complexity

- **Brute Force**: `O(n)` - stores the hand-cleaned characters.
- **Filter then Two Pointers**: `O(n)` - stores the cleaned characters.
- **Two Pointers with Inline Filtering**: `O(1)` - only two index pointers.
- **Filter and Reverse**: `O(n)` - builds a cleaned string and its reverse.
- **Builtin Filter and Reverse**: `O(n)` - builds a cleaned string and its reverse.

### Trade-offs

- Brute Force defines the alphanumeric test and case fold from scratch with
  `ord` arithmetic, showing what the built-ins do, but is the most verbose form.
- Filtering first keeps each phase easy to follow but pays for an `O(n)` buffer.
- Inline filtering reaches `O(1)` space at the cost of two nested skip loops that
  must guard against the pointers crossing.
- The reverse-based forms are the shortest to read but copy the input twice.

### When to Use Each

- **Brute Force**: As a teaching baseline that derives the character-class rules
  by hand, without relying on `isalnum` or `lower`.
- **Two Pointers with Inline Filtering**: Preferred when space matters or the
  string is very large, since it allocates nothing beyond two integers.
- **Filter then Two Pointers**: A good teaching form that separates cleaning from
  checking without relying on slice tricks.
- **Filter and Reverse** / **Builtin Filter and Reverse**: Best for quick,
  readable code where the extra `O(n)` memory is acceptable.

### Optimization Notes

- The Brute Force form spells out alphanumeric and case-fold logic with `ord`
  arithmetic; the other forms hand that work to `isalnum` and `lower`, which do
  the same checks in a single optimized C-level call.
- The inline two-pointer approach processes the input in place and never builds a
  cleaned copy, making it the most memory-efficient option.
- In the inline approach, retaining the `left < right` guard inside both skip
  loops is essential to avoid indexing past the end on all-punctuation input.
- The builtin form lowercases the joined string once rather than per character,
  shifting that work into a single optimized call.

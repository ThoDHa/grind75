# [Letter Combinations of a Phone Number](https://leetcode.com/problems/letter-combinations-of-a-phone-number/)

**Medium** | **30 minutes** | **Hash Table, String, Backtracking**

**Pattern:** [Backtracking](../patterns/backtracking_exploration/intuition.md)

**Practice:** [`practice/letter_combinations_of_a_phone_number/solution.py`](../../practice/letter_combinations_of_a_phone_number/solution.py)

Given a string containing digits from `2-9` inclusive, return all possible letter combinations that the number could represent. Return the answer in **any order**.

A mapping of digits to letters (just like on the telephone buttons) is given below. Note that `1` does not map to any letters.

![Phone Keypad](assets/letter_combinations_keypad.png)

## Examples

### Example 1

**Input:** `digits = "23"`

**Output:** `["ad","ae","af","bd","be","bf","cd","ce","cf"]`

### Example 2

**Input:** `digits = ""`

**Output:** `[]`

**Explanation:** An empty input maps to no combinations.

### Example 3

**Input:** `digits = "2"`

**Output:** `["a","b","c"]`

## Constraints

- `0 <= digits.length <= 4`
- `digits[i]` is a digit in the range `['2', '9']`.

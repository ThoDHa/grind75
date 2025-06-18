# [Ransom Note](https://leetcode.com/problems/ransom-note/)

Easy - 15 minutes - Hash Table, String, Counting

Given two strings `ransomNote` and `magazine`, return `true` if `ransomNote` can be constructed from `magazine` and `false` otherwise.

Each letter in `magazine` can only be used once in `ransomNote`.

## Examples

### Example 1

**Input:** `ransomNote = "a"`, `magazine = "b"`

**Output:** `false`

### Example 2

**Input:** `ransomNote = "aa"`, `magazine = "ab"`

**Output:** `false`

### Example 3

**Input:** `ransomNote = "aa"`, `magazine = "aab"`

**Output:** `true`

## Constraints

- `1 <= ransomNote.length, magazine.length <= 10^5`
- `ransomNote` and `magazine` consist of lowercase English letters.

## Solutions

### Solution 1: Using Dictionary Counter

```python
class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        if len(ransomNote) > len(magazine):
            return False
        counter = {}

        for c in magazine:
            counter[c] = counter.get(c, 0) + 1
        
        for c in ransomNote:
            if counter.get(c, 0) == 0:
                return False
            counter[c] -= 1
        return True
```

#### Approach

This solution uses a hash map to count the occurrences of each character in the magazine. We first check if the ransom note is longer than the magazine - if so, it's immediately impossible to construct the note. Then we:

1. Build a frequency counter of all characters in the magazine
2. Iterate through the ransom note, checking if each character is available in sufficient quantity
3. For each character in the ransom note, we decrement its count in our counter
4. If at any point we need a character that isn't available, we return `False`

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m + n)`

We iterate through the magazine string once (of length m) to build our counter dictionary, and then through the ransom note once (of length n) to check if it can be constructed. All operations inside the loop (dictionary lookups and updates) are `O(1)`.

##### Space Complexity: `O(k)`

Where `k` is the number of unique characters in the magazine. In the worst case, this would be 26 (for lowercase English letters), which is a constant. So effectively, the space complexity is `O(1)`.

#### Key Insights

- The early length check (`len(ransomNote) > len(magazine)`) is a key optimization that avoids unnecessary processing
- Using a hash map/dictionary provides efficient lookups and updates for character counts
- The solution efficiently handles arbitrary characters, not just lowercase letters
- We only need a single pass through each string, making this solution optimal in terms of time complexity

### Solution 2: Using Python's Counter

```python
from collections import Counter

class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        if len(ransomNote) > len(magazine):
            return False
        
        magazine_counts = Counter(magazine)
        ransom_counts = Counter(ransomNote)
        
        for char, count in ransom_counts.items():
            if magazine_counts[char] < count:
                return False
                
        return True
```

#### Approach

This solution leverages Python's built-in `Counter` class, which is specifically designed for counting hashable objects. The approach is conceptually similar to Solution 1:

1. Create frequency counters for both the magazine and ransom note
2. Check if each character in the ransom note appears in the magazine with sufficient frequency
3. Return `False` if any character in the ransom note exceeds its count in the magazine

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m + n)`

Creating the Counter objects requires one pass through each string (magazine of length m and ransom note of length n). The comparison loop iterates through unique characters in the ransom note, which is at most n iterations.

##### Space Complexity: `O(k)`

We store two Counter objects, each with at most k unique characters (where k ≤ 26 for lowercase English letters). This is effectively `O(1)` space.

#### Key Insights

- Python's Counter class streamlines the process of counting and comparing character frequencies
- Creating two counters and then comparing them allows for a cleaner, more readable implementation
- This approach is more declarative than imperative, focusing on what we want (compare frequencies) rather than how to do it
- Counter objects handle missing keys gracefully, eliminating the need for explicit default value handling

### Solution 3: Using Array Counter

```python
class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        if len(ransomNote) > len(magazine):
            return False
        
        # Array of size 26 for lowercase letters
        counts = [0] * 26
        
        # Count character occurrences in magazine
        for char in magazine:
            counts[ord(char) - ord('a')] += 1
        
        # Check if we can construct the ransom note
        for char in ransomNote:
            index = ord(char) - ord('a')
            if counts[index] <= 0:
                return False
            counts[index] -= 1
            
        return True
```

#### Approach

This solution takes advantage of the constraint that all characters are lowercase English letters:

1. Create a fixed-size array with 26 elements (one for each lowercase letter)
2. Count the frequency of each character in the magazine by mapping characters to array indices
3. For each character in the ransom note, check if it's available and decrement its count
4. Return `False` if any required character isn't available

#### Time and Space Complexity Analysis

##### Time Complexity: `O(m + n)`

We make one pass through the magazine string (of length m) to populate our counts array, and one pass through the ransom note (of length n) to check if it can be constructed. Array indexing and updates are `O(1)` operations.

##### Space Complexity: `O(1)`

The solution uses a fixed-size array of 26 elements, regardless of the input size. This is constant space complexity.

#### Key Insights

- Using an array is most memory-efficient when the character set is known and limited
- Array indexing with `ord(char) - ord('a')` provides a direct mapping from characters to indices
- This approach avoids hash computation overhead that would be present in dictionary-based solutions
- For very large inputs, this solution may have better cache locality due to the contiguous memory of arrays## Comparison of Solutions

### Time Complexity

- **Dictionary Counter**: `O(m + n)` - One pass through magazine and one through ransom note
- **Python Counter**: `O(m + n)` - Same complexity as dictionary approach
- **Array Counter**: `O(m + n)` - One pass through each string with direct array indexing

### Space Complexity

- **Dictionary Counter**: `O(k)` - Where k is number of unique characters (at most 26), effectively `O(1)`
- **Python Counter**: `O(k)` - Same as dictionary approach, effectively `O(1)`
- **Array Counter**: `O(1)` - Fixed size array (26 elements) regardless of input size

### Comparison of Solutions

#### Trade-offs

- The dictionary solution works with any character set but has slight hash table overhead
- The Counter solution is most concise and leverages Python's built-in optimizations
- The array solution has the best memory efficiency but is limited to lowercase letters only

#### When to Use Each

- **Dictionary Counter**: When dealing with arbitrary character sets or in languages without specialized counter structures
- **Python Counter**: When working in Python and prioritizing code readability and conciseness
- **Array Counter**: When memory optimization is critical and character set is limited to lowercase letters

#### Optimization Notes

- Early length check (`len(ransomNote) > len(magazine)`) provides a quick fail path
- For very large inputs with limited character set, the array-based approach may have better cache locality
- All solutions are single-pass which is optimal for this problem
- Using direct array indexing avoids hash computation overhead for small, fixed character sets

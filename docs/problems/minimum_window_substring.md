# [Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/)

**Hard** | **45 minutes** | **Hash Table, String, Sliding Window**

**Pattern:** [Sliding Window](../patterns/sliding_window/intuition.md)

**Practice:** [`practice/minimum_window_substring/solution.py`](https://github.com/ThoDHa/grind75/blob/main/practice/minimum_window_substring/solution.py)

Given two strings s and t of lengths m and n respectively, return the **minimum window substring** of s such that every character in t (including duplicates) is included in the window. If there is no such substring, return the empty string "".

The testcases will be generated such that the answer is **unique**.

## Examples

### Example 1

**Input:** s = `"ADOBECODEBANC"`, t = `"ABC"`

**Output:** `"BANC"`

**Explanation:** The minimum window substring `"BANC"` includes 'A', 'B', and 'C' from string t.

### Example 2

**Input:** s = `"a"`, t = `"a"`

**Output:** `"a"`

**Explanation:** The entire string s is the minimum window.

### Example 3

**Input:** s = `"a"`, t = `"aa"`

**Output:** `""`

**Explanation:** Both 'a's from t must be included in the window.
Since the largest window of s only has one 'a', return empty string.

## Constraints

- `m == s.length`
- `n == t.length`
- `1 <= m, n <= 10^5`
- `s` and `t` consist of uppercase and lowercase English letters.

## Follow-up

Could you find an algorithm that runs in `O(m + n)` time?

## Solutions

### Brute Force

```python
class Solution:
    def minWindow(self, s: str, t: str) -> str:
        """
        Brute force approach - check all possible substrings
        """
        if not s or not t or len(s) < len(t):
            return ""

        def is_valid_window(window_str, target):
            """Check if window contains all characters from target"""
            t_count = {}
            for char in target:
                t_count[char] = t_count.get(char, 0) + 1

            for char in window_str:
                if char in t_count:
                    t_count[char] -= 1
                    if t_count[char] == 0:
                        del t_count[char]

            return len(t_count) == 0

        min_window = ""
        min_len = float('inf')

        # Check all possible substrings
        for i in range(len(s)):
            for j in range(i + len(t), len(s) + 1):
                window = s[i:j]
                if is_valid_window(window, t):
                    if len(window) < min_len:
                        min_len = len(window)
                        min_window = window
                    break  # Found valid window starting at i, no need to extend

        return min_window
```

#### Approach

This **brute force solution** checks all possible substrings of s that could contain all characters from t. While correct, it's highly inefficient and included only for educational comparison.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(|s|² × |t|)`

For each starting position (O(|s|)), we check substrings of increasing length (O(|s|)) and validate each (O(|t|)).

##### Space Complexity: `O(|t|)`

Space for character counting in validation function.

#### Key Insights

- Enumerating every substring is the most direct reading of the problem and needs no auxiliary insight, which makes it a useful baseline.
- The early `break` after the first valid window from a given start prunes longer windows that share that start, but the quadratic substring count still dominates.
- It is correct for all inputs yet impractical once `|s|` grows, so it serves comparison and intuition rather than production use.

### Sliding Window with Hash Maps

```python
class Solution:
    def minWindow(self, s: str, t: str) -> str:
        """
        Two-pointer sliding window approach with frequency tracking
        """
        if not s or not t or len(s) < len(t):
            return ""

        # Count characters in t
        t_count = {}
        for char in t:
            t_count[char] = t_count.get(char, 0) + 1

        required = len(t_count)  # Number of unique characters in t
        formed = 0  # Number of unique characters matched with desired frequency

        # Sliding window
        left = right = 0
        window_counts = {}

        # Result: (window length, left, right)
        min_len = float('inf')
        min_left = 0

        while right < len(s):
            # Expand window by including character at right
            char = s[right]
            window_counts[char] = window_counts.get(char, 0) + 1

            # Check if frequency of current character matches desired count in t
            if char in t_count and window_counts[char] == t_count[char]:
                formed += 1

            # Contract window until it ceases to be 'desirable'
            while left <= right and formed == required:
                char = s[left]

                # Update minimum window if current is smaller
                if right - left + 1 < min_len:
                    min_len = right - left + 1
                    min_left = left

                # Remove character at left from window
                window_counts[char] -= 1
                if char in t_count and window_counts[char] < t_count[char]:
                    formed -= 1

                left += 1

            right += 1

        return "" if min_len == float('inf') else s[min_left:min_left + min_len]
```

#### Approach

This solution uses the **sliding window technique** with two pointers. We expand the window by moving the right pointer and contract it by moving the left pointer when we have a valid window. The key insight is tracking when we have all required characters with correct frequencies, then trying to minimize the window size.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(|s| + |t|)`

Each character in s is visited at most twice (once by right pointer, once by left pointer). Building t_count takes O(|t|) time.

##### Space Complexity: `O(|s| + |t|)`

In the worst case, window_counts could contain all characters from s, and t_count contains all characters from t.

#### Key Insights

- Tracking `formed` versus `required` (unique characters matched at their exact frequency) reduces the validity check to `O(1)` instead of rescanning counts each step.
- The window only contracts while it remains valid, so the moment `formed` drops below `required` the left pointer stops, capturing the smallest window precisely.
- Counting frequencies rather than mere presence is what makes duplicate characters in `t` handled correctly.

### Optimized Sliding Window

```python
class Solution:
    def minWindow(self, s: str, t: str) -> str:
        """
        Optimized sliding window that only considers relevant characters
        """
        if not s or not t:
            return ""

        # Count characters in t
        dict_t = {}
        for char in t:
            dict_t[char] = dict_t.get(char, 0) + 1

        required = len(dict_t)

        # Filter s to only include characters present in t
        # This optimization helps when |s| >> |t|
        filtered_s = []
        for i, char in enumerate(s):
            if char in dict_t:
                filtered_s.append((i, char))

        left = right = 0
        formed = 0
        window_counts = {}

        min_len = float('inf')
        min_left = 0

        while right < len(filtered_s):
            # Expand window
            char = filtered_s[right][1]
            window_counts[char] = window_counts.get(char, 0) + 1

            if window_counts[char] == dict_t[char]:
                formed += 1

            # Contract window
            while left <= right and formed == required:
                char = filtered_s[left][1]

                # Calculate actual window size in original string
                start = filtered_s[left][0]
                end = filtered_s[right][0]

                if end - start + 1 < min_len:
                    min_len = end - start + 1
                    min_left = start

                window_counts[char] -= 1
                if window_counts[char] < dict_t[char]:
                    formed -= 1

                left += 1

            right += 1

        return "" if min_len == float('inf') else s[min_left:min_left + min_len]
```

#### Approach

This is an **optimized version** that pre-filters the string s to only include characters that exist in t. This optimization is particularly beneficial when the length of s is much larger than t and t has few unique characters.

#### Time and Space Complexity Analysis

##### Time Complexity: `O(|s| + |t|)`

Same asymptotic complexity, but with better practical performance when |s| >> |t|.

##### Space Complexity: `O(|s| + |t|)`

Additional space for filtered_s in worst case, but typically much smaller.

#### Key Insights

- Pre-filtering skips characters irrelevant to `t`, so iterations are spent only on positions that can change the window's validity.
- The original indices are carried alongside each filtered character so the true window length in `s` is measured even though we iterate over the compressed list.
- The asymptotic bound is unchanged; the gain is purely in constant factors and only materializes when `|s| >> |t|` and `t` has few unique characters.

## Comparison of Solutions

### Time Complexity

- **Brute Force**: `O(|s|² × |t|)` - Quadratic time, unacceptable for large inputs
- **Sliding Window with Hash Maps**: `O(|s| + |t|)` - Optimal linear time
- **Optimized Sliding Window**: `O(|s| + |t|)` - Same complexity, better constants

### Space Complexity

- **Brute Force**: `O(|t|)` - Only target character counting
- **Sliding Window with Hash Maps**: `O(|s| + |t|)` - Hash maps for character counting
- **Optimized Sliding Window**: `O(|s| + |t|)` - Additional filtered array

### Trade-offs

- **Brute Force**: Implementation complexity is low and space usage is minimal, with excellent code clarity. However, performance is poor, making it practically applicable for learning only.
- **Sliding Window with Hash Maps**: Implementation complexity is medium with reasonable space usage and good code clarity. Performance is excellent, making it the best general solution for practical use.
- **Optimized Sliding Window**: Implementation complexity is high with higher space usage and medium code clarity. Performance is better than the standard sliding window for sparse t, making it the best choice for those specific cases.

### When to Use Each

- **Brute Force**: Only for understanding the problem or when constraints are very small
- **Sliding Window with Hash Maps**: Best general-purpose solution for production code and interviews
- **Optimized Sliding Window**: When t has very few unique characters compared to s

### Optimization Notes

- The **Sliding Window with Hash Maps** solution is the recommended choice: it achieves the follow-up's requested `O(m + n)` time complexity using the classic expand/contract pattern with two pointers, balancing simplicity and efficiency for production code and interviews.
- Key implementation detail: track `formed` versus `required` (the count of unique characters matched at their desired frequency) so the window only contracts while it remains valid, allowing the minimum to be captured precisely.
- The **Optimized Sliding Window** pre-filters s to only relevant characters, which delivers real benefits only when `|s| >> |t|` and t has few unique characters. Otherwise the extra filtered array adds overhead without asymptotic improvement.
- Common pitfall: mishandling edge cases such as empty strings, impossible cases where t is longer than s, and duplicate characters in t. Frequency counts (not mere presence) must be tracked to handle duplicates correctly.

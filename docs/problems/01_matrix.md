# [01 Matrix](https://leetcode.com/problems/01-matrix/)

**Medium** | **25 minutes** | **Array, Dynamic Programming, BFS, Matrix**

**Practice:** [`practice/01_matrix/solution.py`](https://github.com/ThoDHa/grind75/blob/main/practice/01_matrix/solution.py)

Given an `m x n` binary matrix `mat`, return the distance of the nearest `0` for each cell.

The distance between two adjacent cells is `1`.

## Examples

### Example 1

![01 Matrix Example1](assets/01_matrix_example1.jpg)

**Input:** `mat = [[0,0,0],[0,1,0],[0,0,0]]`

**Output:** `[[0,0,0],[0,1,0],[0,0,0]]`

**Explanation:** All zeros are at distance 0 from themselves, and the 1 in the middle is 1 away from the closest 0.

### Example 2

![01 Matrix Example1](assets/01_matrix_example2.jpg)

**Input:** `mat = [[0,0,0],[0,1,0],[1,1,1]]`

**Output:** `[[0,0,0],[0,1,0],[1,2,1]]`

**Explanation:** The cells at (2,0) and (2,2) are at distance 1 from the closest 0, and the cell at (2,1) is at distance 2.

## Constraints

- `m == mat.length`
- `n == mat[i].length`
- `1 <= m, n <= 10^4`
- `1 <= m * n <= 10^4`
- `mat[i][j]` is either `0` or `1`
- There is at least one `0` in `mat`

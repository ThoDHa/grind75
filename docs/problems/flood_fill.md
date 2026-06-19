# [Flood Fill](https://leetcode.com/problems/flood-fill/)

**Easy** | **20 minutes** | **Array, DFS, BFS, Matrix**

**Pattern:** [Graph Traversal](../patterns/graph/intuition.md)

**Practice:** [`practice/flood_fill/solution.py`](../../practice/flood_fill/solution.py)

You are given an image represented by an m x n grid of integers `image`, where `image[i][j]` represents the pixel value of the image. You are also given three integers `sr`, `sc`, and `color`. Your task is to perform a flood fill on the image starting from the pixel `image[sr][sc]`.

To perform a flood fill:

- Begin with the starting pixel and change its color to `color`.
- Perform the same process for each pixel that is directly adjacent (pixels that share a side with the original pixel, either horizontally or vertically) and shares the same color as the starting pixel.
- Keep repeating this process by checking neighboring pixels of the updated pixels and modifying their color if it matches the original color of the starting pixel.
- The process stops when there are no more adjacent pixels of the original color to update.

Return the modified image after performing the flood fill.

## Examples

### Example 1

![Flood Fill Example](assets/flood_fill_example1.jpg)

**Input:** `image = [[1,1,1],[1,1,0],[1,0,1]]`, `sr = 1`, `sc = 1`, `color = 2`

**Output:** `[[2,2,2],[2,2,0],[2,0,1]]`

**Explanation:** From the center of the image with position `(sr, sc) = (1, 1)` (i.e., the red pixel), all pixels connected by a path of the same color as the starting pixel (i.e., the blue pixels) are colored with the new color. Note the bottom corner is not colored `2`, because it is not horizontally or vertically connected to the starting pixel.

### Example 2

**Input:** `image = [[0,0,0],[0,0,0]]`, `sr = 0`, `sc = 0`, `color = 0`

**Output:** `[[0,0,0],[0,0,0]]`

**Explanation:** The starting pixel is already colored with `0`, which is the same as the target color. Therefore, no changes are made to the image.

## Constraints

- `m == image.length`
- `n == image[i].length`
- `1 <= m, n <= 50`
- `0 <= image[i][j], color < 216`
- `0 <= sr < m`
- `0 <= sc < n`

## Solutions

### Recursive DFS

```python
class Solution:
    def floodFill(self, image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:
        initial_color = image[sr][sc]
        # If the starting color is already the target color, return the image as is
        if initial_color == color:
            return image
        self.fill(image, sr, sc, initial_color, color)
        return image

    def fill(self, image: List[List[int]], sr: int, sc: int, initial_color: int, color: int):
        # Check if coordinates are out of bounds or pixel is not the initial color
        if sr < 0 or sr >= len(image) or sc < 0 or sc >= len(image[0]) or image[sr][sc] != initial_color:
            return

        # Change the color of the current pixel
        image[sr][sc] = color

        # Recursively fill the adjacent pixels
        self.fill(image, sr-1, sc, initial_color, color)  # Up
        self.fill(image, sr+1, sc, initial_color, color)  # Down
        self.fill(image, sr, sc-1, initial_color, color)  # Left
        self.fill(image, sr, sc+1, initial_color, color)  # Right
```

#### Approach

This solution uses a recursive depth-first search (DFS) approach to implement the flood fill algorithm:

- We first check if the starting pixel already has the target color to avoid unnecessary work
- For each pixel, we check if it's valid (within bounds and has the initial color)
- If valid, we change its color and recursively apply the algorithm to its four adjacent neighbors
- The recursion naturally stops when there are no more pixels matching the initial color

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

- In the worst case, we might need to visit all pixels in the image
- Each pixel is visited at most once, where `n` is the total number of pixels (`m × n` for an `m×n` image)

##### Space Complexity: `O(n)`

- The recursion stack can go as deep as the number of pixels in the worst case
- This occurs in scenarios where the image consists of a snake-like path of connected pixels

#### Key Insights

- The early check for `initial_color == color` is an important optimization that prevents unnecessary processing
- Using recursion provides an elegant solution for traversing connected components
- The algorithm only modifies pixels that match the initial color, precisely implementing the flood fill behavior

### Iterative DFS

```python
class Solution:
    def floodFill(self, image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:
        initial_color = image[sr][sc]
        if initial_color == color:
            return image

        stack = [(sr, sc)]
        rows, cols = len(image), len(image[0])

        while stack:
            r, c = stack.pop()  # Pop from the end - stack behavior

            if 0 <= r < rows and 0 <= c < cols and image[r][c] == initial_color:
                image[r][c] = color

                # Push all 4 neighbors onto the stack
                stack.append((r+1, c))  # Down
                stack.append((r-1, c))  # Up
                stack.append((r, c+1))  # Right
                stack.append((r, c-1))  # Left

        return image
```

#### Approach

This solution implements flood fill using an iterative depth-first search approach with a stack:

- We use a stack to keep track of pixels we need to process
- For each pixel, we check if it's valid and has the initial color
- If valid, we change its color and add all four adjacent pixels to the stack
- The stack naturally handles the DFS traversal pattern without recursion

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

- Each pixel is examined at most once
- All stack operations (`append` and `pop`) are `O(1)`

##### Space Complexity: `O(n)`

- In the worst case, we might need to store many pixels in the stack
- The maximum stack size depends on the image structure, but is bounded by the number of pixels

#### Key Insights

- Eliminates the risk of stack overflow errors that could occur with recursive approaches
- Maintains the same traversal pattern as recursive DFS
- The order of neighbor addition affects the traversal path

### Recursive BFS

```python
class Solution:
    def floodFill(self, image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:
        initial_color = image[sr][sc]
        if initial_color == color:
            return image

        # Initial level contains just the starting pixel
        self.bfs_level(image, [(sr, sc)], initial_color, color)
        return image

    def bfs_level(self, image: List[List[int]], level: List[tuple], initial_color: int, color: int):
        if not level:  # Base case: no more pixels to process
            return

        next_level = []  # Will contain pixels for the next recursive call
        rows, cols = len(image), len(image[0])

        for r, c in level:
            if 0 <= r < rows and 0 <= c < cols and image[r][c] == initial_color:
                image[r][c] = color

                # Add all 4 neighbors to the next level
                next_level.append((r+1, c))  # Down
                next_level.append((r-1, c))  # Up
                next_level.append((r, c+1))  # Right
                next_level.append((r, c-1))  # Left

        # Process the next level recursively
        self.bfs_level(image, next_level, initial_color, color)
```

#### Approach

This solution implements a breadth-first search using recursive level-by-level processing:

- Instead of processing one pixel at a time, we process entire "levels" of pixels
- Each recursive call handles all pixels at the same distance from the starting point
- We build up the next level as we process the current one
- This ensures we visit pixels in order of increasing distance from the start

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n)`

- Each pixel is processed exactly once
- Building the next level list is an `O(1)` operation per pixel

##### Space Complexity: `O(n)`

- The recursion stack depth is at most the diameter of the connected component
- The level lists can collectively contain at most `n` pixels

#### Key Insights

- Provides a level-order traversal pattern while still using recursion
- Generally has shallower recursion depth than DFS, reducing stack overflow risk
- Each recursive call processes a "wave" of pixels at equal distance from the start

### Iterative BFS

```python
class Solution:
    def floodFill(self, image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:
        initial_color = image[sr][sc]
        if initial_color == color:
            return image

        rows, cols = len(image), len(image[0])
        queue = [(sr, sc)]

        while queue:
            r, c = queue.pop(0)  # Pop from the beginning - queue behavior

            if 0 <= r < rows and 0 <= c < cols and image[r][c] == initial_color:
                image[r][c] = color

                # Add all 4 neighbors to the queue
                queue.append((r+1, c))  # Down
                queue.append((r-1, c))  # Up
                queue.append((r, c+1))  # Right
                queue.append((r, c-1))  # Left

        return image
```

#### Approach

This solution implements a standard iterative breadth-first search using a queue:

- We use a list as a queue to process pixels in order of their distance from the start
- For each pixel, we check if it's valid and has the initial color
- If valid, we change its color and add all four adjacent pixels to the queue
- This ensures we process pixels in concentric "waves" from the starting point

#### Time and Space Complexity Analysis

##### Time Complexity: `O(n²)`

- Each pixel is examined at most once: `O(n)`
- However, using `list.pop(0)` is an `O(n)` operation
- This results in an overall `O(n²)` time complexity

##### Space Complexity: `O(n)`

- In the worst case, the queue might contain many pixels
- The maximum queue size depends on the image structure but is bounded by the number of pixels

#### Key Insights

- Processes pixels in order of their distance from the starting point
- Without a proper queue implementation, the time complexity suffers
- Using a list as a queue is inefficient due to the `O(n)` cost of `pop(0)`

## Comparison of Solutions

### Time Complexity

- **Recursive DFS**: `O(n)` - each of the `n` pixels is visited at most once.
- **Iterative DFS**: `O(n)` - each pixel is pushed and popped a constant number of times with `O(1)` stack operations.
- **Recursive BFS**: `O(n)` - each pixel is processed once across the level lists.
- **Iterative BFS**: `O(n²)` - each pixel is visited once, but `list.pop(0)` costs `O(n)` per dequeue.

### Space Complexity

- **Recursive DFS**: `O(n)` - recursion stack can reach the size of the connected component.
- **Iterative DFS**: `O(n)` - explicit stack bounded by the number of pixels.
- **Recursive BFS**: `O(n)` - recursion depth plus level lists holding up to all pixels.
- **Iterative BFS**: `O(n)` - queue bounded by the number of pixels.

### Trade-offs

- Recursive DFS gains the most concise, readable code but gives up control over stack depth, risking overflow on large images.
- Iterative DFS gives up brevity to gain an explicit stack that sidesteps recursion limits.
- Recursive BFS gains a level-order traversal while keeping recursion, trading a slightly unusual structure for shallower recursion depth than DFS.
- Iterative BFS gains the classic queue-based BFS shape but gives up performance, degrading to `O(n²)` because a list is used as a queue.

### When to Use Each

- **Recursive DFS**: When simplicity and readability matter and the grid is small enough that stack depth is not a concern.
- **Iterative DFS**: When DFS traversal is desired but recursion limits must be avoided.
- **Recursive BFS**: When level-order processing is wanted while keeping recursive logic.
- **Iterative BFS**: When strict distance-ordered processing is needed, ideally with a real queue implementation.

### Optimization Notes

- For flood fill the recursive DFS is the common practical choice for its simplicity; iterative DFS is the safer pick when input size could exhaust the call stack.
- The `initial_color == color` early return is essential in every variant; without it the BFS and DFS would loop forever since recolored pixels would still match the target.
- The Iterative BFS approach's `O(n²)` cost comes entirely from `list.pop(0)`; swapping the list for `collections.deque` restores true `O(n)` BFS.
- Given the small constraints (`m, n <= 50`), all four run fast enough, but the Iterative BFS approach's list-as-queue pattern is the pitfall to avoid in larger graph problems.

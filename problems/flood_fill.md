# [Flood Fill](https://leetcode.com/problems/flood-fill/)

Easy - 20 minutes - Array, DFS, BFS, Matrix

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

### Solution 1: Recursive DFS

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

### Solution 2: Iterative DFS

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

### Solution 3: Recursive BFS

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

### Solution 4: Iterative BFS

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

### Comparison of Solutions

#### Time Complexity

- **Solution 1 (Recursive DFS)**: `O(n)`
- **Solution 2 (Iterative DFS)**: `O(n)`
- **Solution 3 (Recursive BFS)**: `O(n)`
- **Solution 4 (Iterative BFS)**: `O(n²)` due to inefficient queue operations

#### Space Complexity

- **Solution 1 (Recursive DFS)**: `O(n)` for the recursion stack
- **Solution 2 (Iterative DFS)**: `O(n)` for the stack
- **Solution 3 (Recursive BFS)**: `O(n)` for the recursion stack and level lists
- **Solution 4 (Iterative BFS)**: `O(n)` for the queue

#### Trade-offs

- **Recursive DFS**: Simple and elegant but risks stack overflow for large images
- **Iterative DFS**: Avoids stack overflow but slightly more verbose code
- **Recursive BFS**: Unique approach combining recursion with level-based processing
- **Iterative BFS**: Classic level-order traversal but inefficient without proper queue

#### When to Use Each

- **Recursive DFS** is best for simplicity and readability when stack size isn't a concern
- **Iterative DFS** is preferred when you need DFS traversal but want to avoid recursion limits
- **Recursive BFS** might be useful when you need level-order processing with recursive logic
- **Iterative BFS** is ideal when you need to process pixels strictly by distance from origin (with proper queue implementation)

In practical implementations, the recursive DFS approach is often preferred for flood fill due to its simplicity and efficiency, while iterative BFS with a proper queue implementation would be chosen when level-order traversal is important.

import heapq
import os
import time

def parse_map(map_string):
    """Parse the maze map into a grid and find the start and end positions."""
    grid = [list(row) for row in map_string.strip().split("\n")]
    start = end = None
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 'S':
                start = (x, y)
            elif cell == 'E':
                end = (x, y)
    return grid, start, end

def is_valid(grid, x, y):
    """Check if a position is within bounds and not a wall."""
    return 0 <= y < len(grid) and 0 <= x < len(grid[0]) and grid[y][x] != '#'

def print_grid(grid, x, y):
    """Print the grid with the current position of the reindeer."""
    temp_grid = [row.copy() for row in grid]
    temp_grid[y][x] = 'R'  # Mark the current position of the reindeer
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n".join("".join(row) for row in temp_grid))
    print("\n" + "=" * 20)

def a_star_all_paths(grid, start, end):
    """Find all tiles that are part of any best path using A* search."""
    directions = {
        'N': (0, -1), 'E': (1, 0), 'S': (0, 1), 'W': (-1, 0)
    }
    rotations = {'N': ['E', 'W'], 'E': ['S', 'N'], 'S': ['W', 'E'], 'W': ['N', 'S']}

    def heuristic(x, y):
        """Heuristic: Manhattan distance to the end."""
        return abs(x - end[0]) + abs(y - end[1])

    # Priority queue: (total_cost, x, y, direction, path)
    queue = [(0, start[0], start[1], 'E', [])]
    visited = {}
    best_cost = float('inf')
    best_paths = []

    while queue:
        cost, x, y, direction, path = heapq.heappop(queue)

        # Skip if cost exceeds the best cost
        if cost > best_cost:
            continue

        # If we reach the end, save the path
        if (x, y) == end:
            if cost < best_cost:
                best_cost = cost
                best_paths = [path + [(x, y)]]
            elif cost == best_cost:
                best_paths.append(path + [(x, y)])
            continue

        # Skip if this state has been visited with a lower or equal cost
        if (x, y, direction) in visited and visited[(x, y, direction)] <= cost:
            continue
        visited[(x, y, direction)] = cost

        # Move forward
        dx, dy = directions[direction]
        nx, ny = x + dx, y + dy
        if is_valid(grid, nx, ny):
            heapq.heappush(queue, (cost + 1, nx, ny, direction, path + [(x, y)]))

        # Rotate
        for new_direction in rotations[direction]:
            heapq.heappush(queue, (cost + 1000, x, y, new_direction, path + [(x, y)]))

    # Mark all tiles in any best path
    tiles_in_best_paths = set()
    for path in best_paths:
        tiles_in_best_paths.update(path)

    return tiles_in_best_paths


# Example usage
maze = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""

grid, start, end = parse_map(maze)
tiles_in_best_paths = a_star_all_paths(grid, start, end)

# Mark the tiles in the grid
for y, row in enumerate(grid):
    for x, _ in enumerate(row):
        if (x, y) in tiles_in_best_paths and grid[y][x] not in {'S', 'E'}:
            grid[y][x] = 'O'

# Print the updated grid
print("\n".join("".join(row) for row in grid))
print("Number of tiles in best paths:", len(tiles_in_best_paths))

import argparse
from collections import deque
from time import perf_counter
def parse_map(input_map):
    return [list(map(int, line)) for line in input_map.strip().split("\n")]

def find_trailheads(topographic_map):
    trailheads = []
    for r, row in enumerate(topographic_map):
        for c, value in enumerate(row):
            if value == 0:
                trailheads.append((r, c))
    return trailheads

def bfs(topographic_map, start):
    rows, cols = len(topographic_map), len(topographic_map[0])
    visited = set()
    queue = deque([start])
    visited.add(start)
    reachable_nines = set()

    while queue:
        r, c = queue.popleft()
        current_height = topographic_map[r][c]

        # Check neighbors
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                neighbor_height = topographic_map[nr][nc]
                if neighbor_height == current_height + 1:
                    visited.add((nr, nc))
                    queue.append((nr, nc))
                    if neighbor_height == 9:
                        reachable_nines.add((nr, nc))

    return len(reachable_nines)

def calculate_scores(input_map):
    topographic_map = parse_map(input_map)
    trailheads = find_trailheads(topographic_map)
    total_score = 0

    for trailhead in trailheads:
        total_score += bfs(topographic_map, trailhead)

    return total_score

def main():
    #inicializar el contador
    start = perf_counter()

    parser = argparse.ArgumentParser(description="Calculate scores from a topographic map.")
    parser.add_argument("file", help="Path to the input map file")
    args = parser.parse_args()

    try:
        with open(args.file, 'r') as f:
            input_map = f.read()
        print("Total score:", calculate_scores(input_map))
        print(f"Tiempo: {(perf_counter() - start) * 1000:.2f} ms")
    except FileNotFoundError:
        print(f"Error: File '{args.file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

import heapq
import os
import time
import sys
import argparse
def leer_archivo(file_path):
    """
    Analiza el mapa del almacén y devuelve la cuadrícula, 
    la posición del inicio y las posicion final
    """
    grid = []
    start= None
    end = None
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        for y, line in enumerate(lines):
            row = []
            for x, char in enumerate(line.strip()):
                if char == 'S':
                    start = (x, y)
                    row.append(".")
                elif char == 'E':
                    end = (x, y)
                    row.append(".")
                elif char in '#.':
                    row.append(char)
                else:
                    print(f"caracter no esperado => {char}")
                
            grid.append(row)

        return grid, start,end
    except FileExistsError:
        print(f"Error al leer el archivo'{file_path}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error al cargar el archivo: '{e}'")
        sys.exit(1)

def parse_map(map_string):
    #Analice el mapa del laberinto en una cuadrícula y encuentre las posiciones de inicio y final.
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
    #Comprueba si una posición está dentro de los límites y no en una pared.
    return 0 <= y < len(grid) and 0 <= x < len(grid[0]) and grid[y][x] != '#'

def print_grid(grid, x, y):
    #Imprima la cuadrícula con la posición actual del reno.
    temp_grid = [row.copy() for row in grid]
    temp_grid[y][x] = 'R'  # Marcar la posición actual del reno
   
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
    visited = set()
    best_paths = []
    best_cost = float('inf')

    while queue:
        cost, x, y, direction, path = heapq.heappop(queue)

        # Si superamos el mejor costo, saltamos
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

        # Skip if this state has been visited
        if (x, y, direction) in visited:
            continue
        visited.add((x, y, direction))

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
#maze = """###############
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

def main():
    # Configura el analizador de argumentos
    parser = argparse.ArgumentParser(
        description="Advent of Code dia 16 desfio 2, procesa la informacion del archivo del desafio",
        usage=f"python {sys.argv[0]} <archivo>"
    )
    parser.add_argument(
        'archivo',
        type=str,
        help=f"use: python {sys.argv[0]}  <archivo"
        )
    
    # Analiza los argumentos
    args = parser.parse_args()
    grid, start, end = leer_archivo(args.archivo)
    #grid, start, end = parse_map(maze)
    tiles_in_best_paths = a_star_all_paths(grid, start, end)

    # Mark the tiles in the grid
    for y, row in enumerate(grid):
        for x, _ in enumerate(row):
            if (x, y) in tiles_in_best_paths and grid[y][x] not in {'S', 'E'}:
                grid[y][x] = 'O'

    # imprime la grip actualizada
    print("\n".join("".join(row) for row in grid))
    print("Number of tiles in best paths:", len(tiles_in_best_paths))



    print(f"Tiempo de ejecución: {(time.perf_counter() - Rstart) * 1000:.2f} ms")

if __name__ == "__main__":
    Rstart = time.perf_counter()
    main()
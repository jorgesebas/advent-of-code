import heapq
import sys
import time
import argparse
import os
def print_grid(grid, inicio, fin):
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m' # orange on some systems
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    LIGHT_GRAY = '\033[37m'
    DARK_GRAY = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m' # called to return to standard terminal text color
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if (y, x) == inicio:
                print(YELLOW + 'S' + RESET, end="")  # Muestra el robot en rojo
            elif (y,x) == fin:
                 print(YELLOW + 'E' + RESET, end="")         
            else:
                print(cell, end="")  # Muestra el resto de la celda sin cambios
        print()  # Salto de línea para la siguiente fila
    #print()  # Espacio entre actualizaciones



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
    #Comprueba si una posición está dentro de los límites y no en una pared".
    return 0 <= y < len(grid) and 0 <= x < len(grid[0]) and grid[y][x] != '#'

def a_star(grid, start, end,delay=0.5):
    #Encuentre la puntuación más baja utilizando la búsqueda A*.
    directions = {
        'N': (0, -1), 'E': (1, 0), 'S': (0, 1), 'W': (-1, 0)
    }
    rotations = {'N': ['E', 'W'], 'E': ['S', 'N'], 'S': ['W', 'E'], 'W': ['N', 'S']}

    def heuristic(x, y):
        #Heurística: Distancia de Manhattan hasta el final
        return abs(x - end[0]) + abs(y - end[1])

    # Cola de prioridad: (costo_total, x, y, dirección)
    queue = [(0, start[0], start[1], 'E')]
    visited = set()
    
    while queue:
        #os.system('cls' if os.name == 'nt' else 'clear')
        cost, x, y, direction = heapq.heappop(queue)
        #print_grid(grid, start, end)
        #time.sleep(delay) 
        # Si llegamos al final, devolvemos el coste.
        if (x, y) == end:
            return cost

        # Omitir si este estado ya ha sido visitado
        if (x, y, direction) in visited:
            continue
        visited.add((x, y, direction))

        # Avanzar
        dx, dy = directions[direction]
        nx, ny = x + dx, y + dy
        if is_valid(grid, nx, ny):
            heapq.heappush(queue, (cost + 1, nx, ny, direction))

        # Rotate
        for new_direction in rotations[direction]:
            heapq.heappush(queue, (cost + 1000, x, y, new_direction))

    return float('inf')  # If no path found

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
def imprimir_matrix(matrix):
    for line in matrix:
        print("".join(line))


def main():
    # Configura el analizador de argumentos
    parser = argparse.ArgumentParser(
        description="Advent of Code dia 16 desfio 1, procesa la informacion del archivo del desafio",
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
    imprimir_matrix(grid)
    print(f"S {start}  E{end}")
    lowest_score = a_star(grid, start, end)
    print("Lowest score:", lowest_score)
    print(f"Tiempo de ejecución: {(time.perf_counter() - start) * 1000:.2f} ms")

if __name__ == "__main__":
    start = time.perf_counter()
    main()
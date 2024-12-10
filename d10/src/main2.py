import argparse
from collections import deque
from time import perf_counter

def parse_map(input_map):
    """Convierte el mapa topográfico de texto a una lista de listas de enteros."""
    return [list(map(int, line)) for line in input_map.strip().split("\n")]

def find_trailheads(topographic_map):
    """Encuentra todos los puntos de inicio (altura 0) en el mapa."""
    trailheads = []
    for r, row in enumerate(topographic_map):
        for c, value in enumerate(row):
            if value == 0:
                trailheads.append((r, c))
    return trailheads

def bfs_count_trails(topographic_map, start):
    """Cuenta los senderos distintos que comienzan en el punto de inicio dado."""
    rows, cols = len(topographic_map), len(topographic_map[0])
    queue = deque([(start, [])])  # Agregamos una lista para rastrear el camino actual
    trail_count = 0

    # Realizamos BFS para encontrar todos los senderos posibles
    while queue:
        (r, c), path = queue.popleft()
        current_height = topographic_map[r][c]
        path.append((r, c))

        # Verificar vecinos
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbor_height = topographic_map[nr][nc]
                # Si el vecino tiene altura exactamente 1 más que la actual, es un paso válido
                if neighbor_height == current_height + 1:
                    # Si llegamos a una altura 9, contamos este sendero
                    if neighbor_height == 9:
                        trail_count += 1
                    else:
                        queue.append(((nr, nc), path.copy()))  # Copiamos el camino actual

    print (f"cuenta los sienderos:'{trail_count}'")
    return trail_count

def calculate_trailhead_ratings(input_map):
    """Calcula la suma de las clasificaciones de todos los puntos de inicio."""
    topographic_map = parse_map(input_map)
    trailheads = find_trailheads(topographic_map)
    total_rating = 0

    # Para cada punto de inicio, contamos cuántos senderos distintos pueden empezar
    for trailhead in trailheads:
        total_rating += bfs_count_trails(topographic_map, trailhead)

    return total_rating

def main():
    #inicializar el temporizador
    start = perf_counter()
    parser = argparse.ArgumentParser(description="Calculate the sum of trailhead ratings.")
    parser.add_argument("file", help="Path to the input map file")
    args = parser.parse_args()

    try:
        with open(args.file, 'r') as f:
            input_map = f.read()
        print("Total trailhead rating:", calculate_trailhead_ratings(input_map))
        print(f"Tiempo:{(perf_counter() - start) * 1000:.2f} ms")
    except FileNotFoundError:
        print(f"Error: File '{args.file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

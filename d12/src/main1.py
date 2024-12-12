from collections import deque
import sys
from time import perf_counter
def cargando_archivo(file_path):
    try:
        with open(file_path, 'r') as file:
            # Leer el archivo y convertirlo en una lista de cadenas (una por línea)
            mapa = [line.strip() for line in file if line.strip()]
        return mapa
    except Exception as e:
        print(f"Error al cargar el archivo: '{e}'")
        sys.exit(1)


def parse_map(garden_map):
    rows, cols = len(garden_map), len(garden_map[0])
    visited = [[False] * cols for _ in range(rows)]

    def bfs(start_row, start_col):
        # Definir desplazamientos para moverse en 4 direcciones (N, S, E, O)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        queue = deque([(start_row, start_col)])
        region_type = garden_map[start_row][start_col]
        area = 0
        perimeter = 0

        while queue:
            row, col = queue.popleft()

            if visited[row][col]:
                continue
            visited[row][col] = True
            area += 1

            # Revisar vecinos
            for dr, dc in directions:
                nr, nc = row + dr, col + dc

                if 0 <= nr < rows and 0 <= nc < cols:
                    if garden_map[nr][nc] == region_type and not visited[nr][nc]:
                        queue.append((nr, nc))
                    elif garden_map[nr][nc] != region_type:
                        perimeter += 1
                else:
                    # Si estamos fuera del mapa, cuenta como perímetro
                    perimeter += 1

        return area, perimeter

    # Explorar todo el mapa y calcular áreas/perímetros de las regiones
    total_price = 0
    for row in range(rows):
        for col in range(cols):
            if not visited[row][col]:
                area, perimeter = bfs(row, col)
                ap = area * perimeter
                total_price += ap
                print(f"area x perimetro => {area} x {perimeter} = {ap} ")

    return total_price
def imprimir_mapa(mapa):
    for fila in mapa:
        print(' '.join(fila))  # Imprime los elementos de cada fila separados por un espacio

def main():
    #iniciando el contador
    start = perf_counter()

    # Ejemplo de uso
    #garden_map = [
    #    "AAAA",
    #    "BBCD",
    #    "BBCC",
    #    "EEEC"
    #]
    # Verificando si se ha proporcionado un archivo como argumento
    if len(sys.argv) != 2:
        print(f"use: python {sys.argv[0]} <archivo>")
        sys.exit(1)
    garden_map = cargando_archivo(sys.argv[1])

    print("mapa", garden_map)
    imprimir_mapa(garden_map)
    print("Precio total:", parse_map(garden_map))
    print(f"Tiempo de ejecucion {(perf_counter() - start) * 1000:.2f} ms")


if __name__ == "__main__":
    main()
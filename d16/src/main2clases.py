import os
import time
import sys
import argparse
from collections import deque

def imprimir_matrix(matrix):
    for line in matrix:
        print("".join(line))

def leer_archivo(file_path):
    """
    Analiza el mapa del almacén y devuelve la cuadrícula, 
    la posición del inicio y las posiciones finales.
    """
    grid = []
    start = None
    end = None
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        for y, line in enumerate(lines):
            row = []
            for x, char in enumerate(line.strip()):
                if char == 'S':
                    start = (x, y)
                    row.append(".")  # Cambia el inicio 'S' por un camino '.'
                elif char == 'E':
                    end = (x, y)
                    row.append(".")  # Cambia el final 'E' por un camino '.'
                elif char in '#.':  # Paredes y caminos
                    row.append(char)
                else:
                    print(f"caracter no esperado => {char}")
                
            grid.append(row)

        return grid, start, end
    except FileNotFoundError:
        print(f"Error al leer el archivo '{file_path}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error al cargar el archivo: '{e}'")
        sys.exit(1)

class Laberinto:
    def __init__(self, laberinto, inicio, fin):
        self.laberinto = laberinto  # Matriz que representa el laberinto
        self.inicio = inicio        # Coordenadas de inicio (x, y)
        self.fin = fin              # Coordenadas de fin (x, y)
        self.visitado = set()       # Conjunto para almacenar celdas visitadas
        self.campos = []            # Lista para almacenar todos los caminos válidos

    def es_valido(self, x, y):
        # Verifica si una posición está dentro de los límites y es libre (.)
        return 0 <= x < len(self.laberinto) and 0 <= y < len(self.laberinto[0]) and self.laberinto[x][y] != '#'

    def bfs(self):
        # Implementamos BFS para encontrar todos los caminos más cortos
        queue = deque([[(self.inicio[0], self.inicio[1])]])  # Cola que contiene los caminos
        self.visitado = set([self.inicio])  # Marcamos el punto de inicio como visitado
        shortest_paths = []
        shortest_length = float('inf')

        while queue:
            # Extraemos el siguiente camino de la cola
            path = queue.popleft()
            x, y = path[-1]

            # Si llegamos al fin, verificamos si este camino es más corto
            if (x, y) == self.fin:
                if len(path) < shortest_length:
                    # Encontramos un camino más corto, lo actualizamos
                    shortest_paths = [path]
                    shortest_length = len(path)
                elif len(path) == shortest_length:
                    # Si el camino tiene la misma longitud que los anteriores, lo agregamos
                    shortest_paths.append(path)
                continue  # No seguimos explorando caminos más largos

            # Movimientos posibles (arriba, abajo, izquierda, derecha)
            movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            
            # Intentamos movernos en cada dirección
            for dx, dy in movimientos:
                nx, ny = x + dx, y + dy
                if self.es_valido(nx, ny) and (nx, ny) not in self.visitado:
                    self.visitado.add((nx, ny))
                    queue.append(path + [(nx, ny)])  # Agregamos el nuevo camino a la cola

        return shortest_paths

    def contar_campos_cortos(self, caminos):
        # Crea un conjunto para marcar todos los tiles en los caminos más cortos
        camino_tiles = set()
        for camino in caminos:
            for x, y in camino:
                camino_tiles.add((x, y))
        
        # Devolvemos el número total de tiles únicos en los caminos más cortos
        return len(camino_tiles)

    def marcar_camino(self, caminos):
        # Crea un conjunto para marcar todos los tiles en los caminos más cortos
        camino_tiles = set()
    
        # Agregar todos los tiles de todos los caminos más cortos al conjunto
        for camino in caminos:
            for x, y in camino:
                camino_tiles.add((x, y))

        # Ahora marcamos el laberinto con "O" en las posiciones de los caminos más cortos
        for y in range(len(self.laberinto)):
            for x in range(len(self.laberinto[0])):
                if (x, y) in camino_tiles and self.laberinto[y][x] != '#':
                    self.laberinto[y][x] = 'O'

def main():
    # Configura el analizador de argumentos
    parser = argparse.ArgumentParser(
        description="Desafio de Advent of Code dia 16 parte, encuentra las rutas más cortas entre el inicio y el fin.",
        usage=f"python {sys.argv[0]} <archivo>"
    )
    parser.add_argument(
        'archivo',
        type=str,
        help=f"Uso: python {sys.argv[0]} <archivo>"
    )
    
    # Analiza los argumentos
    args = parser.parse_args()
    laberinto, inicio, fin = leer_archivo(args.archivo)
    imprimir_matrix(laberinto)
    
    # Crear una instancia del laberinto
    mi_laberinto = Laberinto(laberinto, inicio, fin)

    # Encontrar todos los caminos más cortos
    caminos_cortos = mi_laberinto.bfs()

    # Contamos la cantidad de tiles únicos que forman parte de los caminos más cortos
    cantidad_campos = mi_laberinto.contar_campos_cortos(caminos_cortos)
    print(f"Cantidad de tiles que forman parte de los caminos más cortos: {cantidad_campos}")

    # Marcar los caminos más cortos en el laberinto
    mi_laberinto.marcar_camino(caminos_cortos)

    print("Laberinto con los caminos más cortos marcados (con 'O'):")
    imprimir_matrix(mi_laberinto.laberinto)

if __name__ == "__main__":
    Rstart = time.perf_counter()  # Debe ir antes de llamar a main()
    main()

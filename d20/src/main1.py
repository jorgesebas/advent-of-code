from collections import deque
import itertools
import sys
import argparse
import time

def leer_archivo(file_path):
    """
    Analiza archivo para obtner los patrones y el diseño
    """
    grid= []
    start= end = None
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for r, row in enumerate(lines):
                line =[]
                for c, cell in enumerate(row):
                    if cell == 'S':
                        start = (r, c)
                        line.append('.')
                    elif cell == 'E':
                        end = (r, c)
                        line.append('.')
                    elif cell in '#.':
                        line.append(cell)
                    elif cell == '\n':
                        continue
                    else:
                        print(f"caracter no esperado {cell} {c}")
                        #sys.exit(1)
                grid.append(line)
            return grid, start, end

    except FileExistsError:
        print(f"Error al leer el archivo'{file_path}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error al cargar el archivo: '{e}'")
        sys.exit(1)

def parse_map(map_string):
    #Analizar el mapa de entrada en una matriz y encontrar puntos de inicio y fin
    grid = [list(line) for line in map_string.strip().split("\n")]
    start = end = None
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == 'S':
                start = (r, c)
            elif cell == 'E':
                end = (r, c)
    return grid, start, end
def imprimir_matrix_con_trampa(matrix, visitado,trampa):
    for i,(x,y) in enumerate(visitado):
         matrix[x][y] = '\033[34m' + str(i%10) + '\033[0m'  #  Muestra O en azul si está visitado
    for (start, endt, _) in trampa: 
        sx,sy = start
        ex,ey = endt
        matrix[sx][sy] = '\033[31m' + 'S' + '\033[0m'
        matrix[ex][ey] = '\033[31m' + 'E' + '\033[0m'
    for x, row in enumerate(matrix):
        for y, cell in enumerate(row):
            print(cell, end="")  # Muestra el resto de la celda sin cambios
        print()  # Salto de línea para la siguiente fila

def imprimir_matrix_con_movimiento(matrix, visitado):
    for i,(x,y) in enumerate(visitado):
        matrix[x][y] = '\033[34m' + str(i%10) + '\033[0m'  #  Muestra O en azul si está visitado
    for x, row in enumerate(matrix):
        for y, cell in enumerate(row):
            print(cell, end="")  # Muestra el resto de la celda sin cambios
        print()  # Salto de línea para la siguiente fila

def bfs_with_path(grid, start, end):
    #Encuentra la ruta más corta y devuelve la ruta como una lista de coordenadas.
    rows, cols = len(grid), len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    queue = deque([(start, 0, [start])])  # (posicion de inicio , distancia, camino)
    visited = set([start])

    while queue:
        (r, c), dist, path = queue.popleft()
        if (r, c) == end:
            return path  # Return the full path from start to end

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#' and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append(((nr, nc), dist + 1, path + [(nr, nc)]))
    return []  # Return empty if no path is found

def find_cheats(grid, path):
    #Analizar la ruta para encontrar y evaluar posibles trampas.
    cheats = []
    rows, cols = len(grid), len(grid[0])
    n_path = len(path)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    cheat_distance = 2  # Hacer trampa lleva exactamente 2 picosegundos
    for i in range(n_path):
        ventana_evaluacion = path[i+2:n_path] #se obtine todos lo punto del camino a avaluar desde la siguiente la ultima
        n_ventana_evaluacion = len(ventana_evaluacion )
        a,b = path[i] 
        for j in range(n_ventana_evaluacion  ):#
            # Simular un truco entre path[i] y path[j]
            for (Δx,Δy) in directions:                                                                                                                                                                                                  
                dmx = Δx + a
                dmy = Δy + b#calculando la posision de la muralla 
                dpx = Δx * cheat_distance + a#calculando la posicion del camino a saltar
                dpy = Δy * cheat_distance + b
                if (ventana_evaluacion[j]==(dpx,dpy) and grid[dmx][dmy] =='#'):
                    # Calcular distancia ahorrada
                    original_distance = j  
                    saved_time = original_distance #- cheat_distance
                    print(f" S {path[i]} \t E{path[j]} \t T {saved_time} \tj {i} {j}  ")
                    cheats.append((path[i], path[j], saved_time))
    return cheats
def imprimir_matrix(matrix):
    for line in matrix:
        print("".join(line))
# Input map example
#map_string = """
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
#"""
# Parse the map
#grid, start, end = parse_map(map_string)
def main():
    timerstart = time.perf_counter()
    # Configura el analizador de argumentos
    parser = argparse.ArgumentParser(
        description="Advent of Code día 20 parte 1",
        usage=f"python {sys.argv[0]} <archivo>"
    )
    parser.add_argument(
        'archivo',
        type=str,
        help=f"Uso: python {sys.argv[0]} <archivo>"
    )
    
    # Analiza los argumentos
    args = parser.parse_args()

    grid, starti, endf = leer_archivo(args.archivo)
    imprimir_matrix(grid)
    print (f"inicio {starti}\n fin {endf}")


    # Encuentra el camino más corto sin hacer trampa
    camino = bfs_with_path(grid,starti,endf)
    print(f"distancia {len(camino)}\n {camino}")
    imprimir_matrix_con_movimiento(grid, camino)
    #no_cheat_dist = bfs(grid, start, endf)

    # Simula las posibles trampas
    
    if camino:
    # Analyze cheats along the path
        cheats = find_cheats(grid, camino)
        print(cheats)
        # Contar y mostrar los trucos que cumplen criterios específicos
        significant_cheats = [cheat for cheat in cheats if cheat[2] >= 100]
        #max_tr = max(elemento[2] for elemento in vector)
        conteo = {}
        for elemento in cheats:
            valor = elemento[2]  # Extraer el tercer elemento de la tupla
            if valor in conteo:
                conteo[valor] += 1
            else:
                conteo[valor] = 1
        print(conteo)
        for valor, cantidad in conteo.items():
            print(f"Hay {cantidad} trucos que ahorran {valor} picosegundos")
        imprimir_matrix_con_trampa(grid,camino,cheats)
            
        print("Number of cheats saving at least 100 picoseconds:", len(significant_cheats))
        print("Details of significant cheats:", significant_cheats)
    else:
        print("No valid path found from start to end.")

if __name__ == "__main__":
    main()

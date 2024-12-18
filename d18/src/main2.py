import sys
import argparse
import time
from collections import deque
import os
def imprimir_matrix_con_movimiento(matrix, visitado):
    
    
    for x, row in enumerate(matrix):
        for y, cell in enumerate(row):
            if(x,y)in visitado :  # Acceso correcto a visitados
                print('\033[34m' + 'O' + '\033[0m', end="")  # Muestra O en azul si está visitado
            else:
                print(cell, end="")  # Muestra el resto de la celda sin cambios
        print()  # Salto de línea para la siguiente fila

def encontrar_camino_mas_corto(laberinto, inicio, fin):
    """
    Encuentra la ruta más corta en un laberinto usando BFS.
    
    Args:
        laberinto: Lista de listas que representa el mapa ('.' y '#').
        inicio: Tupla con la posición inicial (x, y).
        fin: Tupla con la posición final (x, y).
        
    Returns:
        El número mínimo de pasos para llegar al final, o -1 si es imposible.
    """
    max_y = len(laberinto)
    max_x = len(laberinto[0])

    # Movimientos posibles (arriba, abajo, izquierda, derecha)
    movimientos = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Cola para BFS: cada elemento es (posición_actual, pasos_actuales, ruta_actual)
    cola = deque([(inicio, 0, [inicio])])

    # Matriz para marcar visitados
    visitados = [[False for _ in range(max_x)] for _ in range(max_y)]
    visitados[inicio[1]][inicio[0]] = True  # Marcar el inicio como visitado

    while cola:
        (x, y), pasos, ruta = cola.popleft()

        # Si llegamos al final, devolvemos la distancia y el camino
        if (x, y) == fin:
            return pasos, ruta

        # Explorar movimientos válidos
        for dx, dy in movimientos:
            nx, ny = x + dx, y + dy

            # Verificar si el movimiento es válido
            if 0 <= nx < max_x and 0 <= ny < max_y and not visitados[ny][nx] and laberinto[ny][nx] == '.':
                visitados[ny][nx] = True
                # Añadir la nueva posición y el camino actualizado
                cola.append(((nx, ny), pasos + 1, ruta + [(nx, ny)]))

    # Si agotamos la cola sin encontrar el final, no hay camino
    return -1, []

def imprimir_matrix(matrix):
    for line in matrix:
        print("".join(line))

def leer_archivo(file_path):
    """
    Lee un archivo con registros y un programa.
    """
    max_x = max_y = 0  # Determinar el tamaño de la memoria o matriz
    registros = []
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if ',' in line:
                    valuex, valuey = line.split(',', 1)
                    valuex = valuex.strip()  # Limpiar espacios
                    valuey = valuey.strip()  # Limpiar espacios

                    # Asignar valores según el registro
                    x = int(valuex)
                    if x > max_x:
                        max_x = x
                    y = int(valuey)
                    if y > max_y:
                        max_y = y
                    registros.append((x, y))
                else:
                    print(f"Caracter no esperado: {line}")

        return registros, max_x, max_y
    except FileNotFoundError:
        print(f"Error al leer el archivo '{file_path}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error al cargar el archivo: '{e}'")
        sys.exit(1)

def generar_mapa(registro, max_x, max_y):
    grip = []
    for y in range(max_y + 1):
        line = []
        for x in range(max_x + 1):
            if (x, y) in registro:
                line.append('#')
            else:
                line.append('.')
        grip.append(line)
    return grip

def main():
    start_timer = time.perf_counter()  # Inicializa el contador
    # Configura el analizador de argumentos
    parser = argparse.ArgumentParser(
        description="Desafío de Advent of Code día 18 parte 1",
        usage=f"python {sys.argv[0]} <archivo>"
    )
    parser.add_argument(
        'archivo',
        type=str,
        help=f"Uso: python {sys.argv[0]} <archivo>"
    )
    
    # Analiza los argumentos
    args = parser.parse_args()

    registro, max_x, max_y = leer_archivo(args.archivo)
    inicio = (0, 0)
    fin = (max_x, max_y)
    
    #print(registro)
    print(f"Inicia en {inicio}")
    print(f"Fin en {fin}")
   
  
    registro_contador = 0  # Solo usamos los primeros 12 bytes en el ejemplo
  
    registro_maximo = len(registro)
    grid = generar_mapa([],max_x,max_y)
    imprimir_matrix(grid)
    input()
    
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpia la consola para la animacion
        a,b = registro[registro_contador]
        grid[a][b] = '#'  
        
        #imprimir_matrix(grid)
        resultado, visitado = encontrar_camino_mas_corto(grid, inicio, fin)
        imprimir_matrix_con_movimiento(grid, visitado)
        if resultado == -1 or registro_contador == registro_maximo:
            print(f"\rNo es posible llegar al destino.{resultado},  {registro_contador+1}")
            break
        else:
            
            print(f"\rEl camino más corto tiene {resultado} pasos. el registro {registro_contador+1} => {registro[registro_contador]}")
        if registro_maximo < 26:
            print("precione entrer")
            input()
            
        else:
            time.sleep(0.1)
        registro_contador += 1
    
    
        
    print(f"Las coordenadas del primer byte que evitarán que la salida sea accesible desde su posición  es {registro[registro_contador]} el registro {registro_contador+1} ")    
    print(f"Tiempo de ejecución: {(time.perf_counter() - start_timer) * 1000:.2f} ms")

if __name__ == "__main__":
    main()

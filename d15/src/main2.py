import time
import argparse
import sys
import os

def imprimir_matrix(matrix):
    for line in matrix:
        print("".join(line))
def imprimir_matrix_con_movimiento(matrix, robot_pos,boxes, movimiento_actual=None):
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
    for y, row in enumerate(matrix):
        for x, cell in enumerate(row):
            if (y, x) == robot_pos:
                print(YELLOW + '@' + RESET, end="")  # Muestra el robot en rojo
            elif any((y, x) == right for _, right in boxes):
                if(y,x)== movimiento_actual:
                    print(GREEN + '[]' + RESET,end="")  #muestra las cajas 
                else:
                    print(BRIGHT_CYAN + '[]' + RESET,end="")  #muestra las cajas           
            elif (y,x) == movimiento_actual and cell == "#":
                print(RED + cell + RESET, end="")  # Muestra el movimiento actual en verde
            elif (y,x) == movimiento_actual and cell== '.':
                print(GREEN+cell+RESET,end="") #Muestra el moviemiento en el espacio vacio
            elif (y,x) != movimiento_actual:
                print(cell, end="")  # Muestra el resto de la celda sin cambios
        print()  # Salto de línea para la siguiente fila
    #print()  # Espacio entre actualizaciones


def imprimir_posiciones(moves, t, ventana=30):
    RED = '\033[31m'
    RESET = '\033[0m'
    total = len(moves)  # Total de movimientos

    # Calcula el porcentaje de progreso
    porcentaje = (t + 1) / total  # +1 porque los índices comienzan en 0
    ancho_barra = 20  # Ancho visual de la barra
    progreso = int(porcentaje * ancho_barra)
    
    # Genera la barra de progreso
    barra = ("#" * progreso).ljust(ancho_barra, '-')
    print(f'\r[{barra}] {t + 1}/{total} movimientos', end='', flush=True)

    # Calcula el rango de la ventana
    inicio = max(0, t - ventana)
    fin = min(len(moves), t + ventana + 1)

    # Extrae la parte de los movimientos a mostrar
    ventana_moves = moves[inicio:fin]

    # Muestra los movimientos alrededor del índice actual
    print("\nMovimientos: ", end="")
    for i, move in enumerate(ventana_moves, start=inicio):
        if i == t:
            print(f"{RED}{move}{RESET}", end="")  # Resalta el movimiento actual
        else:
            print(move, end="")
    print()  # Salto de línea al final
    
   
   
    if total <30:
        print("presione enter para continual")

def parse_warehouse(file_path):
    """
    Analiza el mapa del almacén y devuelve la cuadrícula, 
    la posición del robot y las posiciones iniciales de las cajas.
    """
    grid = []
    robot_pos = None
    boxes = set()
    moves = ""
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        for y, line in enumerate(lines):
            row = []
            for x, char in enumerate(line.strip()):
                if char == '@':
                    robot_pos = (y, x)
                    row.append(".")  # Reemplazar el robot por un espacio vacío
                elif char == 'O':
                    boxes.add((y, x))
                    row.append('.')  # Reemplazar la caja por un espacio vacío
                elif char in '#.':
                    row.append(char)
                elif char in '^v<>':  # Los movimientos pueden estar en el mapa
                    moves += char
            grid.append(row)

        return grid, robot_pos, boxes, moves

    except FileExistsError:
        print(f"Error al leer el archivo'{file_path}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error al cargar el archivo: '{e}'")
        sys.exit(1)
def listar_box_a_mover(grid, box, move, new_robot_pos):
    """
    Lista todas las cajas conectadas en línea en la dirección del movimiento.
    
    Args:
        grid: Mapa del almacén.
        box: Tupla con las posiciones izquierda y derecha de la caja ((y1, x1), (y2, x2)).
        move: Dirección de movimiento ('^', 'v', '<', '>').
        new_robot_pos: Nueva posición del robot después del movimiento.
    
    Returns:
        lista_cajas: Lista de todas las cajas en la dirección del movimiento.
        movible: Booleano indicando si todas las cajas pueden moverse.
    """
    directions = {
        '^': (-1, 0),
        'v': (1, 0),
        '<': (0, -1),
        '>': (0, 1),
    }
    
    dy, dx = directions[move]
    lista_cajas = [box]
    movible = True
    
    # Posiciones iniciales de la caja detectada
    left_pos, right_pos = box
    
    # Variables de posición para iterar en la dirección
    next_left = (left_pos[0] + dy, left_pos[1] + dx)
    next_right = (right_pos[0] + dy, right_pos[1] + dx)

    # Itera buscando más cajas en la dirección del movimiento
    while True:
        if (
            0 <= next_left[0] < len(grid) and
            0 <= next_left[1] < len(grid[0]) and
            0 <= next_right[0] < len(grid) and
            0 <= next_right[1] < len(grid[0])
        ):
            if (
                grid[next_left[0]][next_left[1]] == '.' and
                grid[next_right[0]][next_right[1]] == '.'
            ):
                # Espacios vacíos encontrados: no hay más cajas
                break
            elif (
                (next_left, next_right) not in lista_cajas
            ):  # Verifica si hay otra caja alineada
                lista_cajas.append((next_left, next_right))
                next_left = (next_left[0] + dy, next_left[1] + dx)
                next_right = (next_right[0] + dy, next_right[1] + dx)
            else:
                break
        else:
            movible = False
            break

    # Verifica si todas las cajas alineadas pueden moverse
    for left, right in lista_cajas:
        new_left = (left[0] + dy, left[1] + dx)
        new_right = (right[0] + dy, right[1] + dx)
        if not (
            0 <= new_left[0] < len(grid) and
            0 <= new_left[1] < len(grid[0]) and
            0 <= new_right[0] < len(grid) and
            0 <= new_right[1] < len(grid[0]) and
            grid[new_left[0]][new_left[1]] == '.' and
            grid[new_right[0]][new_right[1]] == '.'
        ):
            movible = False
            break

    return lista_cajas, movible


def move_robot(grid, robot_pos, boxes, moves, delay=0.2):
    """
    Mueve el robot y las cajas como entidades completas (izquierda y derecha juntas).
    
    Args:
        grid: Mapa del almacén.
        robot_pos: Posición inicial del robot.
        boxes: Conjunto de pares de posiciones ((y1, x1), (y2, x2)) para cada caja.
        moves: Cadena de movimientos ('^', 'v', '<', '>').
        delay: Tiempo de pausa entre movimientos.
    
    Returns:
        Conjunto de posiciones finales de las cajas.
    """
    directions = {
        '^': (-1, 0),
        'v': (1, 0),
        '<': (0, -1),
        '>': (0, 1),
    }

    for t, move in enumerate(moves):
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpia la consola para la animacion
        # calculo de movimiento del robot
        dy, dx = directions[move]
        new_robot_pos = (robot_pos[0] + dy, robot_pos[1] + dx)
        #detectar una colicion con las paredes
        if (
             0 <= new_robot_pos[0] < len(grid) and
             0 <= new_robot_pos[1] < len(grid[0]) and
             grid[new_robot_pos[0]][new_robot_pos[1]] == '#'
             ):
            continue
        elif ( #detectar espacio vacio . tambien puede haber caja si el grip esta vicio
            0 <= new_robot_pos[0] < len(grid) and
            0 <= new_robot_pos[1] < len(grid[0]) and
            grid[new_robot_pos[0]][new_robot_pos[1]] == '.'
            ):
           #//nose detecto la colicion con la caja
       
        # Verifica si el movimiento del robot afecta a una caja
            for box in boxes:
                left_pos, right_pos = box #posiones de las cajas derecha e izquierda
                if new_robot_pos == left_pos or new_robot_pos == right_pos:  # Detacta colicion con la caja
                    l_box,movable =listar_box_a_mover(grid, box,move,new_robot_pos)
                    if movable:
                    # Mueve todas las cajas en lista_cajas
                        for caja in l_box:
                            boxes.remove(caja)
                            nueva_caja = (
                                (caja[0][0] + dy, caja[0][1] + dx),
                                (caja[1][0] + dy, caja[1][1] + dx),
                                )
                            boxes.add(nueva_caja)
                        robot_pos = new_robot_pos  # Mueve el robot detrás de las cajas
                #break
                else:
                    robot_pos = new_robot_pos#si ha espacio vacio el robot debe moverse


        # Imprime el estado actual del almacén
        imprimir_matrix_con_movimiento(grid, robot_pos, boxes,  new_robot_pos)
        imprimir_posiciones(moves, t)
        print(f"las cajas=> {boxes}")
        print(f"Robot => {robot_pos}")

        # Pausa para visualizar
        if len(moves) < 60:
            input()
        elif len(moves) < 300:
            time.sleep(delay)

    return boxes

def calculate_gps_sum(boxes):
    """
    Calcula la suma GPS para las cajas, considerando la posición izquierda de cada una.
    
    Args:
        boxes: Conjunto de pares de posiciones ((y1, x1), (y2, x2)) para cada caja.
    
    Returns:
        Suma GPS basada en las posiciones izquierdas de las cajas.
    """
    return sum(100 * left[0] + left[1] for left, right in boxes)

def nuevo_mapa(grid, robot_pos, boxes):
    # Lista para el nuevo mapa
    mapa = []

    # Itera sobre cada fila de la cuadrícula original
    for y, row in enumerate(grid):
        nueva_fila = []  # Almacena las celdas de la nueva fila
        for x, cell in enumerate(row):
            if (y, x) == robot_pos:  # Si es la posición del robot
                nueva_fila.append('@.')  # Robot no cambia de tamaño, pero agrega un "."
            elif (y, x) in boxes:  # Si es una caja
                nueva_fila.append('[]')  # Caja se convierte en "[]"
            elif cell == "#":  # Pared
                nueva_fila.append('##')  # Pared se duplica
            elif cell == ".":  # Espacio vacío
                nueva_fila.append('..')  # Espacio vacío se duplica
        mapa.append("".join(nueva_fila))  # Combina las celdas en una fila como cadena
    return mapa
def parse_II(input_map):
    """
    Analiza el mapa ampliado y devuelve:
    - La cuadrícula (grid).
    - La posición del robot.
    - Las posiciones iniciales de las cajas (pares de posiciones).
    """
    grid = []
    robot_pos = None
    boxes = set()

    for y, line in enumerate(input_map):
        row = []
        x = 0
        while x < len(line):
            char = line[x]
            if char == '@':
                robot_pos = (y, x)
                row.append('.')  # Reemplaza el robot con espacio vacío
                x += 1
            elif char == '[' and x + 1 < len(line) and line[x + 1] == ']':  # Caja detectada
                boxes.add(((y, x), (y, x + 1)))
                row.append('.')  # Representa la caja como espacio vacío
                x += 2
            else:
                row.append(char)
                x += 1
        grid.append(row)

    return grid, robot_pos, boxes



def main():
    # Configura el analizador de argumentos
    parser = argparse.ArgumentParser(
        description="Advent of Code dia 15 desfio 2, procesa la informacion del archivo del desafio",
        usage=f"python {sys.argv[0]} <archivo>"
    )
    parser.add_argument(
        'archivo',
        type=str,
        help=f"use: python {sys.argv[0]}  <archivo"
        )
    
    # Analiza los argumentos
    args = parser.parse_args()



    #moves = "<^^>>>vv<v>>v<<"
    #Función principal para analizar la entrada, simular el movimiento del robot y calcular la suma del GPS.
    grid, robot_pos, boxes, moves = parse_warehouse(args.archivo)
    
    
    imprimir_matrix(grid)
    print(f"los movimiento son {moves}")
    mapa2 = nuevo_mapa(grid,robot_pos,boxes)
    imprimir_matrix(mapa2)
    
    grid2,robot_pos,boxes = parse_II(mapa2)
    
    print(f"la posicion del robot es {robot_pos}")
    print(f'la posicion de las cajas es {boxes } ')
    input()
    final_boxes = move_robot(grid2, robot_pos, boxes , moves)
    
   
    result =  calculate_gps_sum(final_boxes)
    print("Sum of GPS coordinates:", result)
    print(f"Tiempo de ejecución: {(time.perf_counter() - start) * 1000:.2f} ms")

"""# Example usage:
input_map = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########"""



if __name__ == "__main__":
    start = time.perf_counter()
    main()
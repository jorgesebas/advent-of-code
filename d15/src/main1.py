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
            elif (y,x)in boxes:
                if(y,x)== movimiento_actual:
                    print(GREEN + 'O' + RESET,end="")  #muestra las cajas
                else:
                    print(BRIGHT_CYAN + 'O' + RESET,end="")  #muestra las cajas
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
    print("\n\r Movimientos: ", end="")
    for i, move in enumerate(ventana_moves, start=inicio):
        if i == t:
            print(f"{RED}{move}{RESET}", end="")  # Resalta el movimiento actual
        else:
            print(move, end="")
    print()  # Salto de línea al final
    if total <60:
        print("presione enter para continuar")



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

def move_robot(grid, robot_pos, boxes, moves,delay=0.4):
    directions = {
        '^': (-1, 0),
        'v': (1, 0),
        '<': (0, -1),
        '>': (0, 1),
    }

    for t, move in enumerate(moves):
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpia la consola
        dy, dx = directions[move]
        new_robot_pos = (robot_pos[0] + dy, robot_pos[1] + dx)

        if new_robot_pos in boxes:  # El robot intenta mover una caja
            movable = True
            current_pos = new_robot_pos
            box_positions = []

            # Revisa si todas las cajas en línea pueden moverse
            while current_pos in boxes:
                box_positions.append(current_pos)
                current_pos = (current_pos[0] + dy, current_pos[1] + dx)

                # Si el próximo espacio está fuera del grid o bloqueado, no se puede mover
                if not (0 <= current_pos[0] < len(grid) and 0 <= current_pos[1] < len(grid[0])):
                    movable = False
                    break
                if grid[current_pos[0]][current_pos[1]] != '.' and current_pos not in boxes:
                    movable = False
                    break

            # Si es posible mover todas las cajas en línea
            if movable:
                for pos in reversed(box_positions):
                    new_pos = (pos[0] + dy, pos[1] + dx)
                    boxes.remove(pos)
                    boxes.add(new_pos)
                robot_pos = new_robot_pos

        elif (
            0 <= new_robot_pos[0] < len(grid) and
            0 <= new_robot_pos[1] < len(grid[0]) and
            grid[new_robot_pos[0]][new_robot_pos[1]] == '.'
        ):
            # Mueve el robot si la nueva posición es válida
            robot_pos = new_robot_pos

        imprimir_matrix_con_movimiento(grid, robot_pos, boxes,(robot_pos[0] + dy, robot_pos[1] + dx))
        imprimir_posiciones(moves, t)
        if(len(moves)<60):
            input()  # Pausa para visualizar
        elif(len(moves)<300):
            time.sleep(delay)
    return boxes


def calculate_gps_sum(boxes):
    #Calcular la suma GPS para las cajas.
    return sum(100 * y + x for y, x in boxes)

def main():
    # Configura el analizador de argumentos
    parser = argparse.ArgumentParser(
        description="Advent of Code dia 15 desfio 1, procesa la informacion del archivo del desafio",
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
    print(f"la posicion del robot es {robot_pos}")
    print(f'la posicion de las cajas es {boxes}')
    
    imprimir_matrix(grid)
    print(f"los movimiento son {moves}")
    moves = moves.replace("\n", "")  # Remove newlines from moves
    final_boxes = move_robot(grid, robot_pos, boxes, moves)
   
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
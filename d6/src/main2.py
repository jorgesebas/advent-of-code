import sys
from time import perf_counter
def cargar_mapa(archivo):
    try:
        with open(archivo, 'r') as f:
            return f.readlines()
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo '{archivo}'.")
        sys.exit(1)


def main():


    start = perf_counter()
    # Verificar si se proporcionó un archivo como argumento
    if len(sys.argv) != 2:
        print(f"ERROR {sys.argv[0]} <archivo_mapa>")
        sys.exit(1)
    archivo_mapa = sys.argv[1]
      # Cargar el mapa
    lines = cargar_mapa(archivo_mapa)


   # with open("mapa1.txt", "r") as f:
    #    lines = f.readlines()
    
    total = 0
    map_data = []
    map_visited = []

    x_guarda_inicial = y_guarda_inicial = 0
    x_guarda = y_guarda = 0
    direccion_guarda = 0  # 0 --> N, 1 --> E, 2 --> S, 3 --> O

    max_x = 0
    max_y = 0
    num_obstaculos = 0

    for line in lines:
        line = line.strip()
        if max_x == 0:
            max_x = len(line)
        if line:
            max_y += 1
            x_values = []
            x_values_visited = []
            for x, char in enumerate(line):
                x_values_visited.append(False)
                if char == '.':
                    x_values.append(False)
                elif char == '#':
                    x_values.append(True)
                    num_obstaculos += 1
                elif char == '^':
                    x_values.append(False)
                    x_guarda, y_guarda = x, max_y - 1
                    x_guarda_inicial, y_guarda_inicial = x, max_y - 1
                else:
                    print(f"Error en la línea {line}")
            map_data.append(x_values)
            map_visited.append(x_values_visited)

    for y in range(max_y):
        for x in range(max_x):
            if x != x_guarda_inicial or y != y_guarda_inicial:
                x_guarda = x_guarda_inicial
                y_guarda = y_guarda_inicial
                direccion_guarda = 0
                salida = False
                infinite_loop = False
                num_loop = 0

                x_loop = []
                y_loop = []
                d_loop = []

                while not salida:
                    is_obstaculo = False
                    if direccion_guarda == 0:  # N
                        y_guarda -= 1
                        if y_guarda < 0:
                            salida = True
                        elif map_data[y_guarda][x_guarda] or (x == x_guarda and y == y_guarda):
                            x_loop.append(x_guarda)
                            y_loop.append(y_guarda)
                            d_loop.append(direccion_guarda)
                            num_loop += 1
                            is_obstaculo = True
                            direccion_guarda += 1
                            y_guarda += 1
                    elif direccion_guarda == 1:  # E
                        x_guarda += 1
                        if x_guarda >= max_x:
                            salida = True
                        elif map_data[y_guarda][x_guarda] or (x == x_guarda and y == y_guarda):
                            x_loop.append(x_guarda)
                            y_loop.append(y_guarda)
                            d_loop.append(direccion_guarda)
                            num_loop += 1
                            is_obstaculo = True
                            direccion_guarda += 1
                            x_guarda -= 1
                    elif direccion_guarda == 2:  # S
                        y_guarda += 1
                        if y_guarda >= max_y:
                            salida = True
                        elif map_data[y_guarda][x_guarda] or (x == x_guarda and y == y_guarda):
                            x_loop.append(x_guarda)
                            y_loop.append(y_guarda)
                            d_loop.append(direccion_guarda)
                            num_loop += 1
                            is_obstaculo = True
                            direccion_guarda += 1
                            y_guarda -= 1
                    elif direccion_guarda == 3:  # O
                        x_guarda -= 1
                        if x_guarda < 0:
                            salida = True
                        elif map_data[y_guarda][x_guarda] or (x == x_guarda and y == y_guarda):
                            x_loop.append(x_guarda)
                            y_loop.append(y_guarda)
                            d_loop.append(direccion_guarda)
                            num_loop += 1
                            is_obstaculo = True
                            direccion_guarda = 0
                            x_guarda += 1

                    if is_obstaculo:
                        for i in range(num_loop - 1):
                            if (x_loop[i] == x_loop[num_loop - 1] and 
                                y_loop[i] == y_loop[num_loop - 1] and 
                                d_loop[i] == d_loop[num_loop - 1]):
                                salida = True
                                infinite_loop = True
                                break

                if infinite_loop:
                    total += 1

    print(f"{(perf_counter() - start) * 1000:.2f} ms")
    print(f"Total infinite loops encontrados: {total}")

if __name__ == "__main__":
    main()

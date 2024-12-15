import sys
import time 
import os
def parse_input(file_path):
    """
    Lee los datos del archivo de entrada y los convierte en una lista de tuplas.
    """
    robots = []
    try:
          with open(file_path, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
            for line in lines:  # Procesar cada línea individualmente
                if not line.startswith("p=") or "v=" not in line:
                 raise ValueError(f"Línea mal formada: {line}")

                # Separar las partes de posición (p) y velocidad (v)
                p_part, v_part = line.split(' v=')  # Divide en "p=..." y "v=..."
                p_x, p_y = map(int, p_part.split('=')[1].split(','))  # Extraer p
                v_x, v_y = map(int, v_part.split(','))  # Extraer v
                
                # Añadir las tuplas al resultado
                robots.append((p_x, p_y, v_x, v_y))
            return robots
    except Exception as e:
        print(f"Error al cargar el archivo: '{e}'")
        sys.exit(1)



# Función para simular el movimiento y verificar el área ocupada
def simulate_and_find_pattern(robots, width, height,delay = 0.5):
    area = float('inf')
    seconds = 0
      # Retardo para animaciones
    max_iterations = 10000  # Límite de iteraciones
    
    while seconds < max_iterations:
        os.system('cls' if os.name == 'nt' else 'clear')
        positions = []
        max_x = max_y = float('-inf')
        min_x = min_y = float('inf')
        
        # Calcular nuevas posiciones
        for x, y, vx, vy in robots:
            new_x = (x + vx * seconds) % width
            if new_x < 0: new_x += width
            new_y = (y + vy * seconds) % height
            if new_y < 0: new_y += height
            
            positions.append((new_x, new_y))
            max_x = max(max_x, new_x)
            min_x = min(min_x, new_x)
            max_y = max(max_y, new_y)
            min_y = min(min_y, new_y)
        
        # Calcular área ocupada
        delta_width = max_x - min_x + 1
        delta_height = max_y - min_y + 1
        area_aux = delta_width * delta_height
        
        print_pattern(positions, width, height)
        print(f"max_x={max_x} min_x={min_x} max_y={max_y} min_y={min_y}")
        print(f"Área = {delta_width} * {delta_height} = {area_aux}")
        print(f"Tiempo = {seconds}")
        
        if area_aux > area:
            return seconds, positions
        area = area_aux
        time.sleep(delay)
        seconds += 1

    # Representar el patrón visualmente
def print_pattern(positions, width, height):
    grid = [["  . " for _ in range(width)] for _ in range(height)]
    #print("posiciones ")
    #print(positions)
    for idx, (x, y) in enumerate(positions):
        if grid[y][x] == "  . ":
            grid[y][x] = f"{(idx+1):3d} "  # Representación de un robot
    else:
        grid[y][x] = " X "  # Colisión 
    for row in grid:
        print("".join(row))


def imprimir_mapa(mapa):
    print("\nInformacion de los Robots")
    for fila in mapa:
        print(fila)
    print()
def main():
     #inicualizar el contador
    start = time.perf_counter()

    if len(sys.argv) != 2:
        print("Uso: python main.py data.txt")
        sys.exit(1)
    else:
        robots = parse_input(sys.argv[1])
        imprimir_mapa(robots)
        input()
        # Dimensiones del espacio
        if sys.argv[1] == "input.txt":
            width, height = 101, 103
        else:
            width, height = 11, 7

            # Lista de robots (posiciones y velocidades de ejemplo)
            """    robots = [
            (0, 4, 3, -3),
            (6, 3, -1, -3),
            (10, 3, -1, 2),
            (2, 0, 2, -1),
            (0, 0, 1, 3),
            (3, 0, -2, -2),
            (7, 6, -1, -3),
            (3, 0, -1, -2),
            (9, 3, 2, 3),
            (7, 3, -1, 2),
            (2, 4, 2, -3),
            (9, 5, -3, -3),
            ]   
            """

        # Ejecutar la simulación para encontrar el patrón
        time_to_pattern, final_positions = simulate_and_find_pattern(robots, width, height)

                # Imprimir el resultado
        print("Time to pattern:", time_to_pattern)


        print(f"Final Pattern:{final_positions}")
        #print_pattern(final_positions, width, height)
        
        print(f"Tiempo de ejecucion {(time.perf_counter() - start) * 1000:.2f} ms")

if __name__ == "__main__":
    main()



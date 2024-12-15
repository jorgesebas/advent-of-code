import sys
from time import perf_counter

def parse_input(file_path):
    """
    Lee los datos del archivo de entrada y los convierte en una lista de tuplas.
    """
    robots = []
    try:
          with open(file_path, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
            for line in lines:  # Procesar cada línea individualmente
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


def imprimir_mapa(mapa):
    print("\nInformacion de los Robots")
    for fila in mapa:
        print(fila)
    print()
def main():
     #inicualizar el contador
    start = perf_counter()

    if len(sys.argv) != 2:
        print("Uso: python main.py data.txt")
        sys.exit(1)
    else:
        robots = parse_input(sys.argv[1])
        imprimir_mapa(robots)
        
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

        # Simulación de movimiento durante 100 segundos
        seconds = 100
        positions = []

        for x, y, vx, vy in robots:
        # Calcular nuevas posiciones con espacio envolvente
            new_x = (x + vx * seconds) % width
            new_y = (y + vy * seconds) % height
            positions.append((new_x, new_y))

        # Contar robots en cada cuadrante
        quadrants = [0, 0, 0, 0]  # [Q1, Q2, Q3, Q4]
        mid_x, mid_y = width // 2, height // 2

        for x, y in positions:
            if x == mid_x or y == mid_y:
                continue  # Ignorar robots exactamente en el medio
            if x > mid_x and y < mid_y:
                quadrants[0] += 1  # Q1
            elif x < mid_x and y < mid_y:
                quadrants[1] += 1  # Q2
            elif x < mid_x and y > mid_y:
                quadrants[2] += 1  # Q3
            elif x > mid_x and y > mid_y:
                quadrants[3] += 1  # Q4

        # Calcular el factor de seguridad
        safety_factor = quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]

        # Imprimir resultados
        print("Quadrants:", quadrants)
        print("Safety Factor:", safety_factor)
        print(f"Tiempo de ejecucion {(perf_counter() - start) * 1000:.2f} ms")

if __name__ == "__main__":
    main()
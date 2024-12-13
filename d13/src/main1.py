import sys
from itertools import product
from time import perf_counter

def solve_claw_machine(a_x, a_y, b_x, b_y, p_x, p_y, max_presses=100):
    """
    Encuentra el número mínimo de fichas necesarias para alinear la garra con el premio.

    Args:
        a_x, a_y: Movimientos en X e Y al presionar el botón A.
        b_x, b_y: Movimientos en X e Y al presionar el botón B.
        p_x, p_y: Coordenadas del premio.
        max_presses: Número máximo de presiones por botón permitido.

    Returns:
        (min_cost, presses_a, presses_b): Costo mínimo y presiones de A y B, o None si no hay solución.
    """
    min_cost = float('inf')
    best_combination = None

    for x, y in product(range(max_presses + 1), repeat=2):
        # Verifica si la combinación x, y cumple las ecuaciones de posición
        if x * a_x + y * b_x == p_x and x * a_y + y * b_y == p_y:
            cost = 3 * x + y  # Calcula el costo
            if cost < min_cost:
                min_cost = cost
                best_combination = (x, y)

    return (min_cost, best_combination[0], best_combination[1]) if best_combination else None

def parse_input(file_path):
    """
    Lee los datos del archivo de entrada y los convierte en una lista de tuplas.

    Args:
        file_path: Ruta al archivo de entrada.

    Returns:
        Una lista de tuplas con la configuración de cada máquina.
    """
    data = []
    try:
        with open(file_path, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
            for i in range(0, len(lines), 3):
                # Extrae los valores de cada línea
                a_x, a_y = map(int, lines[i].split(':')[1].replace('X+', '').replace('Y+', '').split(','))
                b_x, b_y = map(int, lines[i + 1].split(':')[1].replace('X+', '').replace('Y+', '').split(','))
                p_x, p_y = map(int, lines[i + 2].split(':')[1].replace('X=', '').replace('Y=', '').split(','))
                data.append((a_x, a_y, b_x, b_y, p_x, p_y))
        return data
    except Exception as e:
        print(f"Error al cargar el archivo: '{e}'")
        sys.exit(1)

def solve_all_machines(data):
    total_cost = 0
    prizes_won = 0

    for i, (a_x, a_y, b_x, b_y, p_x, p_y) in enumerate(data, start=1):
        result = solve_claw_machine(a_x, a_y, b_x, b_y, p_x, p_y)
        if result:
            min_cost, presses_a, presses_b = result
            print(f"Máquina {i}: Costo mínimo = {min_cost}, A = {presses_a}, B = {presses_b}")
            total_cost += min_cost
            prizes_won += 1
        else:
            print(f"Máquina {i}: No se puede ganar el premio.")

    print(f"\nTotal de premios ganados: {prizes_won}")
    print(f"Costo total mínimo: {total_cost}")

def main():
    #inicualizar el contador
    start = perf_counter()

    if len(sys.argv) != 2:
        print("Uso: python main.py data.txt")
        sys.exit(1)
    else:
        data = parse_input(sys.argv[1])
        solve_all_machines(data)
        print(f"Tiempo de ejecucion {(perf_counter() - start) * 1000:.2f} ms")

if __name__ == "__main__":
    main()

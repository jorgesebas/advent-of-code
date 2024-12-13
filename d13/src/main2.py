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
    
    # Calculamos el determinante y los determinantes auxiliares
    Δ = a_x * b_y - b_x * a_y
    Δx = p_x * b_y - b_x * p_y
    Δy = a_x * p_y - a_y * p_x
    print(f" Δ = {a_x} * {b_y} - {b_x} * {a_y} = {Δ} ")
    print(f"Δx = {p_x} * {b_y} - {a_y} * {p_x} = {Δx}")
    print(f"Δy = {a_x} * {p_y} - {a_y} * {p_x} = {Δy}")
    # Verificamos el determinante para saber si el sistema tiene solución única
    if Δ != 0:
        # Si Δ != 0, calculamos las soluciones de x y y
        x = Δx / Δ
        y = Δy / Δ
        # Comprobamos que x y y son enteros positivos
        if x.is_integer() and y.is_integer() and x >= 0 and y >= 0:
            x = int(x)
            y = int(y)
            cost = 3 * x + y  # Calcula el costo
            best_combination = (x, y)
            min_cost = cost
            
    else:
        # Si Δ == 0, el sistema puede ser inconsistente o tener infinitas soluciones
        # Verificamos si las ecuaciones son proporcionales
        if Δx == 0 and Δy == 0:
            # Infinitas soluciones, pero no podemos usar la Regla de Cramer directamente aquí
            # Deberíamos usar otro enfoque para encontrar soluciones discretas
            print("El sistema tiene infinitas soluciones.")
        else:
            # El sistema es inconsistente, no hay solución
            print("El sistema no tiene solución.")
#    for x, y in product(range(max_presses + 1), repeat=2):
        # Verifica si la combinación x, y cumple las ecuaciones de posición
#        if x * a_x + y * b_x == p_x and x * a_y + y * b_y == p_y:
#            cost = 3 * x + y  # Calcula el costo
#            if cost < min_cost:
#                min_cost = cost
#                best_combination = (x, y)

#    return (min_cost, best_combination[0], best_combination[1]) if best_combination else None
    print(f"los valores de x,y = {x},{y} y el costo = {3 * x + y}")
    return (3 * x + y), x,y 
def imprimir_mapa(mapa):
    for fila in mapa:
        print(f" {fila}")  # Imprime los elementos de cada fila separados por un espacio
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
                # Ajusta las coordenadas del premio según la parte dos
                p_x += 10000000000000
                p_y += 10000000000000
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
    start = perf_counter()
    if len(sys.argv) != 2:
        print("Uso: python main.py data.txt")
        sys.exit(1)
    else:
        data = parse_input(sys.argv[1])
        imprimir_mapa(data)
        print("----------------")
        solve_all_machines(data)
        print(f"Tiempo de ejecucion {(perf_counter() - start) * 1000:.2f} ms")

if __name__ == "__main__":
    main()

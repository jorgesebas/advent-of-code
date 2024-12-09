import sys
from itertools import product
from time import perf_counter

# Función para evaluar una ecuación con los operadores insertados
def evaluate_equation(nums, operators):
    result = nums[0]
    for i in range(1, len(nums)):
        if operators[i-1] == '+':
            result += nums[i]
        elif operators[i-1] == '*':
            result *= nums[i]
    return result

# Función para procesar el archivo de entrada
def process_file(file_path):
    try:
        with open(file_path, 'r') as f:
            equations = []
            for line in f:
                test_value_str, nums_str = line.split(':')
                test_value = int(test_value_str.strip())
                nums = list(map(int, nums_str.strip().split()))
                equations.append((test_value, nums))
            return equations
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo '{file_path}")

# Función principal para resolver el desafío
def solve_challenge(file_path):
    equations = process_file(file_path)
    total_calibration_result = 0
    
    for test_value, nums in equations:
        # Generar todas las combinaciones posibles de operadores
        operators_combinations = product(['+', '*'], repeat=len(nums) - 1)
        
        for operators in operators_combinations:
            if evaluate_equation(nums, operators) == test_value:
                total_calibration_result += test_value
                break  # Solo necesitamos una combinación válida para esta ecuación
                
    return total_calibration_result

# Ejecución principal
if __name__ == "__main__":
    #iniciando el temporizador
    start = perf_counter()
    if len(sys.argv) != 2:
        print("Uso: python main.py data.txt")
        sys.exit(1)

    file_path = sys.argv[1]
    result = solve_challenge(file_path)
    print(f"El resultado total de calibración es: {result}")
    print(f"{(perf_counter() - start) * 1000:.2f} ms")

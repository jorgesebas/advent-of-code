import sys
import argparse
import time


def leer_archivo(file_path):
    """
    Lee un archivo con 
 
    """
    combina = []
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                #'
                line = line.strip() # Limpiar espacio
                if line: 
                    value = int(line)
                    combina.append(value)
                else:
                    print(f"valor no esperado {line}")

        return combina
    except FileNotFoundError:
        print(f"Error al leer el archivo '{file_path}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error al cargar el archivo: '{e}'")
        sys.exit(1)

def next_secret_number(secret):
    MODULO = 16777216  # Valor para la poda

    # Paso 1: Multiplica por 64, mezcla y poda
    secret = (secret ^ (secret * 64)) % MODULO

    # Paso 2: Divide entre 32, redondea hacia abajo, mezcla y poda
    secret = (secret ^ (secret // 32)) % MODULO

    # Paso 3: Multiplica por 2048, mezcla y poda
    secret = (secret ^ (secret * 2048)) % MODULO

    return secret

def calculate_2000th_secret(initial_secrets):
    total = 0
    
    for secret in initial_secrets:
        current = secret
        
        print(f"0: {current}")
        for _ in range(2000):
            
            current = next_secret_number(current)
             
            
           
        total += current

    return total
def main():
    start = time.perf_counter()  # inicializa el contador 
    # Configura el analizador de argumentos
    parser = argparse.ArgumentParser(
        description="Solucion de Advent of Code dia 22 parte 1",
        usage=f"python {sys.argv[0]} <archivo>"
    )
    parser.add_argument(
        'archivo',
        type=str,
        help=f"Uso: python {sys.argv[0]} <archivo>"
    )
    
    # Analiza los argumentos
    args = parser.parse_args()
    initial_secrets = leer_archivo(args.archivo)
    print(initial_secrets) #comprobacion de entrada
    # Entrada del problema
    """initial_secrets = [
    1,   # Cambia estos números por la entrada real del desafío
    10,
    100,
    2024
    ]"""

    # Cálculo del resultado
    result = calculate_2000th_secret(initial_secrets)
    print("Suma de los 2000° números secretos:", result)

    print(f"Tiempo de ejecución: {(time.perf_counter() - start) * 1000:.2f} ms")

  
if __name__ == "__main__":
   main()

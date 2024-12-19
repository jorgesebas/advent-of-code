import sys
import argparse
import time

def leer_archivo(file_path):
    """
    Analiza archivo para obtner los patrones y el diseño
    """
    patrones= []
    diseño = []
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        for x, line in enumerate(lines):
            if (x == 0): # si es la primera linea
                patrones = [item.strip() for item in line.split(",")]
            elif  line.strip():
                diseño.append(line.strip())  # Agregar la línea sin espacios en blanco
        return patrones,diseño

    except FileExistsError:
        print(f"Error al leer el archivo'{file_path}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error al cargar el archivo: '{e}'")
        sys.exit(1)
def count_combinations(design, patterns, memo):
    """
    Cuenta la cantidad de formas en las que se puede formar un diseño usando los patrones disponibles.

    :param design: La cadena de diseño que se va a verificar.
    :param patterns: Un conjunto de patrones de toallas disponibles.
    :param memo: Un diccionario para memorizar. 
    :return: La cantidad de formas en las que se puede formar el diseño.
    """
    if design in memo:
        return memo[design]

    if design == "":
        return 1

    total_combinations = 0

    for pattern in patterns:
        if design.startswith(pattern):
            remaining_design = design[len(pattern):]
            total_combinations += count_combinations(remaining_design, patterns, memo)

    memo[design] = total_combinations
    return total_combinations


def total_design_combinations(patterns, designs):
    """
    Calcula la cantidad total de formas en que se pueden formar todos los diseños utilizando los patrones disponibles.

    :param patterns: Lista de patrones de toallas disponibles.
    :param designs: Lista de diseños deseados.
    :return: La cantidad total de formas de formar todos los diseños.
    """
    patterns_set = set(patterns)  #Utilice un conjunto para búsquedas más rápidas
    total_count = 0

    for design in designs:
       
        c = count_combinations(design, patterns_set, {})
        total_count += c
        print(f"Diseños: {design}\t\t\t combinaciones {c}")

    return total_count
def main():
    start_timer = time.perf_counter()  # Inicializa el contador
    # Configura el analizador de argumentos
    parser = argparse.ArgumentParser(
        description="Desafío de Advent of Code día 19 parte 1",
        usage=f"python {sys.argv[0]} <archivo>"
    )
    parser.add_argument(
        'archivo',
        type=str,
        help=f"Uso: python {sys.argv[0]} <archivo>"
    )
    
    # Analiza los argumentos
    args = parser.parse_args()

    patterns,designs = leer_archivo(args.archivo)
    # Example input
    #patterns = ["r", "wr", "b", "g", "bwu", "rb", "gb", "br"]
    #designs = ["brwrr","bggr","gbbr","rrbgbr", "ubwu", "bwurrg","brgr", "bbrgwb"]

    # Calcula el resultado
    result = total_design_combinations(patterns, designs)
    print(f"Total number of combinations: {result}")


if __name__== "__main__":
    main()
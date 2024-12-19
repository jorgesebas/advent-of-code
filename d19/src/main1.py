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

def can_form_design(design, patterns, memo):
    """
    Comprueba si se puede formar un diseño usando los patrones disponibles.

    :param design: La cadena de diseño que se va a comprobar.
    :param patterns: Un conjunto de patrones de toallas disponibles.
    :param memo: Un diccionario para memorizar.
    :return: Verdadero si se puede formar el diseño, Falso en caso contrario.
    """
    if design in memo:
        return memo[design]

    if design == "":
        return True

    for pattern in patterns:
        if design.startswith(pattern):
            remaining_design = design[len(pattern):]
            if can_form_design(remaining_design, patterns, memo):
                memo[design] = True
                return True

    memo[design] = False
    return False


def count_possible_designs(patterns, designs):
    """
    Cuente cuántos diseños se pueden formar utilizando los patrones disponibles.

    :param patterns: Lista de patrones de toallas disponibles.
    :param designs: Lista de diseños deseados.
    :return: La cantidad de diseños que se pueden formar."""
    BRIGHT_GREEN = '\033[92m'
    LIGHT_GRAY = '\033[37m'
    BRIGHT_CYAN = '\033[96m'
    RESET = '\033[0m' 
    patterns_set = set(patterns)  # Utilice un conjunto para búsquedas más rápidas
    possible_count = 0

    for design in designs:
        print(f"diseños: {design}", end="\t")
        if can_form_design(design, patterns_set, {}):
            possible_count += 1
            print(BRIGHT_GREEN + "posible" + RESET)
        else:
            print(LIGHT_GRAY + "imposible" + RESET)

    return possible_count
def main():
    start_timer = time.perf_counter()  # Inicializa el contador
    # Configura el analizador de argumentos
    parser = argparse.ArgumentParser(
        description="Desafío de Advent of Code día 18 parte 1",
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
    #designs = ["brwrr","bggr","gbbr","rrbgbr", "ubwu", "bwurrg","brgr","bbrgwb", ]
    print(f"patrones {patterns}\ndiseños{designs} ")
    # Calcular el resultado
    result = count_possible_designs(patterns, designs)
    print(f"Numero de diseños posible: {result} ")

if __name__== "__main__":
    main()
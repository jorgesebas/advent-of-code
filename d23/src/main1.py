from itertools import combinations
from collections import defaultdict
import sys
import argparse
import time


def leer_archivo(file_path):
    """
    Lee un archivo con 
 
    """
    lines = []
    puzze = []
    connections = defaultdict(set)
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            
            for line in lines:
                linea = line.strip()
                a, b = linea.split("-")
                connections[a].add(b)
                connections[b].add(a)
                puzze += line 
        return (''.join(puzze)), connections
        
    except FileNotFoundError:
        print(f"Error al leer el archivo '{file_path}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error al cargar el archivo: '{e}'")
        sys.exit(1)
def find_trios(connections):
    trios = set()
    for node in connections:
        neighbors = connections[node]
        # Comprobar combinaciones de vecinos
        for a, b in combinations(neighbors, 2):
            if a in connections[b]:
                trio = tuple(sorted([node, a, b]))
                trios.add(trio)
    return trios

def count_trios_with_t(trios):
    return sum(1 for trio in trios if any(node.startswith("t") for node in trio))

def main():
    start = time.perf_counter()  # inicializa el contador 
    # Configura el analizador de argumentos
    parser = argparse.ArgumentParser(
        description="Solucion de Advent of Code dia 23 parte 1",
        usage=f"python {sys.argv[0]} <archivo>"
    )
    parser.add_argument(
        'archivo',
        type=str,
        help=f"Uso: python {sys.argv[0]} <archivo>"
    )
    
    # Analiza los argumentos
    args = parser.parse_args()
    puzzle_input, conecc = leer_archivo(args.archivo)
    #print("entrada\n", puzzle_input,conecc )
    # Encuentra todos los tríos
    trios = find_trios(conecc)
    print("trios", trios)
    # Cuente tríos con al menos una computadora que comience con 't'
    result = count_trios_with_t(trios)

    print("Tríos totales que contienen al menos una computadora que comienza con 't':", result)

    print(f"Tiempo de ejecución: {(time.perf_counter() - start) * 1000:.2f} ms")

  
if __name__ == "__main__":
   main()
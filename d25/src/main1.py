import sys
import argparse
import time

def leer_archivo(file_path):
    """
    Lee el archivo de entrada y devuelve una lista de matrices.
    """
    matrices = []
    try:
        with open(file_path, 'r') as file:
            matrix = []
            for line in file:
                stripped_line = line.strip()
                if not stripped_line:
                    if matrix:
                        matrices.append(matrix)
                        matrix = []
                elif '#' in stripped_line or '.' in stripped_line:
                    matrix.append(stripped_line)
                else:
                    raise ValueError(f"Carácter no esperado en línea: {stripped_line}")
            if matrix:
                matrices.append(matrix)

        return matrices
    except FileNotFoundError:
        print(f"Error: Archivo '{file_path}' no encontrado.")
        sys.exit(1)
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
        sys.exit(1)

def transponer_matrix(matrix):
    """
    Transpone cada submatriz en la lista de matrices.
    """
    return [["".join(row) for row in zip(*submatrix)] for submatrix in matrix]

def imprimir_matrix(matrix):
    """
    Imprime la lista de matrices con formato.
    """
    print("Matrices:")
    for submatrix in matrix:
        for row in submatrix:
            print(row)
        print()

def analiza(matrix):
    """
    Analiza bloqueos y superposiciones en la matriz transpuesta.
    """
    bloqueos = []
    superposiciones = []

    for submatrix in matrix:
        conteos = [sum(1 for char in row if char == '#') - 1 for row in submatrix]

        if submatrix[0][0] == '#':
            bloqueos.append(conteos)
        else:
            superposiciones.append(conteos)

    return bloqueos, superposiciones

def main():
    # Inicializar temporizador
    tstart = time.perf_counter()

    # Configurar argumentos
    parser = argparse.ArgumentParser(
        description="Solución de Advent of Code día 25 parte 1",
        usage=f"python {sys.argv[0]} <archivo>"
    )
    parser.add_argument('archivo', type=str, help="Ruta del archivo de entrada")
    args = parser.parse_args()

    # Leer y procesar archivo
    matrices = leer_archivo(args.archivo)
    if not matrices:
        print("La matriz cargada está vacía. Verifica el archivo de entrada.")
        sys.exit(1)

    imprimir_matrix(matrices)

    transposed_matrices = transponer_matrix(matrices)
    imprimir_matrix(transposed_matrices)

    bloqueos, claves = analiza(transposed_matrices)
    max_n = len(transposed_matrices[0][0]) - 2  # Tamaño menos los 2 '#' de inicio y fin
    print(f"max_n: {max_n}")

    contador_superposiciones = 0
    for bloqueo in bloqueos:
        for clave in claves:
            ajuste = -1
            for i in range(len(bloqueo)):
                variable = bloqueo[i] + clave[i]
                if variable > max_n:
                    ajuste = i
            if ajuste == -1:
                print(f"Bloqueo {bloqueo} y clave {clave}: Todas las columnas ajustadas.")
                contador_superposiciones += 1
            else:
                print(f"Bloqueo {bloqueo} y clave {clave}: Superposición en columna {ajuste}.")
    print(f"Número de superposiciones: {contador_superposiciones}")

    # Mostrar tiempo de ejecución
    elapsed_time = time.perf_counter() - tstart
    print(f"Tiempo de ejecución: {elapsed_time:.2f} segundos")

if __name__ == "__main__":
    main()

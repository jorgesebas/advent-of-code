import sys

def leer_archivo(nombre_archivo):
    """Lee el archivo de entrada y devuelve el tablero de letras."""
    with open(nombre_archivo, 'r') as archivo:
        return [linea.strip() for linea in archivo]

def buscar_xmas_en_x(tablero):
    filas = len(tablero)
    columnas = len(tablero[0])
    encontrados = []

    # Recorremos todo el tablero, evitando los bordes
    for i in range(1, filas-1):  # Evitamos los bordes
        for j in range(1, columnas-1):
            # Si encontramos una 'A' en la posición central de la posible "X"
            if tablero[i][j] == 'A':
                # Verificamos si cumple con las condiciones del patrón "X-MAS"
                if (tablero[i-1][j-1] == 'M' and tablero[i-1][j+1] == 'M' and
                    tablero[i+1][j-1] == 'S' and tablero[i+1][j+1] == 'S'):
                    encontrados.append((i, j))  # Guardamos la posición central de la "X"
                elif (tablero[i-1][j-1] == 'S' and tablero[i-1][j+1] == 'M' and
                    tablero[i+1][j-1] == 'S' and tablero[i+1][j+1] == 'M'):
                    encontrados.append((i, j))  # Guardamos la posición central de la "X"
                elif (tablero[i-1][j-1] == 'S' and tablero[i-1][j+1] == 'S' and
                    tablero[i+1][j-1] == 'M' and tablero[i+1][j+1] == 'M'):
                    encontrados.append((i, j))  # Guardamos la posición central de la "X"
                elif (tablero[i-1][j-1] == 'M' and tablero[i-1][j+1] == 'S' and
                    tablero[i+1][j-1] == 'M' and tablero[i+1][j+1] == 'S'):
                    encontrados.append((i, j))  # Guardamos la posición central de la "X"
    
    return encontrados

def main():
    # Comprobamos si se pasó un archivo como argumento
    if len(sys.argv) != 2:
        print("Por favor, proporciona el archivo de entrada como argumento.")
        sys.exit(1)
    
    archivo = sys.argv[1]

    # Leemos el archivo y obtenemos el tablero
    tablero = leer_archivo(archivo)

    # Buscamos el patrón X-MAS en forma de X
    resultados = buscar_xmas_en_x(tablero)

    # Mostramos los resultados
    print(f"El patrón X-MAS en forma de X fue encontrado {len(resultados)} veces.")

if __name__ == "__main__":
    main()

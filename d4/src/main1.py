import sys

# Función que verifica si "XMAS" se encuentra en una dirección específica
def buscar_palabra_en_direccion(tablero, palabra, fila, columna, direccion):
    longitud_palabra = len(palabra)
    fila_inicial, columna_inicial = fila, columna
    
    for i in range(longitud_palabra):
        # Calculamos la nueva posición según la dirección
        f = fila_inicial + i * direccion[0]
        c = columna_inicial + i * direccion[1]
        
        # Verificamos si estamos fuera del tablero
        if f < 0 or f >= len(tablero) or c < 0 or c >= len(tablero[0]):
            return False
        
        # Si la letra en la posición no coincide con la palabra, retornamos False
        if tablero[f][c] != palabra[i]:
            return False
    
    return True

# Función para contar las apariciones de la palabra en el tablero
def contar_apariciones(tablero, palabra):
    direcciones = [
        (-1, 0), (1, 0), (0, -1), (0, 1),    # verticales (arriba, abajo) y horizontales (izquierda, derecha)
        (-1, -1), (-1, 1), (1, -1), (1, 1)    # diagonales (4 direcciones)
    ]
    
    contador = 0
    for fila in range(len(tablero)):
        for columna in range(len(tablero[0])):
            # Comprobamos todas las direcciones
            for direccion in direcciones:
                if buscar_palabra_en_direccion(tablero, palabra, fila, columna, direccion):
                    contador += 1
    return contador

# Función para leer el tablero desde un archivo
def leer_tablero_desde_archivo(nombre_archivo):
    with open(nombre_archivo, 'r') as file:
        # Leemos cada línea del archivo y las convertimos en una lista de caracteres
        tablero = [list(line.strip()) for line in file.readlines()]
    return tablero

# Verificamos que se pasó un archivo como argumento
if len(sys.argv) != 2:
    print("Por favor, pasa el archivo de entrada como argumento.")
    sys.exit(1)

# Nombre del archivo que contiene el tablero
archivo = sys.argv[1]

# Leemos el tablero desde el archivo
tablero = leer_tablero_desde_archivo(archivo)

# Palabra a buscar
palabra = "XMAS"

# Contar las apariciones
apariciones = contar_apariciones(tablero, palabra)
print(f"La palabra '{palabra}' aparece {apariciones} veces.")



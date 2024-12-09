import sys

# Definir las direcciones en orden: arriba, derecha, abajo, izquierda
direcciones = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # movimientos para (fila, columna)

# Función para cargar el mapa desde un archivo
def cargar_mapa(archivo):
    with open(archivo, "r") as f:
        return [linea.strip() for linea in f.readlines()]

# Función para simular el movimiento del guardia
def predecir_ruta(mapa, fila_inicial, col_inicial, direccion_inicial):
    fila, col = fila_inicial, col_inicial
    direccion = direccion_inicial
    visitados = set()  # Conjunto para almacenar las posiciones visitadas
    visitados.add((fila, col))
    
    while True:
        # Verificar la siguiente posición en la dirección actual
        next_fila = fila + direcciones[direccion][0]
        next_col = col + direcciones[direccion][1]
        
        # Verificar si el siguiente paso está dentro de los límites del mapa
        if not (0 <= next_fila < len(mapa) and 0 <= next_col < len(mapa[0])):
            break  # El guardia salió del área mapeada
        
        # Verificar si hay un obstáculo
        if mapa[next_fila][next_col] == '#':
            # Si hay un obstáculo, girar 90 grados a la derecha
            direccion = (direccion + 1) % 4
        else:
            # Si no hay obstáculo, avanzar un paso
            fila, col = next_fila, next_col
            visitados.add((fila, col))
    
    return visitados

# Verificar que se pase un archivo como argumento
if len(sys.argv) != 2:
    print("Por favor, pasa el archivo del mapa como argumento.")
    sys.exit(1)

# Cargar el mapa desde el archivo proporcionado
archivo_mapa = sys.argv[1]
mapa = cargar_mapa(archivo_mapa)

# Buscar la posición inicial del guardia (^) y la dirección inicial
direcciones_iniciales = {'^': 0, '>': 1, 'v': 2, '<': 3}
for i, fila in enumerate(mapa):
    for j, celda in enumerate(fila):
        if celda in direcciones_iniciales:
            fila_inicial, col_inicial = i, j
            direccion_inicial = direcciones_iniciales[celda]
            break
    else:
        continue
    break

# Ejecutar la simulación
visitados = predecir_ruta(mapa, fila_inicial, col_inicial, direccion_inicial)

# Mostrar el resultado
print(f"El guardia visitará {len(visitados)} posiciones distintas.")

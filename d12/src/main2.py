from collections import deque
import sys
from time import perf_counter

# Direcciones posibles: arriba, abajo, izquierda, derecha
direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def cargando_archivo(file_path):
    try:
        with open(file_path, 'r') as file:
            mapa = [line.strip() for line in file if line.strip()]
        return [list(row) for row in mapa]  # Convertir las filas en listas de caracteres
    except Exception as e:
        print(f"Error al cargar el archivo: '{e}'")
        sys.exit(1)

def imprimir_mapa(mapa):
    print("\nMapa del jardín:")
    for fila in mapa:
        print(''.join(fila))
    print()

def crea_mapa_vaya(mapa):
    filas = len(mapa)
    columnas = len(mapa[0])

    # Crear la primera y última fila del marco
    marco_superior = "+--" * (columnas - 1) + "+"
    marco_inferior = marco_superior


    # Crear el mapa con el marco lateral
    mapa_con_marco = [marco_superior]
    for fila in mapa:
        fila_con_delimitadores = " "
        for i in range(columnas):
            fila_con_delimitadores += fila[i]
            # Agregar '|' solo si el elemento siguiente es diferente o si es el último
            if i < columnas - 1 and fila[i] != fila[i + 1]:
                fila_con_delimitadores += "|"
            else:
                fila_con_delimitadores += " "  # Espacio si son iguales
        fila_con_marco = f"|{fila_con_delimitadores.strip()}|"
        mapa_con_marco.append(fila_con_marco)
        mapa_con_marco.append(marco_inferior)

    return [list(fila) for fila in mapa_con_marco]  # Convertir de nuevo a listas de caracteres

def contar_lados(mapa, fila, col, direccion_entrada, tipo_planta):
    lados_totales = 0
    for d in direcciones:
        nuevo_fila = fila + d[0]
        nuevo_col = col + d[1]
        
        # Condiciones para la primera exploración (dirección de entrada (0, 0))
        if direccion_entrada == (0, 0):
            if nuevo_fila < 0 or nuevo_fila >= len(mapa) or nuevo_col < 0 or nuevo_col >= len(mapa[0]) or mapa[nuevo_fila][nuevo_col] != tipo_planta:
                lados_totales += 1  # Normalmente se cuentan los lados en la primera exploración

        # Para el resto de la exploración, no contar el lado por donde venimos
        elif (direccion_entrada == d):
            if nuevo_fila < 0 or nuevo_fila >= len(mapa) or nuevo_col < 0 or nuevo_col >= len(mapa[0]) or mapa[nuevo_fila][nuevo_col] != tipo_planta:
                lados_totales += 1  # Contar solo cuando estamos fuera de la planta o en los límites

    return lados_totales

def dfs(mapa, fila, col, tipo_planta, visitado):
    stack = [(fila, col, (0, 0))]  # La primera celda no tiene dirección de entrada, se pasa (0, 0)
    visitado[fila][col] = True
    diraux = (0,0)
    area = 0
    lados_totales = 0

    while stack:
        
        x, y, direccion_entrada = stack.pop()
        area += 1
        lados_totales += contar_lados(mapa, x, y, direccion_entrada, tipo_planta)

        for i, d in enumerate(direcciones):  # Usar el índice de la dirección como entrada
            nuevo_fila = x + d[0]
            nuevo_col = y + d[1]

            if (0 <= nuevo_fila < len(mapa) and 0 <= nuevo_col < len(mapa[0]) and
                not visitado[nuevo_fila][nuevo_col] and mapa[nuevo_fila][nuevo_col] == tipo_planta):
                visitado[nuevo_fila][nuevo_col] = True
                diraux = d
                stack.append((nuevo_fila, nuevo_col, d))  # Pasar la dirección actual como entrada
               

    return area, lados_totales


def calcular_costo_total(mapa):
    filas = len(mapa)
    columnas = len(mapa[0])

    visitado = [[False] * columnas for _ in range(filas)]
    costo_total = 0

    for fila in range(filas):
        for col in range(columnas):
            if not visitado[fila][col]:
                tipo_planta = mapa[fila][col]
                area, lados_totales = dfs(mapa, fila, col, tipo_planta, visitado)
                ap = area * lados_totales
                costo_total += ap
                print(f"Tipo de planta '{tipo_planta}': Área = {area}, Lados = {lados_totales}, Costo = {ap}")
    return costo_total



def main():
    start = perf_counter()

    if len(sys.argv) != 2:
        print(f"Uso: python {sys.argv[0]} <archivo>")
        sys.exit(1)

    # Cargar el mapa desde el archivo
    garden_map = cargando_archivo(sys.argv[1])
    filas = len(garden_map)
    columnas = len(garden_map[0])

    # Imprimir el mapa original
    imprimir_mapa(garden_map)

    # Crear y mostrar el mapa con cercas
    mapa_vaya = crea_mapa_vaya(garden_map)
    imprimir_mapa(mapa_vaya)
    
    # Finalizar el programa
    costo_total = calcular_costo_total(garden_map)
    print(f'El costo total de cercar todas las regiones es: {costo_total}')
    print(f"Tiempo de ejecución: {(perf_counter() - start) * 1000:.2f} ms")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import argparse

# Configuración de argumentos
parser = argparse.ArgumentParser(description="Abrir un archivo y cargarlo en dos vectores.")
parser.add_argument(
    "filename",
    type=str,
    help="El nombre del archivo que deseas abrir."
)
args = parser.parse_args()

# Intentar abrir el archivo
try:
    with open(args.filename, "r") as file:
        left_vector = []
        right_vector = []

        for line in file:
            # Dividir cada línea en dos valores
            numbers = line.strip().split()  # Divide por espacios
            if len(numbers) == 2:  # Asegurarse de que la línea tiene dos columnas
                left, right = map(int, numbers)  # Convertir ambos valores a enteros
                left_vector.append(left)
                right_vector.append(right)
            else:
                print(f"Línea ignorada (no tiene dos columnas): '{line.strip()}'")

    print("Vector izquierdo (primeros 10 elementos):", left_vector[:10])
    print("Vector derecho (primeros 10 elementos):", right_vector[:10])
    

except FileNotFoundError:
    print(f"Error: El archivo '{args.filename}' no existe.")
except ValueError:
    print("Error: Una línea contiene datos no válidos que no pueden convertirse en enteros.")
except Exception as e:
    print(f"Se produjo un error al procesar el archivo: {e}")

# Calcular la puntuación de similitud
puntuacion_similitud = 0

# Iterar sobre cada número en la lista izquierda
for num in left_vector:
    # Contar cuántas veces aparece el número en la lista derecha
    ocurrencias = right_vector.count(num)
    
    # Sumar al puntaje (número * ocurrencias)
    puntuacion_similitud += num * ocurrencias

# Imprimir la puntuación total de similitud
print(f'La puntuación de similitud es: {puntuacion_similitud}')
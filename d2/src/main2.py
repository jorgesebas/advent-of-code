#!/usr/bin/env python3
import argparse

def is_safe(report):
    """
    Verifica si un informe cumple las reglas de seguridad.
    """
    n = len(report)
    for i in range(n - 1):
        diff = report[i + 1] - report[i]
        if diff < -3 or diff > 3:  # Regla de diferencias entre 1 y 3
            return False
        if diff == 0:  # No puede haber dos niveles iguales
            return False

    # Verificar si es consistentemente creciente o decreciente
    increasing = all(report[i] < report[i + 1] for i in range(n - 1))
    decreasing = all(report[i] > report[i + 1] for i in range(n - 1))
    return increasing or decreasing

def is_safe_with_dampener(report):
    """
    Verifica si un informe puede ser seguro eliminando un único nivel.
    """
    n = len(report)
    for i in range(n):
        # Crear una nueva lista sin el nivel en la posición i
        modified_report = report[:i] + report[i + 1:]
        if is_safe(modified_report):
            return True
    return False

def load_data_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            informes = []
            for line in file:
                niveles = list(map(int, line.strip().split()))
                informes.append(niveles)
            return informes
    except FileNotFoundError:
        print(f"Error: El archivo '{file_path}' no existe.")
        exit(1)
    except ValueError:
        print("Error: El archivo contiene datos no válidos. Asegúrate de que todas las líneas contengan solo números.")
        exit(1)
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        exit(1)

def main():
    parser = argparse.ArgumentParser(description="Analiza los informes de niveles.")
    parser.add_argument(
        "file_path",
        type=str,
        help="El nombre del archivo que deseas analizar."
    )
    args = parser.parse_args()

    informes = load_data_from_file(args.file_path)
    resultados = sum(
        1 for informe in informes if is_safe(informe) or is_safe_with_dampener(informe)
    )
    print(f"Cantidad de informes seguros: {resultados}")

if __name__ == "__main__":
    main()



#!/usr/bin/env python3
import argparse

def is_safe_report(report):
    """
    Determina si un informe es seguro.
    Un informe es seguro si:
    1. Todos los niveles son crecientes o decrecientes.
    2. Las diferencias entre niveles adyacentes están entre 1 y 3.
    """
    differences = [report[i + 1] - report[i] for i in range(len(report) - 1)]
    
    # Verificar que todas las diferencias están entre -3 y -1 (decreciente)
    # o entre 1 y 3 (creciente)
    is_increasing = all(1 <= diff <= 3 for diff in differences)
    is_decreasing = all(-3 <= diff <= -1 for diff in differences)
    
    return is_increasing or is_decreasing

def count_safe_reports(data):
    """
    Cuenta cuántos informes son seguros en los datos proporcionados.
    """
    safe_count = 0
    
    for line in data.splitlines():
        if line.strip():  # Ignorar líneas vacías
            try:
                report = list(map(int, line.split()))
                if is_safe_report(report):
                    safe_count += 1
            except ValueError:
                print(f"Error: Línea inválida '{line.strip()}'. Se ignorará.")
    
    return safe_count

def load_data_from_file(file_path):
    """
    Carga los datos desde un archivo de texto.
    """
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: El archivo '{file_path}' no existe.")
        exit(1)
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        exit(1)

def main():
    # Configuración de argumentos
    parser = argparse.ArgumentParser(description="Analiza los informes de niveles.")
    parser.add_argument(
        "file_path",
        type=str,
        help="El nombre del archivo que deseas analizar."
    )
    args = parser.parse_args()

    # Cargar los datos desde el archivo
    data = load_data_from_file(args.file_path)

    # Contar los informes seguros en los datos cargados
    safe_reports = count_safe_reports(data)
    print(f"Número de informes seguros: {safe_reports}")

if __name__ == "__main__":
    main()

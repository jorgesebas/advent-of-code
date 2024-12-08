#!/usr/bin/env python3
import sys

def parse_input(input_text):
    sections = input_text.strip().split("\n\n")
    rules = [tuple(map(int, line.split("|"))) for line in sections[0].split("\n")]
    updates = [list(map(int, update.split(","))) for update in sections[1].split("\n")]
    return rules, updates

def is_update_valid(update, rules):
    # Creamos un índice de las posiciones de las páginas en la actualización
    page_positions = {page: index for index, page in enumerate(update)}
    
    for x, y in rules:
        # Si ambas páginas están en la actualización, verificamos el orden
        if x in page_positions and y in page_positions:
            if page_positions[x] > page_positions[y]:
                return False
    return True

def find_middle_page(update):
    middle_index = len(update) // 2
    return update[middle_index]

def main(file_path):
    # Leer el archivo de entrada
    try:
        with open(file_path, "r") as file:
            puzzle_input = file.read()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {file_path}")
        sys.exit(1)
    
    # Procesar datos
    rules, updates = parse_input(puzzle_input)
    total_middle_sum = 0
    valid_updates = []
    
    for update in updates:
        if is_update_valid(update, rules):
            valid_updates.append(update)
            total_middle_sum += find_middle_page(update)
    
    # Mostrar resultados
    print(f"Suma total de páginas centrales: {total_middle_sum}")
    print("Actualizaciones válidas:")
    for update in valid_updates:
        print(update)

if __name__ == "__main__":
    # Verificar argumentos
    if len(sys.argv) != 2:
        print("Uso: python main.py data.txt")
        sys.exit(1)
    
    # Pasar el archivo al programa
    file_path = sys.argv[1]
    main(file_path)

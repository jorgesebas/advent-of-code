#!/usr/bin/env python3
import sys

def parse_input(file_content):
    """Parses the input into rules and updates."""
    rules_part, updates_part = file_content.strip().split("\n\n")
    rules = [tuple(map(int, line.split('|'))) for line in rules_part.splitlines()]
    updates = [list(map(int, line.split(','))) for line in updates_part.splitlines()]
    return rules, updates


def is_valid_update(update, rules):
    """Checks if an update is valid according to the rules."""
    for x, y in rules:
        if x in update and y in update:
            if update.index(x) > update.index(y):  # x must appear before y
                return False
    return True


def sort_update(update, rules):
    """Sorts an update according to the rules."""
    dependencies = {page: set() for page in update}
    for x, y in rules:
        if x in update and y in update:
            dependencies[y].add(x)
    
    sorted_update = []
    while dependencies:
        # Find a page with no dependencies
        ready_pages = [page for page, deps in dependencies.items() if not deps]
        if not ready_pages:
            raise ValueError("Cyclic dependency detected!")
        ready_pages.sort()  # To ensure deterministic order
        page = ready_pages[0]
        sorted_update.append(page)
        del dependencies[page]
        for deps in dependencies.values():
            deps.discard(page)
    
    return sorted_update


def find_middle_number(update):
    """Finds the middle number of an update."""
    n = len(update)
    return update[n // 2]


def main(file_path):
    # Read the data from the file
    with open(file_path, 'r') as file:
        data = file.read()
    
    rules, updates = parse_input(data)
    
    valid_updates = []
    invalid_updates = []
    
    for update in updates:
        if is_valid_update(update, rules):
            valid_updates.append(update)
        else:
            invalid_updates.append(update)
    
    # Find the sum of middle numbers of valid updates
    middle_sum_valid = sum(find_middle_number(update) for update in valid_updates)
    
    # Correct the invalid updates
    corrected_updates = [sort_update(update, rules) for update in invalid_updates]
    middle_sum_corrected = sum(find_middle_number(update) for update in corrected_updates)
    
    print("Suma de números centrales de actualizaciones válidas:", middle_sum_valid)
    print("Suma de números centrales de actualizaciones corregidas:", middle_sum_corrected)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python main.py <ruta_al_archivo>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    try:
        main(file_path)
    except Exception as e:
        print(f"Error: {e}")

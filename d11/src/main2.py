from time import perf_counter
import sys

def blink_stones(stones, blinks):
    blink_num = 0
    maxb = range(blinks)
    for _ in range(blinks):
        # Calculamos el progreso en la barra
        blink_num += 1
        progreso = ('#' * (blink_num + 1)).ljust(len(maxb))
        print(f'\r[{progreso}] {blink_num}/{len(maxb)}', end='', flush=True)  # Se mantiene en la misma línea
        
        new_stones = []
        for stone in stones:
            if stone == 0:
                new_stones.append(1)
            elif len(str(stone)) % 2 == 0:
                # dividir el número en dos partes
                num_str = str(stone)
                mid = len(num_str) // 2
                left = int(num_str[:mid])
                right = int(num_str[mid:])
                new_stones.extend([left, right])
            else:
                # multiplica por 2024
                new_stones.append(stone * 2024)
        
      
        stones = new_stones
    print()  # Para un salto de línea al finalizar la animación
    return stones

def cargando_archivo(file_path):
    try:
        with open(file_path, 'r') as file:
            stones = list(map(int, file.read().strip().split()))
        return stones
    except Exception as e:
        print(f"Error al cargar el archivo: '{e}'")
        sys.exit(1)

def main():
    # Inicializando el contador
    start = perf_counter()
    
    # Verificando si se ha proporcionado un archivo como argumento
    if len(sys.argv) != 2:
        print(f"use: python {sys.argv[0]} <archivo>")
        sys.exit(1)
    
    initial_stones = cargando_archivo(sys.argv[1])
    print(f"Piedras iniciales => {initial_stones}")
    
    # Número de parpadeos
    blinks = 75
    print(f"Número de parpadeos: {blinks}")
    
    # Calcular el resultado final
    final_stones = blink_stones(initial_stones, blinks)
    print(f"Número de piedras después de {blinks} parpadeos: {len(final_stones)}")
    
    print(f"{(perf_counter() - start) * 1000:.2f} ms")

if __name__ == "__main__":
    main()

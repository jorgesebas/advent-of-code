from time import perf_counter
import sys

def blink_stones(stones,blinks):
    for _ in range(blinks):
        new_stones =[]
        for stone in stones:
            if stone == 0:
                new_stones.append(1)
            elif len(str(stone)) % 2 == 0 :
                # dividir en numero en dos partes
                num_str = str(stone)
                mid = len(num_str) // 2
                left = int(num_str[:mid])
                right =int(num_str[mid:])
                new_stones.extend([left,right])
            else:
                # multiplica por 2024
                new_stones.append(stone * 2024)
        stones = new_stones
       
    return(stones)
def cargando_archivo(file_path):
    try:
        with open(file_path,'r') as file:
              stones = list(map(int, file.read().strip().split()))
        return stones
    except Exception as e:
        print(f"Error al cargar el archivo: '{e}")
        sys.exit(1)
def main():
    #inicializando el contador
    start = perf_counter()
    #verificando si se a proporcionado el un archivo como argumento
    if len(sys.argv) != 2:
        print(f"use: python {sys.argv[0]} <archivo> ")
        sys.exit(1)
    initial_stones = cargando_archivo(sys.argv[1])
    print(f"piedras iniciales =>{initial_stones}")
    #numero de parpadeos
    blinks = 25
    print(f"numero de parpadeos: {blinks}")
    #calcular el resultado final
    final_stones = blink_stones(initial_stones,blinks)
    print(f"Numero en las piedras despues de {blinks} parpadeo: {len(final_stones)}")
    print(f"{(perf_counter() - start) * 1000:.2f} ms")

if __name__== "__main__":
    main()
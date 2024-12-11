#es archivo es para correrlo en https://colab.research.google.com/
from time import perf_counter
import sys

def blink_stones(stones, blinks):
    blink_num = 0
    maxb = range(blinks)
    for _ in range(blinks):
        blink_num += 1
        progreso = ('#' * (blink_num + 1)).ljust(len(maxb))
        print(f'\r[{progreso}] {blink_num}/{len(maxb)}', end='', flush=True)
        
        new_stones = []
        for stone in stones:
            if stone == 0:
                new_stones.append(1)
            elif len(str(stone)) % 2 == 0:
                num_str = str(stone)
                mid = len(num_str) // 2
                left = int(num_str[:mid])
                right = int(num_str[mid:])
                new_stones.extend([left, right])
            else:
                new_stones.append(stone * 2024)
        stones = new_stones
    print()
    return stones

def main():
    start = perf_counter()
    initial_stones = [2, 72, 8949, 0, 981038, 86311, 246, 7636740]
    print(f"Piedras iniciales => {initial_stones}")
    blinks = 75
    print(f"Número de parpadeos: {blinks}")
    final_stones = blink_stones(initial_stones, blinks)
    print(f"Número de piedras después de {blinks} parpadeos: {len(final_stones)}")
    print(f"{(perf_counter() - start) * 1000:.2f} ms")

if __name__ == "__main__":
    main()

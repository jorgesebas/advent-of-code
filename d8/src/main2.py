import sys
import time

def main():
    start = time.time()
    # Verificar si se proporcionó un archivo como argumento
    if len(sys.argv) != 2:
        print(f"python {sys.argv[0]} <archivo_mapa>")
        sys.exit(1)
    # Redirigir la entrada estándar desde un archivo
    try:    
        sys.stdin = open(sys.argv[1], "r")
    except FileExistsError:
        print(f"Error: No se pudo encontrar el archivo '{sys.argv[1]}'.")

    #variables iniciales    
    lines = sys.stdin.readlines()
    total = 0
    num_lines = len(lines)
    num_columns = 0
    mapa = []
    mapa_antinodos = []
    mapa_tipo = []
    mapa_y = []
    mapa_x = []

    for num_lines, line in enumerate(lines, start=1):   
        line = line.strip()
        if num_columns == 0:
            num_columns = len(line)

        mapa_xp = list(line)
        mapa_completo_xp = ['.'] * num_columns

        for i, char in enumerate(line):
            if char != '.':
                mapa_tipo.append(char)
                mapa_y.append(num_lines - 1)
                mapa_x.append(i)

        mapa.append(mapa_xp)
        mapa_antinodos.append(mapa_completo_xp)

    for i in range(len(mapa_tipo)):
        for j in range(i + 1, len(mapa_tipo)):
            if mapa_tipo[i] == mapa_tipo[j]:
                if mapa_antinodos[mapa_y[i]][mapa_x[i]] == '.':
                    mapa_antinodos[mapa_y[i]][mapa_x[i]] = '#'
                    total += 1
                if mapa_antinodos[mapa_y[j]][mapa_x[j]] == '.':
                    mapa_antinodos[mapa_y[j]][mapa_x[j]] = '#'
                    total += 1

                # Calcular diferencias para antinodos
                ydif = -(mapa_y[j] - mapa_y[i])
                xdif = -(mapa_x[j] - mapa_x[i]) if mapa_x[i] < mapa_x[j] else mapa_x[i] - mapa_x[j]

                anti_y1, anti_x1 = mapa_y[i], mapa_x[i]
                fuera = False

                while not fuera:
                    anti_y1 += ydif
                    anti_x1 += xdif

                    if 0 <= anti_y1 < num_lines and 0 <= anti_x1 < num_columns:
                        if mapa_antinodos[anti_y1][anti_x1] == '.':
                            mapa_antinodos[anti_y1][anti_x1] = '#'
                            total += 1
                    else:
                        fuera = True

                ydif = mapa_y[j] - mapa_y[i]
                xdif = mapa_x[j] - mapa_x[i] if mapa_x[i] < mapa_x[j] else -(mapa_x[i] - mapa_x[j])

                anti_y2, anti_x2 = mapa_y[j], mapa_x[j]
                fuera = False

                while not fuera:
                    anti_y2 += ydif
                    anti_x2 += xdif

                    if 0 <= anti_y2 < num_lines and 0 <= anti_x2 < num_columns:
                        if mapa_antinodos[anti_y2][anti_x2] == '.':
                            mapa_antinodos[anti_y2][anti_x2] = '#'
                            total += 1
                    else:
                        fuera = True

    # Mostrar resultados
    print(f"Total antinodes: {total}")
    print(f"{(time.time() - start) * 1000:.2f} ms")


if __name__ == "__main__":
    main()

import time
from typing import List

class Nodo:
    def __init__(self):
        self.num_campos = 0
        self.vallas = []

class Valla:
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna


def calcula_vallas(mapa_pasado, i, j, campo, mapa, num_lines, num_columns, vallas):
    if not mapa_pasado[i][j]:
        mapa_pasado[i][j] = True
        campo.num_campos += 1
        valor = mapa[i][j]

        for k in range(len(vallas)):
            for l in range(len(vallas[k])):
                if vallas[k][l].fila == i and vallas[k][l].columna == j:
                    if k not in campo.vallas:
                        campo.vallas.append(k)
                    break

        if i > 0 and mapa[i - 1][j] == valor:
            calcula_vallas(mapa_pasado, i - 1, j, campo, mapa, num_lines, num_columns, vallas)
        if i < num_lines - 1 and mapa[i + 1][j] == valor:
            calcula_vallas(mapa_pasado, i + 1, j, campo, mapa, num_lines, num_columns, vallas)
        if j > 0 and mapa[i][j - 1] == valor:
            calcula_vallas(mapa_pasado, i, j - 1, campo, mapa, num_lines, num_columns, vallas)
        if j < num_columns - 1 and mapa[i][j + 1] == valor:
            calcula_vallas(mapa_pasado, i, j + 1, campo, mapa, num_lines, num_columns, vallas)


def main():
    start = time.time()

    PATH_FICHERO = "input.txt"
    with open(PATH_FICHERO, "r") as f:
        lines = f.readlines()

    num_lines = len(lines)
    num_columns = len(lines[0].strip())
    mapa = [list(line.strip()) for line in lines]
    mapa_pasado = [[False] * num_columns for _ in range(num_lines)]

    print(f"Lectura fichero: {1000 * (time.time() - start):.2f} ms")

    vallas = []
    num_valla = -1

    for i in range(num_lines):
        for j in range(num_columns):
            tiene_valla = False
            nueva_valla = False

            if i == 0 or mapa[i][j] != mapa[i - 1][j]:
                tiene_valla = True
                if j == 0 or mapa[i][j] != mapa[i][j - 1]:
                    nueva_valla = True

            if tiene_valla:
                valla = Valla(i, j)
                if nueva_valla:
                    num_valla += 1
                    vallas.append([valla])
                else:
                    vallas[num_valla].append(valla)

    total = 0
    for i in range(num_lines):
        for j in range(num_columns):
            campo = Nodo()
            calcula_vallas(mapa_pasado, i, j, campo, mapa, num_lines, num_columns, vallas)
            total += campo.num_campos * len(campo.vallas)

    print(f"Total: {1000 * (time.time() - start):.2f} ms")
    print(f"Total vallas: {total}")

if __name__ == "__main__":
    main()

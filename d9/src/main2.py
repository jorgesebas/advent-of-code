import sys
import time

def main():
    # inicializar el timer
    start_time = time.time()
    
    # Verificar si se proporcionó un archivo como argumento
    if len(sys.argv) != 2:
        print(f"ERROR {sys.argv[0]} <archivo_mapa>")
        sys.exit(1)  # Salir si no se proporciona el archivo

    # variables iniciales
    total = 0
    num_lines = 0

    # Abrir archivo de entrada
    try:
        with open(sys.argv[1], "r") as file:
            # Leer cada línea del archivo
            for line in file:
                num_lines += 1
                map = []
                is_file = True
                file_number = 0
                num_colums = 0

                for i in range(len(line.strip())):
                    if is_file:
                        # Convertir de char a int
                        file_size = int(line[i])
                        for j in range(file_size):
                            map.append(file_number)
                            num_colums += 1
                        file_number += 1
                    else:
                        num_spaces = int(line[i])
                        for j in range(num_spaces):
                            map.append(-1)
                            num_colums += 1

                    is_file = not is_file

                # Registro de tiempo de lectura del archivo
                print(f"Lectura fichero {((time.time() - start_time) * 1000):.2f} ms")

                file_size_tmp = 0
                i_ini = 0
                i_fin = num_colums
                max_space_size = 10
                primer_espacio_libre = 0
                fn = file_number - 1

                for i in range(i_fin - 1, -1, -1):
                    if map[i] == fn:
                        i_ini = i
                        i_fin = i
                        file_size_tmp = 1
                        while i - 1 >= 0 and map[i - 1] == fn:
                            i -= 1
                            i_ini = i
                            file_size_tmp += 1

                        if file_size_tmp <= max_space_size:
                            max_space_size = 0
                            is_primer_espacio_libre = True
                            for j in range(primer_espacio_libre, i):
                                if map[j] < 0:
                                    j_ini = j
                                    j_fin = j
                                    space_size = 1
                                    while j + 1 < len(map) and map[j + 1] < 0:
                                        j += 1
                                        space_size += 1
                                        j_fin = j
                                    if space_size >= file_size_tmp:
                                        for k in range(file_size_tmp):
                                            valor = map[i_ini + k]
                                            map[j_ini + k] = valor
                                            map[i_ini + k] = -1
                                        max_space_size = 10
                                        break
                                    else:
                                        if space_size > max_space_size:
                                            max_space_size = space_size
                                else:
                                    if is_primer_espacio_libre:
                                        primer_espacio_libre = j
                                    is_primer_espacio_libre = False
                        fn -= 1

                # Imprimir el estado de map (opcional, para depuración)
                print("Mapa final de archivos:")
                print(map)

                # Calcular checksum
                for i in range(len(map)):
                    if map[i] >= 0:
                        total += i * map[i]

    except FileNotFoundError:
        print(f"El archivo {sys.argv[1]} no se encuentra.")
        sys.exit(1)

    # Imprimir el tiempo total de ejecución y el checksum
    print(f"Total {((time.time() - start_time) * 1000):.2f} ms")
    print(f"Total checksum: {total}")

# Llamada a la función principal
if __name__ == "__main__":
    main()

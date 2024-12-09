import time
import sys

# Verificar que se pasa el archivo como argumento
if len(sys.argv) != 2:
    print("Uso: python main.py <archivo_de_entrada>")
    sys.exit(1)

# Obtener el archivo de entrada desde los argumentos
input_file = sys.argv[1]

# Abrir archivo
start = time.time()

try:
    with open(input_file, "r") as f:
        lines = f.readlines()
except FileNotFoundError:
    print(f"Error: No se pudo encontrar el archivo '{input_file}'.")
    sys.exit(1)

# Inicializar variables
total = 0
num_lines = 0
num_columns = 0
mapa = []
mapa_antinodos = []
mapa_tipo = []
mapa_y = []
mapa_x = []

# Procesar el archivo línea por línea
for line in lines:
    num_lines += 1
    line = line.strip()
    
    if num_columns == 0:
        num_columns = len(line)

    mapa_xp = []
    mapa_completo_xp = []
    
    for i in range(num_columns):
        mapa_xp.append(line[i])
        mapa_completo_xp.append('.')
        
        if line[i] != '.':
            mapa_tipo.append(line[i])
            mapa_y.append(num_lines - 1)
            mapa_x.append(i)

    mapa.append(mapa_xp)
    mapa_antinodos.append(mapa_completo_xp)

# Bucle para encontrar antinodos
for i in range(len(mapa_tipo)):
    for j in range(i + 1, len(mapa_tipo)):
        if mapa_tipo[i] == mapa_tipo[j]:
            # Calcular primer antinodo
            anti_y1 = mapa_y[i] - (mapa_y[j] - mapa_y[i])
            if mapa_x[i] < mapa_x[j]:
                anti_x1 = mapa_x[i] - (mapa_x[j] - mapa_x[i])
            else:
                anti_x1 = mapa_x[i] + (mapa_x[i] - mapa_x[j])

            if 0 <= anti_y1 < num_lines and 0 <= anti_x1 < num_columns and mapa_antinodos[anti_y1][anti_x1] == '.':
                mapa_antinodos[anti_y1][anti_x1] = '#'
                total += 1

            # Calcular segundo antinodo
            anti_y2 = mapa_y[j] + (mapa_y[j] - mapa_y[i])
            if mapa_x[i] < mapa_x[j]:
                anti_x2 = mapa_x[j] + (mapa_x[j] - mapa_x[i])
            else:
                anti_x2 = mapa_x[j] - (mapa_x[i] - mapa_x[j])

            if 0 <= anti_y2 < num_lines and 0 <= anti_x2 < num_columns and mapa_antinodos[anti_y2][anti_x2] == '.':
                mapa_antinodos[anti_y2][anti_x2] = '#'
                total += 1

# Imprimir mapa de antinodos
for i in range(num_lines):
    print(''.join(mapa_antinodos[i]))

end = time.time()

# Resultados finales
print(f"Tiempo total: {(end - start) * 1000:.2f} ms")
print(f"Total antinodos: {total}")

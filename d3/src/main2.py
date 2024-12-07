import re
import sys

def procesar_memoria(memoria_corrupta):
    # Expresiones regulares para identificar instrucciones
    regex_mul = r"mul\((\d+),(\d+)\)"  # Captura `mul(X,Y)` con X e Y como números
    regex_do = r"do\(\)"               # Identifica `do()`
    regex_dont = r"don't\(\)"          # Identifica `don't()`

    # Buscar todas las instrucciones válidas en el orden en que aparecen
    instrucciones = re.finditer(f"{regex_mul}|{regex_do}|{regex_dont}", memoria_corrupta)

    # Inicializar variables
    suma_total = 0
    habilitado = True  # Al inicio, las multiplicaciones están habilitadas

    # Procesar cada instrucción encontrada
    for instruccion in instrucciones:
        if instruccion.group(0) == "do()":
            habilitado = True
        elif instruccion.group(0) == "don't()":
            habilitado = False
        elif instruccion.group(0).startswith("mul("):
            if habilitado:
                x, y = map(int, instruccion.groups())
                suma_total += x * y

    return suma_total


def main():
    # Verificar que se haya proporcionado un archivo como argumento
    if len(sys.argv) != 2:
        print("Uso: python main.py data.txt")
        sys.exit(1)

    archivo = sys.argv[1]

    try:
        # Leer el contenido del archivo
        with open(archivo, 'r') as f:
            memoria_corrupta = f.read()

        # Procesar la memoria corrupta
        resultado = procesar_memoria(memoria_corrupta)
        print(f"Resultado: {resultado}")

    except FileNotFoundError:
        print(f"Error: El archivo '{archivo}' no existe.")
        sys.exit(1)
    except Exception as e:
        print(f"Se produjo un error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

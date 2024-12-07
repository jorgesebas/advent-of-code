
import re
import sys

def sumar_instrucciones_mul(contenido):
    # Expresión regular para identificar las instrucciones válidas mul(X,Y)
    patron = r"mul\((\d+),(\d+)\)"
    
    # Buscar todas las coincidencias en el contenido
    coincidencias = re.findall(patron, contenido)
    
    # Calcular la suma de los productos
    suma_total = sum(int(x) * int(y) for x, y in coincidencias)
    
    return suma_total

def main():
    # Verificar que se pase el archivo como argumento
    if len(sys.argv) != 2:
        print("Uso: python main.py data.txt")
        sys.exit(1)

    # Leer el archivo proporcionado
    archivo = sys.argv[1]
    try:
        with open(archivo, 'r') as f:
            contenido = f.read()
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo {archivo}")
        sys.exit(1)

    # Procesar el contenido y calcular el resultado
    resultado = sumar_instrucciones_mul(contenido)
    print("Suma total de las instrucciones válidas mul:", resultado)

if __name__ == "__main__":
    main()

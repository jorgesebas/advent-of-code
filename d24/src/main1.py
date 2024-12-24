import sys
import argparse
import time

def leer_archivo(file_path):
    """
    Lee el archivo de entrada y separa las variables iniciales y las operaciones.
    """
    variables = {}
    operaciones = []
   
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                elif ':' in line:
                    clave, valor = line.split(":")
                    clave = clave.strip()
                    valor = int(valor.strip())
                    variables[clave] = valor
                elif '->' in line:
                    partes = line.split(" -> ")
                    entrada = partes[0].split(" ")
                    salida = partes[1].strip()
                    if len(entrada) == 3:  # Operación con dos entradas
                        operaciones.append((entrada[1], entrada[0], entrada[2], salida))
                    else:
                        print(f"Formato de operación inválido: {line}")
                        sys.exit(1)
        return variables, operaciones

    except FileNotFoundError:
        print(f"Error al leer el archivo '{file_path}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
        sys.exit(1)

def simular_sistema(variables, operaciones):
    """
    Simula el sistema de puertas lógicas hasta resolver todas las operaciones.
    """
    operadores = {
        'AND': lambda a, b: a & b,
        'OR': lambda a, b: a | b,
        'XOR': lambda a, b: a ^ b,
    }
    
    pendientes = operaciones[:]
    while pendientes:
        nuevas_pendientes = []
        for operacion in pendientes:
            op, entrada1, entrada2, salida = operacion
            if entrada1 in variables and entrada2 in variables:
                variables[salida] = operadores[op](variables[entrada1], variables[entrada2])
            else:
                nuevas_pendientes.append(operacion)
        if len(pendientes) == len(nuevas_pendientes):
            print("Error: No se pudieron resolver todas las operaciones debido a dependencias no resueltas.")
            sys.exit(1)
        pendientes = nuevas_pendientes
    
    return variables

def calcular_resultado(variables):
    """
    Calcula el número final combinando los bits de las variables que empiezan con 'z'.
    """
    print("variables", variables)
    z_bits = [valor for clave, valor in sorted(variables.items()) if clave.startswith('z')]
    
    print("Z = ",z_bits )
    return int(''.join(map(str, z_bits[::-1])), 2)

def main():
    start = time.perf_counter()
     # Configura el analizador de argumentos
    parser = argparse.ArgumentParser(
        description="Solucion de Advent of Code dia 23 parte 1.\n Simula un sistema lógico de puertas",
        usage=f"python {sys.argv[0]} <archivo>"
    )
    parser.add_argument(
        'archivo',
        type=str,
        help=f"Archivo de entrada con variables y operaciones.\n Uso: python {sys.argv[0]} <archivo>"
    )
    
    args = parser.parse_args()

    variables, operaciones = leer_archivo(args.archivo)
    variables = simular_sistema(variables, operaciones)
    resultado = calcular_resultado(variables)

    print(f"Resultado decimal: {resultado}")
    print(f"Tiempo de ejecución: {(time.perf_counter() - start) * 1000:.2f} ms")

if __name__ == "__main__":
    main()

import sys
import argparse
import time


def leer_archivo(file_path):
    """
    Lee un archivo con registros y un programa,
    y devuelve los valores de A, B, C y la lista del programa.

    Args:
        file_path (str): Ruta al archivo.

    Returns:
        tuple: Una tupla con los valores de A, B, C y el programa (lista de enteros).
    """
    A = B = C = None  # Inicializar los registros como None
    program = []      # Lista para almacenar las instrucciones del programa

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

            for line in lines:
                # Separar el contenido después de ':'
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()      # Limpiar espacios
                    value = value.strip()  # Limpiar espacios

                    # Asignar valores según el registro
                    if key == "Register A":
                        A = int(value)
                    elif key == "Register B":
                        B = int(value)
                    elif key == "Register C":
                        C = int(value)
                    elif key == "Program":
                        # Convertir los números del programa en una lista de enteros
                        program = list(map(int, value.split(',')))
                    else:
                        print(f"caracter no esperado {key}")

        return A, B, C, program

    except FileNotFoundError:
        print(f"Error al leer el archivo '{file_path}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error al cargar el archivo: '{e}'")
        sys.exit(1)
 # Función auxiliar para resolver operandos
def resolve_operand(operand, A, B, C):
    if operand <= 3:
        return operand  # Operandos literales 0-3
    elif operand == 4:
        return A  # Registro A
    elif operand == 5:
        return B  # Registro B
    elif operand == 6:
        return C  # Registro C
    else:
        raise ValueError("Operando inválido")


def run_program( A, B, C , program):
    # Inicializar registros y variables
    pointer = 0  # Puntero de instrucción
    output = []

   
    # Ejecutar programa
    while pointer < len(program):
        opcode = program[pointer]
        operand = program[pointer + 1] if pointer + 1 < len(program) else 0

        if opcode == 0:  # adv: A = A // (2 ** operand)
            denom = 2 ** resolve_operand(operand, A, B, C)
            A //= denom

        elif opcode == 1:  # bxl: B = B ^ operand (literal)
            B ^= operand

        elif opcode == 2:  # bst: B = operand % 8
            B = resolve_operand(operand, A, B, C) % 8

        elif opcode == 3:  # jnz: if A != 0, jump to operand (literal)
            if A != 0:
                pointer = operand
                continue

        elif opcode == 4:  # bxc: B = B ^ C
            B ^= C

        elif opcode == 5:  # out: output operand % 8
            value = resolve_operand(operand, A, B, C) % 8
            output.append(value)

        elif opcode == 6:  # bdv: B = A // (2 ** operand)
            denom = 2 ** resolve_operand(operand, A, B, C)
            B = A // denom

        elif opcode == 7:  # cdv: C = A // (2 ** operand)
            denom = 2 ** resolve_operand(operand, A, B, C)
            C = A // denom

        else:
            raise ValueError(f"Opcode inválido: {opcode}")

        pointer += 2  # Avanzar al siguiente par (opcode, operando)

    return ','.join(map(str, output))

def main():
    start = time.perf_counter()  # inicializa el contador 
    # Configura el analizador de argumentos
    parser = argparse.ArgumentParser(
        description="Desafio de Advent of Code dia 17 parte 1",
        usage=f"python {sys.argv[0]} <archivo>"
    )
    parser.add_argument(
        'archivo',
        type=str,
        help=f"Uso: python {sys.argv[0]} <archivo>"
    )
    
    # Analiza los argumentos
    args = parser.parse_args()
    # Ejemplo proporcionado
    #registers = [729, 0, 0]  # Valores iniciales de los registros
    #program = [0, 1, 5, 4, 3, 0]  # Programa
    A, B, C, program = leer_archivo(args.archivo)
    print(f"Registro A {A}")
    print(f"Registro B {B}")
    print(f"Registro C {C}")
    print(f"Programa {program}")
    
    # Ejecutar el programa
    output = run_program( A, B, C , program)
    print(output)
    print(f"Tiempo de ejecución: {(time.perf_counter() - start) * 1000:.2f} ms")

  
if __name__ == "__main__":
   main()



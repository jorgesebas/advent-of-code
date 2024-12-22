import sys
import argparse
import time



def leer_archivo(file_path):
    """
    Lee un archivo con 
 
    """
    combina = []
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                #'
                line = line.strip() # Limpiar espacio
                if line: 
                    value = int(line)
                    combina.append(value)
                else:
                    print(f"valor no esperado {line}")

        return combina
    except FileNotFoundError:
        print(f"Error al leer el archivo '{file_path}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error al cargar el archivo: '{e}'")
        sys.exit(1)

def next_secret_number(secret):
    MODULO = 16777216  # Valor para la poda

    # Paso 1: Multiplica por 64, mezcla y poda
    secret = (secret ^ (secret * 64)) % MODULO

    # Paso 2: Divide entre 32, redondea hacia abajo, mezcla y poda
    secret = (secret ^ (secret // 32)) % MODULO

    # Paso 3: Multiplica por 2048, mezcla y poda
    secret = (secret ^ (secret * 2048)) % MODULO

    return secret

def calculate_2000th_secret(initial_secrets):
    total = 0
    cambios = [] 
    for r,secret in enumerate(initial_secrets):
        current = secret
        l = []
        #print(f"0,{r}  : {current}")
        for i in range(2000):
            ante_ultimo_digito = abs(current) % 10
            current = next_secret_number(current)
            ultimo_digito = abs(current) % 10 - ante_ultimo_digito 
            #print(f"{i+1},{r} : {current}\t {abs(current) % 10}-{ante_ultimo_digito}={(ultimo_digito)}") #para comprobaciones
            l.append(ultimo_digito)
        total += current
        cambios.append(l)
    return total,cambios
def find_best_sequence(changes):
    """
    Encuentra la mejor secuencia de cambios de precio para maximizar las bananas.
    
    Args:
        changes (list of lists): Matriz de cambios de precio.
    Returns:
        tuple: Una tupla con dos elementos:
            - secuencia: Una lista de listas con las secuencias encontradas.
            - banana: Una lista con los valores máximos de p asociados a cada secuencia.
    """
    
    
    min_sum = 2  # Mínimo valor de la suma de los 4 campos a considerar
    bananas = []
    secuencias= []
    # Recorrer cada fila en la matriz de cambios
    for camp in changes:
        c = 0  # Índice para llenar las secuencias
        secuencia = [[], [], [], []]  # Lista para almacenar hasta 5 secuencias
        banana = [None] * 4  # Lista para almacenar los valores altos de p
        for i in range(len(camp) - 4):  # Aseguramos que haya al menos 4 elementos disponibles
            p = camp[i]  # Valor actual que se está evaluando
            if p >= 6:  # Si existe un valor alto donde se pueda ganar
                seq = camp[i + 1:i + 5]  # Extraer la secuencia de los 4 siguientes elementos
                seq_sum = sum(seq)  # Sumar la secuencia

                # Evaluar si la suma de la secuencia cumple la condición
                if seq_sum <= min_sum:
                    min_sum = seq_sum  # Actualizar el mínimo encontrado
                    secuencia[c] = seq  # Guardar la secuencia en la posición actual
                    banana[c] = p  # Guardar el valor de p asociado
                    # Mover el índice `c` para guardar la siguiente secuencia
                    c = (c + 1) % 4  # Ciclar entre 0 y 4 para sobreescribir
        secuencias.append(secuencia)
        bananas.append(banana)


    return secuencias, bananas


def main():
    start = time.perf_counter()  # inicializa el contador 
    # Configura el analizador de argumentos
    parser = argparse.ArgumentParser(
        description="Solucion de Advent of Code dia 21 parte 2",
        usage=f"python {sys.argv[0]} <archivo>"
    )
    parser.add_argument(
        'archivo',
        type=str,
        help=f"Uso: python {sys.argv[0]} <archivo>"
    )
    
    # Analiza los argumentos
    args = parser.parse_args()
    initial_secrets = leer_archivo(args.archivo)
    print(initial_secrets) #comprobacion de entrada
    # Entrada del problema
    """initial_secrets = [
    1,   # Cambia estos números por la entrada real del desafío
    10,
    100,
    2024
    ]"""

    # Cálculo del resultado
    result,cambios = calculate_2000th_secret(initial_secrets)
    #print(cambios)
    # Cálculo del resultado
    best_sequence,max_bananas= find_best_sequence(cambios)
    print("Mejor secuencia de cambios:", best_sequence)
    suma = 0
    for bana in max_bananas:
        if bana is not None:
            for n_banana in bana:
                if n_banana is not None:
                    suma += n_banana
    print("Máxima cantidad de bananas:", max_bananas)
    print(f"La suma de las bananas es: {suma}")
    print("Suma de los 2000° números secretos:", result)

    print(f"Tiempo de ejecución: {(time.perf_counter() - start) * 1000:.2f} ms")

  
if __name__ == "__main__":
   main()

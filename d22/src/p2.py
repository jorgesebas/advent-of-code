from itertools import product

def next_secret_number(secret):
    MODULO = 16777216  # Valor para la poda

    # Paso 1: Multiplica por 64, mezcla y poda
    secret = (secret ^ (secret * 64)) % MODULO

    # Paso 2: Divide entre 32, redondea hacia abajo, mezcla y poda
    secret = (secret ^ (secret // 32)) % MODULO

    # Paso 3: Multiplica por 2048, mezcla y poda
    secret = (secret ^ (secret * 2048)) % MODULO

    return secret

def simulate_prices(initial_secret, num_steps):
    """Genera una lista de precios y cambios a partir de un secreto inicial."""
    secret = initial_secret
    prices = []

    for _ in range(num_steps):
        prices.append(secret % 10)  # Último dígito es el precio
        secret = next_secret_number(secret)

    changes = [prices[i] - prices[i - 1] for i in range(1, len(prices))]
    return prices, changes

def find_best_sequence(initial_secrets, num_steps=2000):
    """Encuentra la mejor secuencia de cambios de precio para maximizar las bananas."""
    # Genera todas las posibles secuencias de 4 cambios de precio
    possible_sequences = list(product(range(-9, 10), repeat=4))
    
    max_bananas = 0
    best_sequence = None

    for sequence in possible_sequences:
        total_bananas = 0

        for secret in initial_secrets:
            _, changes = simulate_prices(secret, num_steps)

            # Busca la primera ocurrencia de la secuencia en los cambios
            for i in range(len(changes) - len(sequence) + 1):
                if tuple(changes[i:i + 4]) == sequence:
                    total_bananas += (secret % 10)  # Precio correspondiente
                    break

        # Actualiza la mejor secuencia si es necesario
        if total_bananas > max_bananas:
            max_bananas = total_bananas
            best_sequence = sequence

    return best_sequence, max_bananas

# Entrada del problema
initial_secrets = [
    1,   # Cambia estos números por la entrada real del desafío
    2,
    3,
    2024
]

# Cálculo del resultado
best_sequence, max_bananas = find_best_sequence(initial_secrets)
print("Mejor secuencia de cambios:", best_sequence)
print("Máxima cantidad de bananas:", max_bananas)

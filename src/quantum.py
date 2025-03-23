import random

def generate_random_bits(length):
    return [random.randint(0, 1) for _ in range(length)]

def generate_random_bases(length):
    return [random.choice(['H', 'V']) for _ in range(length)]

def encode_bits(bits, bases):
    result = []
    for bit, basis in zip(bits, bases):
        if basis == 'H':
            result.append("|H⟩" if bit == 0 else "|V⟩")
        elif basis == 'V':
            result.append("|D⟩" if bit == 0 else "|A⟩")
    return result

def measure_states(states, bases):
    result = []
    for state, basis in zip(states, bases):
        if basis == 'H':
            result.append(0 if state == "|H⟩" else 1)
        elif basis == 'V':
            result.append(0 if state == "|D⟩" else 1)
    return result

def main():
    length = 10
    bits = generate_random_bits(length)
    bases = generate_random_bases(length)
    states = encode_bits(bits, bases)
    measured_bits = measure_states(states, bases)

    print(f"Переданные биты: {bits}")
    print(f"Использованные базисы: {bases}")
    print(f"Квантовые состояния: {states}")
    print(f"Полученные состояния после канала: {states}")
    print(f"Принимающая сторона: {measured_bits}")

if __name__ == "__main__":
    main()

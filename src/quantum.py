import random

def generate_random_bits(length):
    """Генерирует случайную последовательность битов заданной длины"""
    return [random.randint(0, 1) for _ in range(length)]

def generate_random_bases(length):
    """Генерирует случайную последовательность базисов ('H' или 'V') заданной длины"""
    return [random.choice(['H', 'V']) for _ in range(length)]

def encode_bits(bits, bases):
    """Кодирует биты в квантовые состояния в соответствии с выбранными базисами"""
    result = []
    for bit, basis in zip(bits, bases):
        if basis == 'H':
            result.append("|H⟩" if bit == 0 else "|V⟩")
        elif basis == 'V':
            result.append("|D⟩" if bit == 0 else "|A⟩")
    return result

def measure_states(states, bases):
    """Измеряет квантовые состояния в соответствии с выбранными базисами"""
    result = []
    for state, basis in zip(states, bases):
        if basis == 'H':
            # Если использовался горизонтальный базис, интерпретируем |H⟩ как 0, |V⟩ как 1
            result.append(0 if state == "|H⟩" else 1)
        elif basis == 'V':
            # Если использовался диагональный базис, интерпретируем |D⟩ как 0, |A⟩ как 1
            result.append(0 if state == "|D⟩" else 1)
    return result

def simulate_eavesdropping(states, eavesdropper_bases):
    """Симулирует перехват и измерение квантовых состояний злоумышленником"""
    eavesdropped_bits = []  # Биты, которые получит злоумышленник
    modified_states = []    # Измененные состояния после вмешательства злоумышленника
    
    for state, basis in zip(states, eavesdropper_bases):
        # Злоумышленник измеряет с использованием собственных базисов
        if basis == 'H':
            # Измерение в горизонтальном/вертикальном базисе
            if state == "|H⟩" or state == "|V⟩":
                # Если состояние уже находится в этом базисе, измерение не изменит его
                eavesdropped_bit = 0 if state == "|H⟩" else 1
                new_state = state  # Состояние не меняется при измерении в правильном базисе
            else:  # |D⟩ или |A⟩
                # При измерении в неподходящем базисе результат случаен
                eavesdropped_bit = random.randint(0, 1)  # Случайный результат
                new_state = "|H⟩" if eavesdropped_bit == 0 else "|V⟩"  # Состояние коллапсирует в новый базис
        else:  # basis == 'V'
            # Измерение в диагональном базисе
            if state == "|D⟩" or state == "|A⟩":
                # Если состояние уже находится в этом базисе, измерение не изменит его
                eavesdropped_bit = 0 if state == "|D⟩" else 1
                new_state = state  # Состояние не меняется при измерении в правильном базисе
            else:  # |H⟩ или |V⟩
                # При измерении в неподходящем базисе результат случаен
                eavesdropped_bit = random.randint(0, 1)  # Случайный результат
                new_state = "|D⟩" if eavesdropped_bit == 0 else "|A⟩"  # Состояние коллапсирует в новый базис
                
        eavesdropped_bits.append(eavesdropped_bit)
        modified_states.append(new_state)
        
    return eavesdropped_bits, modified_states

def compare_bases_and_sift_key(alice_bases, bob_bases, bits):
    """Сравнивает базисы измерений и сохраняет только совпадающие биты для ключа"""
    matching_indices = [i for i, (a, b) in enumerate(zip(alice_bases, bob_bases)) if a == b]
    sifted_key = [bits[i] for i in matching_indices]
    return sifted_key, matching_indices

def calculate_error_rate(original_bits, received_bits):
    """Вычисляет частоту ошибок между исходными и полученными битами"""
    if not original_bits:
        return 0
    errors = sum(a != b for a, b in zip(original_bits, received_bits))
    return errors / len(original_bits)

def main():
    length = 20  # Увеличенная длина для лучшей демонстрации
    
    # Алиса генерирует случайные биты и базисы
    alice_bits = generate_random_bits(length)
    alice_bases = generate_random_bases(length)
    
    # Алиса кодирует биты в квантовые состояния
    quantum_states = encode_bits(alice_bits, alice_bases)
    
    print("\n=== Симуляция квантового распределения ключей (протокол BB84) ===")
    print(f"Случайные биты Алисы: {alice_bits}")
    print(f"Случайные базисы Алисы: {alice_bases}")
    print(f"Отправленные квантовые состояния: {quantum_states}")
    
    # Симуляция без подслушивания
    print("\n--- Сценарий 1: Без подслушивания ---")
    
    # Боб выбирает случайные базисы для измерения
    bob_bases = generate_random_bases(length)
    print(f"Случайные базисы Боба: {bob_bases}")
    
    # Боб измеряет состояния
    bob_measured_bits = measure_states(quantum_states, bob_bases)
    print(f"Измеренные биты Боба: {bob_measured_bits}")
    
    # Алиса и Боб сравнивают базисы и просеивают ключ
    sifted_key, matching_indices = compare_bases_and_sift_key(
        alice_bases, bob_bases, alice_bits)
    bob_sifted_key = [bob_measured_bits[i] for i in matching_indices]
    
    print(f"Совпадающие базисы на позициях: {matching_indices}")
    print(f"Просеянный ключ Алисы: {sifted_key}")
    print(f"Просеянный ключ Боба: {bob_sifted_key}")
    
    error_rate = calculate_error_rate(sifted_key, bob_sifted_key)
    print(f"Частота ошибок: {error_rate:.2%}")
    
    if error_rate > 0:
        print("Предупреждение: Обнаружены ошибки, хотя подслушивания не было! Проверьте реализацию.")
    else:
        print("Успех! Ошибки не обнаружены, когда подслушивания не было.")
    
    # Симуляция с подслушиванием
    print("\n--- Сценарий 2: С подслушиванием (Ева) ---")
    
    # Ева генерирует случайные базисы и перехватывает
    eve_bases = generate_random_bases(length)
    eve_bits, modified_states = simulate_eavesdropping(quantum_states, eve_bases)
    
    print(f"Случайные базисы Евы: {eve_bases}")
    print(f"Перехваченные биты Евы: {eve_bits}")
    print(f"Измененные квантовые состояния после измерения Евы: {modified_states}")
    
    # Боб измеряет модифицированные состояния
    bob_measured_bits = measure_states(modified_states, bob_bases)
    print(f"Измеренные биты Боба: {bob_measured_bits}")
    
    # Алиса и Боб сравнивают базисы и просеивают ключ
    sifted_key, matching_indices = compare_bases_and_sift_key(
        alice_bases, bob_bases, alice_bits)
    bob_sifted_key = [bob_measured_bits[i] for i in matching_indices]
    
    print(f"Совпадающие базисы на позициях: {matching_indices}")
    print(f"Просеянный ключ Алисы: {sifted_key}")
    print(f"Просеянный ключ Боба: {bob_sifted_key}")
    
    error_rate = calculate_error_rate(sifted_key, bob_sifted_key)
    print(f"Частота ошибок при подслушивании: {error_rate:.2%}")
    
    if error_rate > 0:
        print(f"Подслушивание обнаружено! Частота ошибок {error_rate:.2%} превышает ожидаемые 0%.")
    else:
        print("Странно! Ошибки не обнаружены, несмотря на подслушивание. Это подозрительно.")

if __name__ == "__main__":
    main()

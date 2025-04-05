import random

class QuantumBB84:
    """Класс для симуляции протокола квантового распределения ключей BB84"""
    
    def __init__(self, length=20):
        """Инициализация с указанной длиной последовательности"""
        self.length = length
        self.reset()
    
    def reset(self):
        """Сбрасывает все данные симуляции"""
        self.alice_bits = []
        self.alice_bases = []
        self.quantum_states = []
        self.bob_bases = []
        self.bob_measured_bits = []
        self.eve_bases = []
        self.eve_bits = []
        self.modified_states = []
        self.matching_indices = []
        self.sifted_key_alice = []
        self.sifted_key_bob = []
        self.error_rate = 0
        self.eavesdropping = False
    
    def generate_random_bits(self, length):
        """Генерирует случайную последовательность битов заданной длины"""
        return [random.randint(0, 1) for _ in range(length)]
    
    def generate_random_bases(self, length):
        """Генерирует случайную последовательность базисов ('+' или '×') заданной длины"""
        return [random.choice(['+', '×']) for _ in range(length)]
    
    def encode_bits(self, bits, bases):
        """Кодирует биты в квантовые состояния в соответствии с выбранными базисами"""
        result = []
        for bit, basis in zip(bits, bases):
            if basis == '+':
                result.append("|0⟩" if bit == 0 else "|1⟩")
            elif basis == '×':
                result.append("|+⟩" if bit == 0 else "|-⟩")
        return result
    
    def measure_states(self, states, bases):
        """Измеряет квантовые состояния в соответствии с выбранными базисами"""
        result = []
        for state, basis in zip(states, bases):
            if basis == '+':
                # Если использовался прямоугольный базис, интерпретируем |0⟩ как 0, |1⟩ как 1
                if state == "|0⟩":
                    result.append(0)
                elif state == "|1⟩":
                    result.append(1)
                else:
                    # Если состояние в другом базисе, результат случайный
                    result.append(random.randint(0, 1))
            elif basis == '×':
                # Если использовался диагональный базис, интерпретируем |+⟩ как 0, |-⟩ как 1
                if state == "|+⟩":
                    result.append(0)
                elif state == "|-⟩":
                    result.append(1)
                else:
                    # Если состояние в другом базисе, результат случайный
                    result.append(random.randint(0, 1))
        return result
    
    def simulate_eavesdropping(self, states, eavesdropper_bases):
        """Симулирует перехват и измерение квантовых состояний злоумышленником"""
        eavesdropped_bits = []  # Биты, которые получит злоумышленник
        modified_states = []    # Измененные состояния после вмешательства злоумышленника
        
        for state, basis in zip(states, eavesdropper_bases):
            # Злоумышленник измеряет с использованием собственных базисов
            if basis == '+':
                # Измерение в прямом базисе (+)
                if state == "|0⟩" or state == "|1⟩":
                    # Если состояние уже находится в этом базисе, измерение не изменит его
                    eavesdropped_bit = 0 if state == "|0⟩" else 1
                    new_state = state  # Состояние не меняется при измерении в правильном базисе
                else:  # |+⟩ или |-⟩
                    # При измерении в неподходящем базисе результат случаен
                    eavesdropped_bit = random.randint(0, 1)  # Случайный результат
                    new_state = "|0⟩" if eavesdropped_bit == 0 else "|1⟩"  # Состояние коллапсирует в новый базис
            else:  # basis == '×'
                # Измерение в диагональном базисе (×)
                if state == "|+⟩" or state == "|-⟩":
                    # Если состояние уже находится в этом базисе, измерение не изменит его
                    eavesdropped_bit = 0 if state == "|+⟩" else 1
                    new_state = state  # Состояние не меняется при измерении в правильном базисе
                else:  # |0⟩ или |1⟩
                    # При измерении в неподходящем базисе результат случаен
                    eavesdropped_bit = random.randint(0, 1)  # Случайный результат
                    new_state = "|+⟩" if eavesdropped_bit == 0 else "|-⟩"  # Состояние коллапсирует в новый базис
                    
            eavesdropped_bits.append(eavesdropped_bit)
            modified_states.append(new_state)
            
        return eavesdropped_bits, modified_states
    
    def compare_bases_and_sift_key(self, alice_bases, bob_bases, bits):
        """Сравнивает базисы измерений и сохраняет только совпадающие биты для ключа"""
        matching_indices = [i for i, (a, b) in enumerate(zip(alice_bases, bob_bases)) if a == b]
        sifted_key = [bits[i] for i in matching_indices]
        return sifted_key, matching_indices
    
    def calculate_error_rate(self, original_bits, received_bits):
        """Вычисляет частоту ошибок между исходными и полученными битами"""
        if not original_bits:
            return 0
        errors = sum(a != b for a, b in zip(original_bits, received_bits))
        return errors / len(original_bits)
    
    def prepare_alice_data(self):
        """Подготавливает данные для Алисы: биты, базисы и квантовые состояния"""
        self.alice_bits = self.generate_random_bits(self.length)
        self.alice_bases = self.generate_random_bases(self.length)
        self.quantum_states = self.encode_bits(self.alice_bits, self.alice_bases)
        return self.alice_bits, self.alice_bases, self.quantum_states
    
    def prepare_bob_data(self):
        """Подготавливает данные для Боба: базисы и измеренные биты"""
        self.bob_bases = self.generate_random_bases(self.length)
        states_to_measure = self.modified_states if self.eavesdropping else self.quantum_states
        self.bob_measured_bits = self.measure_states(states_to_measure, self.bob_bases)
        return self.bob_bases, self.bob_measured_bits
    
    def prepare_eve_data(self):
        """Подготавливает данные для Евы: базисы, измеренные биты и модифицированные состояния"""
        self.eve_bases = self.generate_random_bases(self.length)
        self.eve_bits, self.modified_states = self.simulate_eavesdropping(self.quantum_states, self.eve_bases)
        return self.eve_bases, self.eve_bits, self.modified_states
    
    def sift_keys(self):
        """Сравнивает базисы и генерирует просеянные ключи"""
        self.sifted_key_alice, self.matching_indices = self.compare_bases_and_sift_key(
            self.alice_bases, self.bob_bases, self.alice_bits)
        self.sifted_key_bob = [self.bob_measured_bits[i] for i in self.matching_indices]
        self.error_rate = self.calculate_error_rate(self.sifted_key_alice, self.sifted_key_bob)
        return self.sifted_key_alice, self.sifted_key_bob, self.error_rate
    
    def run_simulation(self, with_eavesdropping=False):
        """Запускает полную симуляцию протокола BB84"""
        self.reset()
        self.eavesdropping = with_eavesdropping
        
        # Генерация данных Алисы
        self.prepare_alice_data()
        
        # Если есть подслушивание, подготавливаем данные Евы
        if self.eavesdropping:
            self.prepare_eve_data()
        
        # Боб выбирает базисы и измеряет состояния
        self.prepare_bob_data()
        
        # Алиса и Боб сравнивают базисы и создают ключи
        self.sift_keys()
        
        return {
            'alice_bits': self.alice_bits,
            'alice_bases': self.alice_bases,
            'quantum_states': self.quantum_states,
            'bob_bases': self.bob_bases,
            'bob_measured_bits': self.bob_measured_bits,
            'matching_indices': self.matching_indices,
            'sifted_key_alice': self.sifted_key_alice,
            'sifted_key_bob': self.sifted_key_bob,
            'error_rate': self.error_rate,
            'eve_present': self.eavesdropping
        }

# Для обратной совместимости старого кода
def generate_random_bits(length):
    return QuantumBB84().generate_random_bits(length)

def generate_random_bases(length):
    return QuantumBB84().generate_random_bases(length)

def encode_bits(bits, bases):
    return QuantumBB84().encode_bits(bits, bases)

def measure_states(states, bases):
    return QuantumBB84().measure_states(states, bases)

def simulate_eavesdropping(states, eavesdropper_bases):
    return QuantumBB84().simulate_eavesdropping(states, eavesdropper_bases)

def compare_bases_and_sift_key(alice_bases, bob_bases, bits):
    return QuantumBB84().compare_bases_and_sift_key(alice_bases, bob_bases, bits)

def calculate_error_rate(original_bits, received_bits):
    return QuantumBB84().calculate_error_rate(original_bits, received_bits)

def main():
    """Основная функция для демонстрации работы протокола BB84 в консоли"""
    simulator = QuantumBB84(length=20)
    
    print("\n=== Симуляция квантового распределения ключей (протокол BB84) ===")
    
    # Симуляция без подслушивания
    print("\n--- Сценарий 1: Без подслушивания ---")
    results = simulator.run_simulation(with_eavesdropping=False)
    
    print(f"Случайные биты Алисы: {results['alice_bits']}")
    print(f"Случайные базисы Алисы: {results['alice_bases']}")
    print(f"Отправленные квантовые состояния: {results['quantum_states']}")
    print(f"Случайные базисы Боба: {results['bob_bases']}")
    print(f"Измеренные биты Боба: {results['bob_measured_bits']}")
    print(f"Совпадающие базисы на позициях: {results['matching_indices']}")
    print(f"Просеянный ключ Алисы: {results['sifted_key_alice']}")
    print(f"Просеянный ключ Боба: {results['sifted_key_bob']}")
    print(f"Частота ошибок: {results['error_rate']:.2%}")
    
    if results['error_rate'] > 0:
        print("Предупреждение: Обнаружены ошибки, хотя подслушивания не было! Проверьте реализацию.")
    else:
        print("Успех! Ошибки не обнаружены, когда подслушивания не было.")
    
    # Симуляция с подслушиванием
    print("\n--- Сценарий 2: С подслушиванием (Ева) ---")
    results = simulator.run_simulation(with_eavesdropping=True)
    
    print(f"Случайные биты Алисы: {results['alice_bits']}")
    print(f"Случайные базисы Алисы: {results['alice_bases']}")
    print(f"Отправленные квантовые состояния: {results['quantum_states']}")
    print(f"Случайные базисы Евы: {simulator.eve_bases}")
    print(f"Перехваченные биты Евы: {simulator.eve_bits}")
    print(f"Измененные квантовые состояния после измерения Евы: {simulator.modified_states}")
    print(f"Случайные базисы Боба: {results['bob_bases']}")
    print(f"Измеренные биты Боба: {results['bob_measured_bits']}")
    print(f"Совпадающие базисы на позициях: {results['matching_indices']}")
    print(f"Просеянный ключ Алисы: {results['sifted_key_alice']}")
    print(f"Просеянный ключ Боба: {results['sifted_key_bob']}")
    print(f"Частота ошибок при подслушивании: {results['error_rate']:.2%}")
    
    if results['error_rate'] > 0:
        print(f"Подслушивание обнаружено! Частота ошибок {results['error_rate']:.2%} превышает ожидаемые 0%.")
    else:
        print("Странно! Ошибки не обнаружены, несмотря на подслушивание. Это подозрительно.")

if __name__ == "__main__":
    main()

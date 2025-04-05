import random

# Алгоритм шифрования рюкзака - асимметричный криптографический алгоритм,
# основанный на задаче об укладке рюкзака (NP-полная задача).
# Использует два типа ключей: закрытый (суперрастущая последовательность) и открытый.

def gen_rand(min_val, max_val):
    """
    Генерирует случайное целое число в заданном диапазоне.
    
    Аргументы:
        min_val (int): Минимальное значение диапазона
        max_val (int): Максимальное значение диапазона
        
    Возвращает:
        int: Случайное число в указанном диапазоне
    """
    return random.randint(min_val, max_val)

def private_key_gen(letter_count):
    """
    Генерирует закрытый ключ в виде суперрастущей последовательности.
    Суперрастущая последовательность - это последовательность, где каждый 
    элемент больше суммы всех предыдущих элементов.
    
    Аргументы:
        letter_count (int): Длина ключа (обычно 8 бит для представления символов)
        
    Возвращает:
        list: Закрытый ключ - суперрастущая последовательность
    """
    private_key = []
    # Начинаем с числа 1 или 2
    private_key.append(gen_rand(1, 2))
    # Генерируем остальные элементы, обеспечивая суперрастущую последовательность
    for _ in range(letter_count - 1):
        # Каждый следующий элемент больше суммы всех предыдущих элементов на случайное число
        new_value = sum(private_key) + gen_rand(3, 4)
        private_key.append(new_value)
    return private_key

def public_key_gen(n, m, private_key):
    """
    Генерирует открытый ключ на основе закрытого ключа и параметров n, m.
    
    Аргументы:
        n (int): Множитель, взаимно простой с m
        m (int): Модуль, больше суммы элементов закрытого ключа
        private_key (list): Закрытый ключ - суперрастущая последовательность
        
    Возвращает:
        list: Открытый ключ - трансформированная последовательность
    """
    # Для каждого элемента закрытого ключа выполняем умножение на n по модулю m
    return [(x * n) % m for x in private_key]

def encrypt_message(message, public_key):
    """
    Шифрует сообщение с помощью открытого ключа.
    
    Аргументы:
        message (str): Исходное текстовое сообщение
        public_key (list): Открытый ключ для шифрования
        
    Возвращает:
        tuple: (Список зашифрованных значений, список деталей шифрования)
    """
    res = []
    encryption_details = []  # Для хранения деталей шифрования каждого символа
    
    for char in message:
        # Преобразуем символ в 8-битное представление
        bits = format(ord(char), '08b')
        encrypt_char = 0
        step_details = {
            'char': char,
            'ascii': ord(char),
            'bits': bits,
            'used_keys': [],
            'sum': 0
        }
        
        # Для каждого бита, если он равен 1, добавляем соответствующий элемент открытого ключа
        for idx, bit in enumerate(bits):
            if bit == '1':
                encrypt_char += public_key[idx]
                step_details['used_keys'].append((idx, public_key[idx]))
                step_details['sum'] += public_key[idx]
        
        step_details['result'] = encrypt_char
        encryption_details.append(step_details)
        # Добавляем зашифрованное значение в результат
        res.append(encrypt_char)
    
    return res, encryption_details

def extended_gcd(a, b):
    """
    Вычисляет наибольший общий делитель и коэффициенты Безу с помощью расширенного алгоритма Евклида.
    Для чисел a и b находит такие x и y, что ax + by = gcd(a,b).
    
    Аргументы:
        a (int): Первое число
        b (int): Второе число
        
    Возвращает:
        tuple: (НОД, x, y) - наибольший общий делитель и коэффициенты Безу
    """
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        # Обратный расчет коэффициентов
        return gcd, y - (b // a) * x, x

def mod_inverse(a, m):
    """
    Находит модульное мультипликативное обратное числа 'a' по модулю 'm'.
    То есть находит число x такое, что (a * x) % m = 1.
    
    Аргументы:
        a (int): Число, для которого ищется обратное
        m (int): Модуль
        
    Возвращает:
        int: Модульное обратное число
        
    Исключения:
        Exception: Если модульное обратное не существует (НОД(a,m) != 1)
    """
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        raise Exception('Модульное обратное не существует')
    else:
        return x % m

def decrypt_message(encrypted_values, private_key, n, m):
    """
    Расшифровывает зашифрованные значения с использованием закрытого ключа и параметров n и m.
    
    Аргументы:
        encrypted_values (list): Список зашифрованных значений
        private_key (list): Закрытый ключ - суперрастущая последовательность
        n (int): Множитель, использованный при генерации открытого ключа
        m (int): Модуль, использованный при генерации открытого ключа
        
    Возвращает:
        tuple: (Расшифрованное сообщение, список деталей дешифрования)
    """
    # Находим обратный элемент к n по модулю m
    n_inverse = mod_inverse(n, m)
    decrypted_message = ""
    decryption_details = []  # Для хранения деталей дешифрования
    
    for value in encrypted_values:
        step_details = {
            'encrypted_value': value,
            'n_inverse': n_inverse,
            'm': m
        }
        
        # Преобразуем в домен закрытого ключа, умножая на обратный элемент
        s_prime = (value * n_inverse) % m
        step_details['s_prime'] = s_prime
        
        # Находим биты, используя суперрастущее свойство закрытого ключа
        # Используем жадный алгоритм, начиная с самых больших элементов
        bits = ['0'] * len(private_key)
        remaining = s_prime
        used_private_keys = []
        
        for i in range(len(private_key) - 1, -1, -1):
            if remaining >= private_key[i]:
                bits[i] = '1'
                remaining -= private_key[i]
                used_private_keys.append((i, private_key[i]))
        
        step_details['bits'] = ''.join(bits)
        step_details['used_private_keys'] = used_private_keys
        
        # Преобразуем биты в символ и добавляем в результат
        char_code = int(''.join(bits), 2)
        step_details['char_code'] = char_code
        step_details['char'] = chr(char_code)
        
        decrypted_message += chr(char_code)
        decryption_details.append(step_details)
        
    return decrypted_message, decryption_details

def generate_keys(bit_length=8):
    """
    Генерирует ключи для алгоритма шифрования рюкзака.
    
    Аргументы:
        bit_length (int): Длина ключа в битах
        
    Возвращает:
        tuple: (private_key, public_key, n, m)
    """
    # Генерируем закрытый ключ
    private_key = private_key_gen(bit_length)
    
    # Выбираем n и m для трансформации ключа
    m = sum(private_key) + gen_rand(10, 100)
    n = gen_rand(2, m - 1)
    while extended_gcd(n, m)[0] != 1:
        n = gen_rand(2, m - 1)
    
    # Генерируем открытый ключ
    public_key = public_key_gen(n, m, private_key)
    
    return private_key, public_key, n, m

def main():
    """
    Основная функция для демонстрации работы алгоритма шифрования рюкзака.
    Показывает примеры шифрования и дешифрования различных сообщений.
    """
    print("=" * 50)
    print("ДЕМОНСТРАЦИЯ АЛГОРИТМА ШИФРОВАНИЯ РЮКЗАКА")
    print("=" * 50)
    
    # Пример 1: Базовая демонстрация
    message = "hello"
    print(f"\nПример 1: Шифрование сообщения '{message}'")
    
    # Генерируем закрытый ключ для 8-битных символов
    private_key = private_key_gen(8)
    print(f"\nСгенерированный закрытый ключ (суперрастущая последовательность):\n{private_key}")
    
    # Выбираем n и m для трансформации ключа
    # m должно быть больше суммы всех элементов закрытого ключа
    m = sum(private_key) + gen_rand(10, 100)
    # n должно быть взаимно простым с m
    n = gen_rand(2, m - 1)
    while extended_gcd(n, m)[0] != 1:
        n = gen_rand(2, m - 1)
        
    print(f"\nПараметры для трансформации ключа:")
    print(f"m = {m} (модуль, больше суммы закрытого ключа)")
    print(f"n = {n} (множитель, взаимно простой с m)")
    
    # Генерируем открытый ключ
    public_key = public_key_gen(n, m, private_key)
    print(f"\nСгенерированный открытый ключ:\n{public_key}")
    
    # Шифруем сообщение
    encrypted, encryption_details = encrypt_message(message, public_key)
    print(f"\nЗашифрованное сообщение (в виде целых чисел):\n{encrypted}")
    print(f"\nДетали шифрования:\n{encryption_details}")
    
    # Расшифровываем сообщение
    decrypted, decryption_details = decrypt_message(encrypted, private_key, n, m)
    print(f"\nРасшифрованное сообщение: '{decrypted}'")
    print(f"\nДетали дешифрования:\n{decryption_details}")
    
    # Пример 2: Еще одна демонстрация с другим сообщением
    print("\n" + "=" * 50)
    message2 = "crypto"
    print(f"\nПример 2: Шифрование сообщения '{message2}'")
    
    # Используем те же ключи для демонстрации
    encrypted2, encryption_details2 = encrypt_message(message2, public_key)
    print(f"\nЗашифрованное сообщение (в виде целых чисел):\n{encrypted2}")
    print(f"\nДетали шифрования:\n{encryption_details2}")
    
    decrypted2, decryption_details2 = decrypt_message(encrypted2, private_key, n, m)
    print(f"\nРасшифрованное сообщение: '{decrypted2}'")
    print(f"\nДетали дешифрования:\n{decryption_details2}")
    
    # Пример 3: Использование пользовательского сообщения
    print("\n" + "=" * 50)
    custom_message = input("\nВведите собственное сообщение для шифрования: ")
    
    # Генерируем новые ключи для этого сообщения
    private_key3 = private_key_gen(8)
    m3 = sum(private_key3) + gen_rand(10, 100)
    n3 = gen_rand(2, m3 - 1)
    while extended_gcd(n3, m3)[0] != 1:
        n3 = gen_rand(2, m3 - 1)
    
    public_key3 = public_key_gen(n3, m3, private_key3)
    
    encrypted3, encryption_details3 = encrypt_message(custom_message, public_key3)
    print(f"\nЗашифрованное сообщение (в виде целых чисел):\n{encrypted3}")
    print(f"\nДетали шифрования:\n{encryption_details3}")
    
    decrypted3, decryption_details3 = decrypt_message(encrypted3, private_key3, n3, m3)
    print(f"\nРасшифрованное сообщение: '{decrypted3}'")
    print(f"\nДетали дешифрования:\n{decryption_details3}")

if __name__ == "__main__":
    # Точка входа в программу
    main()

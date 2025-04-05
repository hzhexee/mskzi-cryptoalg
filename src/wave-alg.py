import random
import math

"""
Реализация алгоритма волнового шифрования (Wave Cipher).

Алгоритм использует тригонометрические функции для создания "волны", которая 
накладывается на ASCII-коды символов исходного сообщения.
Основные параметры шифрования - начальная точка волны (z) и шаг (dx).
"""

def hex_to_vec(message):
    """
    Преобразует шестнадцатеричную строку в список целых чисел.
    
    Каждые два символа из входной строки интерпретируются как одно 
    шестнадцатеричное число и конвертируются в десятичное представление.
    
    Args:
        message (str): Шестнадцатеричная строка
        
    Returns:
        list: Список целых чисел, соответствующих шестнадцатеричным значениям
    """
    res = []
    for i in range(0, len(message), 2):
        res.append(int(message[i:i+2], 16))
    return res

def f_to(x, z, n, dx):
    """
    Функция шифрования отдельного символа.
    
    Добавляет "волновое" смещение к ASCII-коду символа, используя косинусоидальную функцию.
    Параметры z и n*dx определяют фазу косинуса для текущего символа.
    
    Args:
        x (int): ASCII-код символа
        z (float): Начальное значение фазы (ключ шифрования)
        n (int): Позиция символа в сообщении
        dx (float): Шаг изменения фазы (ключ шифрования)
        
    Returns:
        str: Зашифрованный символ
    """
    # Добавляем к коду символа значение косинуса, масштабированное до 255
    res = x + 255 * math.cos(z + n * dx)
    
    # Нормализуем результат, чтобы он находился в пределах 0-255
    if res < 0:
        res += 255
    elif res > 255:
        res -= 255
    
    # Округляем вверх и преобразуем код в символ
    return chr(math.ceil(res))

def f_of(x, z, n, dx):
    """
    Функция дешифрования отдельного символа.
    
    Вычитает "волновое" смещение из ASCII-кода зашифрованного символа.
    Функция является обратной к f_to().
    
    Args:
        x (int): ASCII-код зашифрованного символа
        z (float): Начальное значение фазы (ключ дешифрования)
        n (int): Позиция символа в сообщении
        dx (float): Шаг изменения фазы (ключ дешифрования)
        
    Returns:
        str: Дешифрованный символ
    """
    # Вычитаем из кода символа значение косинуса, масштабированное до 255
    res = x - 255 * math.cos(z + n * dx)
    
    # Нормализуем результат, чтобы он находился в пределах 0-255
    if res < 0:
        res += 255
    elif res > 255:
        res -= 255
    
    # Округляем вниз и преобразуем код в символ
    return chr(math.floor(res))

def encrypt(message, z, dx):
    """
    Шифрует текстовое сообщение с использованием волнового алгоритма.
    
    Для каждого символа применяется функция шифрования f_to().
    Результат конвертируется в шестнадцатеричное представление.
    
    Args:
        message (str): Исходное текстовое сообщение
        z (float): Начальное значение фазы (ключ шифрования)
        dx (float): Шаг изменения фазы (ключ шифрования)
        
    Returns:
        str: Зашифрованное сообщение в шестнадцатеричном формате
    """
    res = ""
    for idx, char in enumerate(message):
        # Шифруем каждый символ и преобразуем результат в шестнадцатеричную строку
        val = f_to(ord(char), z, idx, dx)
        res += format(ord(val), '02x')
    return res

def decrypt(enc_message, z, dx):
    """
    Дешифрует зашифрованное сообщение.
    
    Сначала преобразует шестнадцатеричную строку в числа,
    затем для каждого числа применяет функцию дешифрования f_of().
    
    Args:
        enc_message (str): Зашифрованное сообщение в шестнадцатеричном формате
        z (float): Начальное значение фазы (ключ дешифрования)
        dx (float): Шаг изменения фазы (ключ дешифрования)
        
    Returns:
        str: Дешифрованное текстовое сообщение
    """
    res = ""
    # Преобразуем шестнадцатеричную строку в список чисел
    temp = hex_to_vec(enc_message)
    for idx, num in enumerate(temp):
        # Дешифруем каждое число и добавляем результирующий символ к выходной строке
        res += f_of(num, z, idx, dx)
    return res

def main():
    """
    Демонстрирует работу алгоритма волнового шифрования.
    
    Генерирует случайные ключи шифрования, шифрует и дешифрует тестовое сообщение,
    затем выводит результаты.
    """
    # Тестовое сообщение
    message = "Russia and USA - best friends."
    
    # Генерируем случайные значения ключей
    dx = random.randint(-500, 500)
    z = random.randint(-500, 500)

    # Шифруем и дешифруем сообщение
    enc_message = encrypt(message, z, dx)
    dec_message = decrypt(enc_message, z, dx)
    
    # Преобразуем зашифрованное сообщение в читаемый вид
    enc_readable = ''.join([chr(int(enc_message[i:i+2], 16)) for i in range(0, len(enc_message), 2)])
    
    # Выводим результаты
    print("Зашифрованное сообщение (в читаемом виде):")
    print(enc_readable)
    print("\nРасшифрованное сообщение:")
    print(dec_message)

if __name__ == "__main__":
    main()

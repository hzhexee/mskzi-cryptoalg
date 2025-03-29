# Реализация квантового, волнового и рюкзачного шифрования

## 1. Волновой алгоритм шифрования (wave-alg.py)

Волновой алгоритм шифрования основан на тригонометрических преобразованиях символов текста с использованием косинусоидальной функции.

### Принцип работы:
- Для шифрования каждый символ сообщения преобразуется по формуле: 
  `x + 255 * cos(z + n * dx)`, где:
  - `x` - код символа
  - `z` и `dx` - ключи шифрования
  - `n` - позиция символа в сообщении
- Для дешифрования используется обратная формула: 
  `x - 255 * cos(z + n * dx)`

### Ключевые особенности:
- Два параметра шифрования (`z` и `dx`), генерируемые случайным образом
- Позиционная зависимость шифрования (каждый символ шифруется по-разному в зависимости от его позиции)
- Результат шифрования представлен в шестнадцатеричном формате

## 2. Квантовое шифрование (quantum.py)

Реализация имитирует протокол квантового распределения ключей BB84, используемый для безопасной передачи криптографического ключа.

### Принцип работы:
- Генерация случайной последовательности битов (0 и 1)
- Выбор случайных базисов измерения ('H' - горизонтальный/вертикальный или 'V' - диагональный)
- Кодирование битов в квантовые состояния в зависимости от выбранного базиса:
  - В базисе 'H': бит 0 кодируется как |H⟩, бит 1 как |V⟩
  - В базисе 'V': бит 0 кодируется как |D⟩, бит 1 как |A⟩
- Измерение состояний на приемной стороне, которое корректно декодирует биты только при совпадении базисов

### Ключевые особенности:
- Безопасность основана на принципах квантовой физики
- Любая попытка перехвата приводит к изменению квантовых состояний
- Для получения общего секретного ключа используются только те биты, для которых базисы отправителя и получателя совпали

## 3. Рюкзачное шифрование (knapsack.py)

Реализация криптосистемы Меркла-Хеллмана, основанной на задаче о рюкзаке, которая является NP-полной задачей.

### Принцип работы:
- Генерация приватного ключа в виде сверхвозрастающей последовательности чисел
- Трансформация приватного ключа в публичный ключ с использованием двух параметров:
  - модуля `m`, большего суммы всех элементов приватного ключа
  - числа `n`, взаимно простого с `m`
- Шифрование сообщения путем представления каждого символа в виде битов и умножения на соответствующие элементы публичного ключа

### Ключевые особенности:
- Асимметричная криптосистема с публичным и приватным ключами
- Безопасность основана на сложности решения задачи о рюкзаке
- Для каждого символа сообщения создается 8-битное представление, которое затем шифруется

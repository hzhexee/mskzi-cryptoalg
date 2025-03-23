import random

def gen_rand(min_val, max_val):
    return random.randint(min_val, max_val)

def private_key_gen(letter_count):
    private_key = []
    private_key.append(gen_rand(1, 2))
    for _ in range(letter_count - 1):
        new_value = sum(private_key) + gen_rand(3, 4)
        private_key.append(new_value)
    return private_key

def public_key_gen(n, m, private_key):
    return [(x * n) % m for x in private_key]

def encrypt_message(message, public_key):
    res = []
    for char in message:
        # Преобразуем символ в 8-битное представление
        bits = format(ord(char), '08b')
        encrypt_char = 0
        for idx, bit in enumerate(bits):
            if bit == '1':
                encrypt_char += public_key[idx]
        res.append(encrypt_char)
    return res

def main():
    message = "kriminalkishki"
    private_key = private_key_gen(len(message))
    n = 45
    m = gen_rand(max(private_key), max(private_key) + 200)
    public_key = public_key_gen(n, m, private_key)
    encrypt = encrypt_message(message, public_key)
    
    print(len(message))
    print(private_key)
    print(public_key)
    print(encrypt)

if __name__ == "__main__":
    main()

import random
import math

def hex_to_vec(message):
    res = []
    for i in range(0, len(message), 2):
        res.append(int(message[i:i+2], 16))
    return res

def f_to(x, z, n, dx):
    res = x + 255 * math.cos(z + n * dx)
    if res < 0:
        res += 255
    elif res > 255:
        res -= 255
    return chr(math.ceil(res))

def f_of(x, z, n, dx):
    res = x - 255 * math.cos(z + n * dx)
    if res < 0:
        res += 255
    elif res > 255:
        res -= 255
    return chr(math.floor(res))

def encrypt(message, z, dx):
    res = ""
    for idx, char in enumerate(message):
        val = f_to(ord(char), z, idx, dx)
        res += format(ord(val), '02x')
    return res

def decrypt(enc_message, z, dx):
    res = ""
    temp = hex_to_vec(enc_message)
    for idx, num in enumerate(temp):
        res += f_of(num, z, idx, dx)
    return res

def main():
    message = "A bear was walking through the forest and saw a car on fire. He got in the car and burned to death."
    dx = random.randint(-500, 500)
    z = random.randint(-500, 500)

    enc_message = encrypt(message, z, dx)
    dec_message = decrypt(enc_message, z, dx)
    
    # Выводим зашифрованное сообщение в читаемом виде
    enc_readable = ''.join([chr(int(enc_message[i:i+2], 16)) for i in range(0, len(enc_message), 2)])
    print(enc_readable)
    print(dec_message)

if __name__ == "__main__":
    main()

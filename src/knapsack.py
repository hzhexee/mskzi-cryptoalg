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

def extended_gcd(a, b):
    """Calculate the greatest common divisor and Bézout coefficients using the extended Euclidean algorithm."""
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return gcd, y - (b // a) * x, x

def mod_inverse(a, m):
    """Find the modular multiplicative inverse of 'a' modulo 'm'."""
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % m

def decrypt_message(encrypted_values, private_key, n, m):
    """Decrypt the encrypted values using the private key and parameters n and m."""
    n_inverse = mod_inverse(n, m)
    decrypted_message = ""
    
    for value in encrypted_values:
        # Convert to the private key domain
        s_prime = (value * n_inverse) % m
        
        # Find the bits using the superincreasing property of the private key
        bits = ['0'] * len(private_key)
        for i in range(len(private_key) - 1, -1, -1):
            if s_prime >= private_key[i]:
                bits[i] = '1'
                s_prime -= private_key[i]
        
        # Convert bits to character and add to result
        char_code = int(''.join(bits), 2)
        decrypted_message += chr(char_code)
        
    return decrypted_message

def main():
    print("=" * 50)
    print("KNAPSACK ENCRYPTION ALGORITHM DEMONSTRATION")
    print("=" * 50)
    
    # Example 1: Basic demonstration
    message = "hello"
    print(f"\nExample 1: Encrypting the message '{message}'")
    
    # Generate a private key for 8-bit characters
    private_key = private_key_gen(8)
    print(f"\nGenerated private key (superincreasing sequence):\n{private_key}")
    
    # Choose n and m for key transformation
    # m must be greater than the sum of all elements in the private key
    m = sum(private_key) + gen_rand(10, 100)
    # n must be coprime to m
    n = gen_rand(2, m - 1)
    while extended_gcd(n, m)[0] != 1:
        n = gen_rand(2, m - 1)
        
    print(f"\nParameters for key transformation:")
    print(f"m = {m} (modulus, greater than sum of private key)")
    print(f"n = {n} (multiplier, coprime with m)")
    
    # Generate the public key
    public_key = public_key_gen(n, m, private_key)
    print(f"\nGenerated public key:\n{public_key}")
    
    # Encrypt the message
    encrypted = encrypt_message(message, public_key)
    print(f"\nEncrypted message (as integers):\n{encrypted}")
    
    # Decrypt the message
    decrypted = decrypt_message(encrypted, private_key, n, m)
    print(f"\nDecrypted message: '{decrypted}'")
    
    # Example 2: Another demonstration with a different message
    print("\n" + "=" * 50)
    message2 = "crypto"
    print(f"\nExample 2: Encrypting the message '{message2}'")
    
    # Use the same keys for demonstration
    encrypted2 = encrypt_message(message2, public_key)
    print(f"\nEncrypted message (as integers):\n{encrypted2}")
    
    decrypted2 = decrypt_message(encrypted2, private_key, n, m)
    print(f"\nDecrypted message: '{decrypted2}'")
    
    # Example 3: Using a custom message
    print("\n" + "=" * 50)
    custom_message = input("\nEnter your own message to encrypt: ")
    
    # Generate new keys for this message
    private_key3 = private_key_gen(8)
    m3 = sum(private_key3) + gen_rand(10, 100)
    n3 = gen_rand(2, m3 - 1)
    while extended_gcd(n3, m3)[0] != 1:
        n3 = gen_rand(2, m3 - 1)
    
    public_key3 = public_key_gen(n3, m3, private_key3)
    
    encrypted3 = encrypt_message(custom_message, public_key3)
    print(f"\nEncrypted message (as integers):\n{encrypted3}")
    
    decrypted3 = decrypt_message(encrypted3, private_key3, n3, m3)
    print(f"\nDecrypted message: '{decrypted3}'")

if __name__ == "__main__":
    main()

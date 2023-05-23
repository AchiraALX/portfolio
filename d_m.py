#!/usr/bin/env python3
"""The following cod is used to encrypt
and decrypt messages using the Caesar Cipher.

Keyword arguments:
argument -- description
Return: return_description
"""

import pdb
import random

def generate_prime_modulus():
    # Generate random prime modulus
    while True:
        prime_modulus = random.randint(100, 10000)
        if is_prime(prime_modulus):
            return prime_modulus

def is_prime(number):
    # Check if a number is prime
    if number < 2:
        return False

    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return False

    return True

def encode_password(password):
    encoded_password = ""

    # Define parameters for the finite field
    prime_modulus = generate_prime_modulus()
    field_size = prime_modulus - 1

    # Iterate over each character in the password
    for char in password:
        # Convert the character to its corresponding
        # Unicode code point
        unicode_value = ord(char)

        # Perform modular arithmetic using the finite
        # field
        transformed_value = (unicode_value * 2) % field_size

        # Convert the Unicode code point back to a
        # character
        encoded_char = chr(transformed_value)

        # Append the encoded character to the encoded
        # password
        encoded_password += encoded_char

    return encoded_password

def decode_password(encoded_password):
    password = ""

    # Define parameters for the finite field
    prime_modulus = generate_prime_modulus()
    field_size = prime_modulus - 1

    # Iterate over each character in the encoded
    # password
    for encoded_char in encoded_password:
        # Convert the character to its corresponding
        # Unicode code point
        transformed_value = ord(encoded_char)

        # Perform modular arithmetic using the finite
        # field
        unicode_value = (transformed_value * (field_size // 2)) % prime_modulus

        # Convert the Unicode value back to a character
        char = chr(unicode_value)

        # Append the decoded character to the password
        password += char

    return password

def main():
    # Get the password from the user
    password = input("Enter your password: ")

    # Encode the password
    encoded_password = encode_password(password)

    # Set a breakpoint
    pdb.set_trace()

    # Display the encoded password
    print("Encoded password: " + encoded_password)

    # Decode the password
    decoded_password = decode_password(encoded_password)

    # Display the decoded password
    print("Decoded password: " + decoded_password)

if __name__ == "__main__":
    main()
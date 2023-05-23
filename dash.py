#!/usr/bin/env python3
import pdb
import random

def generate_prime_modulus():
    # Generate a random prime modulus
    while True:
        prime_modulus = random.randint(100, 1000)  # Adjust the range as desired
        if is_prime(prime_modulus):
            return prime_modulus

def is_prime(num):
    # Check if a number is prime
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

def compute_inverse(a, m):
    # Compute the modular multiplicative inverse of a modulo m
    g, x, y = extended_euclidean_algorithm(a, m)
    if g == 1:
        return x % m
    raise ValueError("The modular multiplicative inverse does not exist.")

def extended_euclidean_algorithm(a, b):
    # Extended Euclidean algorithm to compute the greatest common divisor and the Bezout's coefficients
    if a == 0:
        return b, 0, 1
    g, x, y = extended_euclidean_algorithm(b % a, a)
    return g, y - (b // a) * x, x

def encode_password(password, prime_modulus):
    encoded_password = ""

    # Define the parameters for the finite field
    field_size = prime_modulus - 1

    # Compute the modular multiplicative inverse of 2 modulo field_size
    inverse = compute_inverse(2, field_size)

    # Iterate over each character in the password
    for char in password:
        # Convert the character to its corresponding Unicode code point
        unicode_value = ord(char)

        # Perform modular arithmetic using the finite field
        transformed_value = (unicode_value * 2) % field_size

        # Convert the transformed value back to a character
        encoded_char = chr(transformed_value)

        # Append the encoded character to the encoded password
        encoded_password += encoded_char

    return encoded_password

def decode_password(encoded_password, prime_modulus):
    password = ""

    # Define the parameters for the finite field
    field_size = prime_modulus - 1

    # Compute the modular multiplicative inverse of 2 modulo field_size
    inverse = compute_inverse(2, field_size)

    # Iterate over each character in the encoded password
    for encoded_char in encoded_password:
        # Convert the encoded character to its corresponding Unicode code point
        transformed_value = ord(encoded_char)

        # Perform modular arithmetic using the finite field and the inverse
        unicode_value = (transformed_value * inverse) % prime_modulus

        # Convert the Unicode value back to a character
        char = chr(unicode_value)

        # Append the character to the password
        password += char

    return password

# Main program
def main():
    # Get the password from user input
    password = input("Enter your password: ")

    # Generate a random prime modulus
    prime_modulus = generate_prime_modulus()

    max_retries = 1000  # Adjust the maximum number of retries as desired
    retries = 0

    while retries < max_retries:
        try:
            # Encode the password using the algorithm
            encoded_password = encode_password(password, prime_modulus)

            # Set a breakpoint to pause the execution and start debugging
            pdb.set_trace()

            # Display the encoded password
            print("Encoded password:", encoded_password)

            # Decode the password using the algorithm
            decoded_password = decode_password(encoded_password, prime_modulus)

            # Display the decoded password
            print("Decoded password:", decoded_password)

            # Exit the loop if decoding is successful
            break
        except ValueError:
            # If the modular multiplicative inverse does not exist, generate a new prime modulus
            prime_modulus = generate_prime_modulus()
            retries += 1

    if retries == max_retries:
        print("Maximum number of retries reached. Decoding unsuccessful.")

# Run the main program
if __name__ == "__main__":
    main()

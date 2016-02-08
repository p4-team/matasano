import base64
import random
import string

from Crypto.Cipher import AES

key = "".join([chr(random.randint(0, 255)) for i in range(16)])


def decrypt_ecb(line, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(line)


def encrypt_ecb(line, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(line)


def blackbox_ecb_encrypt(data):
    secret = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
    decoded_secret = base64.b64decode(secret)
    input_data = data + decoded_secret
    padding = "\x00" * (16 - len(input_data) % 16)
    input_data += padding
    return encrypt_ecb(input_data, key)


def when_length_changed(init_data):
    added_len = 0
    ciphertext_len = len(blackbox_ecb_encrypt(init_data))
    while True:
        message = init_data + "\x00" * added_len
        new_ciphertext_len = len(blackbox_ecb_encrypt(message))
        if new_ciphertext_len != ciphertext_len:
            return added_len
        else:
            added_len += 1


def brute_block_len():
    first_change = when_length_changed("")
    second_change = when_length_changed("\x00" * first_change)
    return second_change


def brute_secret(block_len):
    secret_len = len(blackbox_ecb_encrypt(""))
    result = []
    bruting_block_number = secret_len / block_len - 1
    for i in range(1, secret_len + 1):
        data = "\x00" * (secret_len - i)
        encrypted = blackbox_ecb_encrypt(data)
        blocks = chunk(encrypted, block_len)
        reference_block = blocks[bruting_block_number]
        result.append(brute_character(data, result, bruting_block_number, reference_block))
    return "".join(result)


def brute_character(data, current_result, bruting_block_number, reference_block):
    for character in string.printable:
        brute_data = data + "".join(current_result) + character
        encrypted = blackbox_ecb_encrypt(brute_data)
        blocks = chunk(encrypted, block_len)
        result_block = blocks[bruting_block_number]
        if reference_block == result_block:
            print("found " + str(i) + " " + character)
            return character
    return "?"  # padding


def chunk(input_data, size):
    return [input_data[i * size:(i + 1) * size] for i in range(len(input_data) / size)]


if __name__ == "__main__":
    block_len = brute_block_len()
    print(block_len)
    recovered_secret = brute_secret(block_len)
    print(recovered_secret)

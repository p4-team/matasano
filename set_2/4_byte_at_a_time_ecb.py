import base64
import random
from Crypto.Cipher import AES


def decrypt_ecb(line, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(line)


def encrypt_ecb(line, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(line)


def blackbox_ecb_encrypt(data):
    key = "".join([chr(random.randint(0, 255)) for i in range(16)])
    secret = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK";
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
    return first_change, second_change


if __name__ == "__main__":
    filling_first_block, key_len = brute_block_len()
    print(filling_first_block, key_len)

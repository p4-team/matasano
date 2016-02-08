import random
import base64
import codecs
from random import randint

from Crypto.Cipher import AES


def random_bytes(n):
    return ''.join(chr(randint(0, 255)) for byte in range(n))


def random_aes_key():
    return random_bytes(16)


def xor(in1, in2):
    return "".join([chr(ord(x) ^ ord(y)) for x, y in zip(in1, in2)])


def decrypt_ecb(line, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(line)


def encrypt_ecb(line, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(line)


def chunk(input_data, size):
    return [input_data[i * size:(i + 1) * size] for i in range(len(input_data) / size)]


def decrypt_cbc(input_data, key, IV):
    result_blocks = []
    previous_block = IV
    for block in chunk(input_data, len(IV)):
        decrypted_ecb = decrypt_ecb(block, key)
        xored = xor(decrypted_ecb, previous_block)
        previous_block = block
        result_blocks.append(xored)
    return "".join(result_blocks)


def encrypt_cbc(input_data, key, IV):
    result_blocks = []
    previous_block = IV
    for block in chunk(input_data, len(IV)):
        xored = xor(block, previous_block)
        encrypted_ecb = encrypt_ecb(xored, key)
        previous_block = encrypted_ecb
        result_blocks.append(encrypted_ecb)
    return "".join(result_blocks)


def random_encrypt(data):
    prefix = random_bytes(randint(5, 10))
    suffix = random_bytes(randint(5, 10))
    key = random_bytes(16)
    if randint(0, 1):
        iv = random_bytes(16)
        return 'cbc', encrypt_cbc(data, key, iv)
    else:
        return 'ecb', encrypt_ecb(data, key)
    

def detect_encrypt_mode(blackbox):
    verify, ciphertext = blackbox('x'*(16*3))
    ch = chunk(ciphertext, 16)
    if len(set(ch)) == len(ch):
        result = 'cbc'
    else:
        result = 'ecb'
    assert result == verify
    return result


def test():
    for _ in range(10):
        print 'detected', detect_encrypt_mode(random_encrypt)


if __name__ == '__main__':
    test()

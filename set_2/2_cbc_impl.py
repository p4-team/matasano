import base64
import codecs

from Crypto.Cipher import AES


def xor(in1, in2):
    return "".join([chr(ord(x) ^ ord(y)) for x, y in zip(in1, in2)])


def decrypt_ecb(line):
    key = "YELLOW SUBMARINE"
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(line)


def encrypt(line):
    key = "YELLOW SUBMARINE"
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(line)


def chunk(input_data, size):
    return [input_data[i * size:(i + 1) * size] for i in range(len(input_data) / size)]


def decrypt_cbc(input_data, IV):
    result_blocks = [IV]
    for block in chunk(input_data, len(IV)):
        decrypted_ecb = decrypt_ecb(block)
        xored = xor(decrypted_ecb, result_blocks[-1])
        result_blocks.append(xored)
    return "".join(result_blocks)


with codecs.open("2.txt", "r") as input_file:
    text = "".join(input_file.read().splitlines())
    text = base64.b64decode(text)
    print(decrypt_cbc(text, "\x00" * 16))

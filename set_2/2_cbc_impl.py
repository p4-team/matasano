import base64
import codecs

from Crypto.Cipher import AES


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


if __name__ == "__main__":
    with codecs.open("2.txt", "r") as input_file:
        text = "".join(input_file.read().splitlines())
        text = base64.b64decode(text)
        key = "YELLOW SUBMARINE"
        print(decrypt_cbc(text, key, "\x00" * 16))
        test = encrypt_cbc("kotykotykotykoty", "keyskeyskeyskeys", "\x00" * 16)
        print(decrypt_cbc(test, "keyskeyskeyskeys", "\x00" * 16))

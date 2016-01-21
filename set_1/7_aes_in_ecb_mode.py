import base64
import codecs

from Crypto.Cipher import AES


def decrypt(line):
    key = "YELLOW SUBMARINE"
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(line)


with codecs.open("7.txt", "r") as input_file:
    text = "".join(input_file.read().splitlines())
    text = base64.b64decode(text)
    print(decrypt(text))

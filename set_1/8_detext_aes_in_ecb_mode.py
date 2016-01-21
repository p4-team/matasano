import codecs
from collections import defaultdict


def blocks(input_data):
    return [input_data[i * 16:(i + 1) * 16].encode("hex") for i in range(len(input_data) / 16)]


with codecs.open("8.txt", "r") as input_file:
    for index, line in enumerate(input_file.read().splitlines()):
        decoded = line.decode("hex")
        cipher_blocks = blocks(decoded)
        counter = defaultdict(int)
        for block in cipher_blocks:
            counter[block] += 1
        for key, value in counter.items():
            if value > 1:
                print(index, cipher_blocks)

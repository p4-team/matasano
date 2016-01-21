import codecs

import langdetect


def decrypt(line):
    x = line.decode("hex")
    for i in range(256):
        yield "".join(chr(ord(character) ^ i) for character in x)


def is_plaintext(data):
    return all(32 <= ord(c) <= 126 or c in '\r\n\t' for c in data)


def get_similarity_to_english(text):
    if ' ' not in text:
        return 0
    return next((lng for lng in langdetect.detect_langs(text) if lng.lang == 'en'), None)


def get_valid_score(decrypted):
    if is_plaintext(decrypted):
        return get_similarity_to_english(decrypted)
    else:
        return 0


with codecs.open("4.txt", "r") as input_file:
    matching = []
    for line in input_file.read().splitlines():
        for decrypted in decrypt(line):
            valid_score = get_valid_score(decrypted)
            if valid_score:
                matching.append((valid_score, decrypted))

    solutions = sorted(matching, key=lambda x: x[0], reverse=True)
    for solution, score in solutions[:200]:
        print solution, score

import langdetect

def is_plaintext(data):
    return all(32 <= ord(c) <= 126 for c in data)

def hamming(x, y):
    count, z = 0, int(x.encode('hex'),16) ^ int(y.encode('hex'),16)
    while z:
        if z & 1:
            count += 1
        z >>= 1
    return count

"""
compute index of coincidence of data
"""
def ioc(data, shift):
    r = 0
    for i in range(len(data) - shift):
        if data[i] == data[i + shift]:
            r += 1
    return r / float(len(data) - shift)

print hamming('this is a test', 'wokka wokka!!!')


def xor(a, b):
    return ''.join(chr(ord(ac) ^ ord(bc)) for ac, bc in zip(a, b))

def get_similarity_to_english(text):
    return next((lng.prob for lng in langdetect.detect_langs(text) if lng.lang == 'en'), None)

def decrypt_bruteforce(data):
    l = len(data)
    possible = []
    for byte in range(256):
        next = xor(data, chr(byte) * l)
        if is_plaintext(next):
            similarity = get_similarity_to_english(next)
            if similarity:
                possible.append((similarity, next))

    solutions = sorted(possible, reverse=True)
    for sln in solutions[:5]:
        print sln[0], sln[1]

def main():
    test_data = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
    print decrypt_bruteforce(test_data.decode('hex')) 

if __name__ == '__main__':
    main()

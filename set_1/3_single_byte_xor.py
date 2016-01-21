import langdetect

def is_plaintext(data):
    return all(32 <= ord(c) <= 126 for c in data)

def xor(a, b):
    return ''.join(chr(ord(ac) ^ ord(bc)) for ac, bc in zip(a, b))

def get_similarity_to_english(text):
    return next((lng for lng in langdetect.detect_langs(next) if lng.lang == 'en'), None)

def decrypt_bruteforce(data):
    l = len(data)
    possible = []
    for b in range(256):
        next = xor(data, chr(b) * l)
        if is_plaintext(next):
            similarity = get_similarity_to_english(next)
            if similarity:
                possible.append([next, similarity])

    solutions = sorted(possible, key=lambda x: x[1], reverse=True)
    for sln in solutions[:5]:
        print sln[1], sln[0]

def main():
    test_data = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
    print decrypt_bruteforce(test_data.decode('hex')) 

if __name__ == '__main__':
    main()

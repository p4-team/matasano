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

"""
find index of coincidence of data
"""
def ioc_test(data, upper=20):
    for i in range(1, upper):
        print i, " ==> ", (ioc(data, i) * 100), "%"

"""
find sources from which char can be xor'd
(pointless when charset is (0..255))
"""
def make_sources(charset):
    s = {}
    for a in charset:
        for b in charset:
            if (b < a):
                continue
            x = ord(a) ^ ord(b)
            if x not in s:
                s[x] = set()
            s[x] = set([a, b]) | s[x]
    return s

"""
get ordered array of best IoCs for data
"""
def get_best_ioc(data, upper=20):
    result = []
    for i in range(1, upper):
        result.append((ioc(data, i), i))
    return sorted(result, reverse=True)

"""
split stream to n substreams with every n-th byte - split_stream([1, 2, 3, 4, 6, 7, 8], 3) = [[1, 4], [2, 5], [3, 6]]
"""
def split_stream(data, by):
    s = []
    for i in range(by):
        s += [[]]
    for i in range(len(data)):
        s[i%by] += [data[i]]
    return s

"""
decode stream of bytes xored with the same byte
"""
def xor_decode(data, charset):
    possible = set(charset)
    sources = make_sources(charset)
    for d in data:
        s = sources[d]
        possible = possible & s
    return list(possible)

def default_decrypt(data):
    for iocValue, ioc in get_best_ioc(data):
        streams = split_stream(data, ioc)
        charset = map(chr, [9, 10, 13] + range(32, 127))
        for s in streams:
            print xor_decode(s, charset)
        break

data = open('6_data.txt').read().decode('base64')

default_decrypt([ord(c) for c in data])

print hamming('this is a test', 'wokka wokka!!!')


#def xor(a, b):
#    return ''.join(chr(ord(ac) ^ ord(bc)) for ac, bc in zip(a, b))
#
#def get_similarity_to_english(text):
#    return next((lng.prob for lng in langdetect.detect_langs(text) if lng.lang == 'en'), None)
#
#def decrypt_bruteforce(data):
#    l = len(data)
#    possible = []
#    for byte in range(256):
#        next = xor(data, chr(byte) * l)
#        if is_plaintext(next):
#            similarity = get_similarity_to_english(next)
#            if similarity:
#                possible.append((similarity, next))
#
#    solutions = sorted(possible, reverse=True)
#    for sln in solutions[:5]:
#        print sln[0], sln[1]

def main():
    test_data = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
    print decrypt_bruteforce(test_data.decode('hex')) 

if __name__ == '__main__':
    main()

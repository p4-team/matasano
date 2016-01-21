import langdetect
import string

def is_plaintext(data):
    return all(32 <= ord(c) <= 126 for c in data)

def xor(in1, in2):
    return "".join([chr(ord(x) ^ ord(y)) for x, y in zip(in1, in2)])

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


def xor_histogram_evaluate(data, byte):
    xored = xor(data, byte * len(data))
    result = 0
    for c in xored:
        if c in 'aeiou':
            result += 3
        elif c in string.ascii_lowercase:
            result += 2
        elif c in string.printable:
            result += 2
        else:
            result -= 500000
    return result

"""
decode stream of bytes xored with the same byte - guessing by histogram
"""
def xor_decode2(data):
    results = []
    for byte in range(256):
        results.append((xor_histogram_evaluate(data, chr(byte)), byte))
    return sorted(results, reverse=True)[0][1]
        

def default_decrypt(data):
    for iocValue, ioc in get_best_ioc(data):
        result = []
        streams = split_stream(data, ioc)
        #charset = map(chr, [9, 10, 13] + range(32, 127))
        for s in streams:
            result.append(xor_decode2(s))
        key = ''.join(chr(c) for c in result)
        print result
        print key
        print xor(data, key * len(data))

data = open('6_data.txt').read().decode('base64')

default_decrypt(data)

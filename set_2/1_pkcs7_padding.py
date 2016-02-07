def pkcs7pad(dat, n=16):
    pad_len = n - (len(dat) % n)
    if pad_len == 0:
        pad_len = n
    return dat + chr(pad_len) * pad_len
    

def test():
    assert pkcs7pad("YELLOW SUBMARINE", 20) == "YELLOW SUBMARINE\x04\x04\x04\x04"

if __name__ == '__main__':
    test()

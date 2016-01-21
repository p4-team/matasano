def xor(in1, in2):
    key=''
    while len(key)<len(in1):
      key+=in2
    key=key[:len(in1)]
    return "".join([chr(ord(x) ^ ord(y)) for x, y in zip(in1, key)])


def main():
    in1 = "Burning 'em, if you ain't quick and nimble".encode('hex').decode("hex")
    in2 = "ICE".encode("hex").decode("hex")
    result = xor(in1, in2)
    print(result)
    print(result.encode("hex"))


if __name__ == '__main__':
    main()
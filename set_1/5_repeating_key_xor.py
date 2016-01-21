def xor(in1, in2):
    while len(in2)<len(in1):
      in2+=in2
    return "".join([chr(ord(x) ^ ord(y)) for x, y in zip(in1, in2)])


def main():
    in1 = "Burning 'em, if you ain't quick and nimble"
    in2 = "ICE"
    result = xor(in1, in2)
    print(result)
    print(result.encode("hex"))


if __name__ == '__main__':
    main()
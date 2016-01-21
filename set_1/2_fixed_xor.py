def xor(in1, in2):
    return "".join([format(ord(x[0]) ^ ord(x[1]), "x") for x in zip(in1, in2)])


def main():
    in1 = "1c0111001f010100061a024b53535009181c".decode("hex")
    in2 = "686974207468652062756c6c277320657965".decode("hex")
    print(xor(in1, in2))


if __name__ == '__main__':
    main()

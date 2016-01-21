def hex_to_base64(data):
    return data.decode('hex').encode('base64')

def test():
    test_data = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
    print hex_to_base64(test_data) 

if __name__ == '__main__':
    test()

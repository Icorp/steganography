import numpy as np

def to_bin(data):
    """Convert `data` to binary format as string"""
    if isinstance(data, str):
        return ''.join([format(ord(i), "08b") for i in data])
    elif isinstance(data, bytes) or isinstance(data, np.ndarray):
        return [format(i, "08b") for i in data]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "08b")
    else:
        raise TypeError("Type not supported.")

secretValue = "this is secret message"
secretBit = to_bin(secretValue)
secretBitTest = "01110100011010000110100101110011001000000110100101110011001000000111001101100101011000110111001001100101011101000010000001101101011001010111001101110011011000010110011101100101"

if secretBit==secretBitTest:
    print("TestIsSuccess")

    
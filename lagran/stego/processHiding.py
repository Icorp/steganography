import numpy as np
import math
import image_slicer

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

def encode(coverImage, values):
    result = coverImage
    result[0][1] += values[0]
    result[1][0] += values[1]
    result[1][1] += values[2]
    return result


def decode(coverImage):
    b = []
    b.append(int(coverImage[0][1]-(coverImage[0][0]+coverImage[0][2])/2))
    b.append(int(coverImage[1][0]-(coverImage[0][0]+coverImage[2][0])/2))
    b.append(int(coverImage[1][1]-(coverImage[0][0]*2 +
                                   ((coverImage[0][2]+coverImage[2][0])/2))/3))
    return b


def calculateD(numbers):
    d = []
    for k in range(len(numbers)):
        if k != 0:
            d.append(numbers[k]-numbers[0])
    return d


def calculateN(d):
    n = []
    for k in range(len(d)):
        n.append(round(math.log2(d[k])))
    return n


def calculateB(n,binSecret):
    b = []
    prev = 0
    for k in range(len(n)):
        b.append(str(binSecret)[prev:prev+n[k]])
        prev = prev+n[k]
    return b


def getValues(b):
    values = []
    for k in range(len(b)): 
        values.append(int(b[k], 2))
    return values


secretValue = "this is secret message"
secretBit = to_bin(secretValue)
sizeSecret = len(secretBit)
image_slicer.slice('huge_test_image.png', 14)
print(sizeSecret)



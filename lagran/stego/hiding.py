from cv2 import phase
import numpy as np
import math


def to_bin(data):
    """Convert data to binary format as string"""
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
    cash = math.floor(((coverImage[0][0]*2 +(coverImage[0][2]+coverImage[2][0])/2))/3)
    b.append(int(coverImage[0][1]-(coverImage[0][0]+coverImage[0][2])/2))
    b.append(int(coverImage[1][0]-(coverImage[0][0]+coverImage[2][0])/2))
    b.append(int(coverImage[1][1]-cash))
    
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
        n.append(math.floor(math.log2(d[k])))
    return n


def calculateB(n):
    b = []
    prev = 0
    for k in range(len(n)):
        b.append(str(binSecret)[prev:prev+n[k]])
        print(n)
        print(b)
        exit()
        prev = prev+n[k]
    return b


def getValues(b):
    values = []
    for k in range(len(b)):
        values.append(int(b[k], 2))
    return values


coverImage = np.array(
    [[46, 79, 112],
     [128, 84, 101],
     [210, 150, 90]]
)
print("\nCoverImage: \n\n", coverImage)


secretMessage = 19225
binSecret = 1001101011000101
# binSecret = to_bin(secretMessage)
print(binSecret)

baseOpor = coverImage[0][0]
square = coverImage[0:2, 0:2]
numbers = square.flatten()

# start
d = calculateD(numbers)
n = calculateN(d)
b = calculateB(n)

values = getValues(b)
stegoImage = encode(coverImage, values)
repairSecret = decode(stegoImage)

print("\nStegoImage: \n\n", stegoImage)
print("\nSecret Values: \n\n", repairSecret)
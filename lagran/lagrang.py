import numpy as np
import cv2
import math
import time
from numpy.core.fromnumeric import shape
from numpy.lib.function_base import append


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


def calculateB(n, secretBin):
    b = []
    prev = 0
    for k in range(len(n)):
        b.append(str(secretBin)[prev:prev+n[k]])
        prev = prev+n[k]
    return b


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


def lagrang(c):
    xk = [1, 3]
    result = []
    result.append(c[0])
    result.append(xk[0])
    result.append(c[1])
    result.append(xk[1])
    result.append(c[2])

    for k in range(len(xk)):
        cash1 = c[0] * ((xk[k]-2)*(xk[k]-4))/8
        cash2 = c[1] * (xk[k]*(xk[k]-4))/-4
        cash3 = c[2] * (xk[k]*(xk[k]-2))/8
        ck = cash1 + cash2 + cash3
        result[xk[k]] = math.floor(ck)

        if ck > 255:
            result[xk[k]] = 255
        if ck < 0:
            result[xk[k]] = 255+math.floor(ck)
    return result


def getValues(b):
    values = []
    for k in range(len(b)):
        try:
            values.append(int(b[k], 2))
        except ValueError:
            pass
    return values


def split(a, n):
    def lol(lst, sz): return [lst[i:i+sz] for i in range(0, len(lst), sz)]
    return lol(a, n)


def makeInterpolation(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    iSize = gray[0].size

    rows = []
    if iSize % 3 == 0:
        for i in range(iSize):
            cashAllNumbers = []
            slices = split(gray[i], 3)

            for k in range(len(slices)):

                if len(slices[k]) != 3:
                    continue

                # Вычисление Лагранджа из 3 чисел в 5 чисел
                cash5Numbers = lagrang(slices[k])

                # добавляем в кеш
                for j in range(len(cash5Numbers)):
                    cashAllNumbers.append(cash5Numbers[j])

            rows.append(cashAllNumbers)

    finalResult = np.empty(shape=(len(rows[0]), len(rows[0])))

    rows = np.array(rows)
    newjSize = len(rows[0])
    
    for i in range(newjSize):

        cashAllNumbers = []
        slices = split(rows[:, i], 3)

        for k in range(len(slices)):

            if len(slices[k]) != 3:
                continue

            # Вычисление Лагранджа из 3 чисел в 5 чисел
            cash5Numbers = lagrang(slices[k])

            # добавляем в кеш
            for j in range(len(cash5Numbers)):
                cashAllNumbers.append([cash5Numbers[j]])
        print(np.shape(finalResult))
        print(np.shape(cashAllNumbers))
        exit()
        finalResult = np.append(finalResult, cashAllNumbers, axis=1)

    img = np.array(finalResult[:, newjSize:])
    return img


def processStego(coverImage, secretBits):
    lenI = math.ceil(len(coverImage)/2)
    lenJ = math.ceil(len(coverImage[0])/2)
    secretMessageFinishStatus = False

    # Разделил картинку по 2х2
    for i in range(lenI):

        if secretMessageFinishStatus == True:
            break

        for j in range(lenJ):

            if secretMessageFinishStatus == True:
                break

            # array 3x3
            block = coverImage[i*3:i*3+3, j*3:j*3+3]
            if len(block[0]) != 3:
                continue

            # array 2x2 from block
            square = block[0:2, 0:2]

            # array 2x2 convert to 1d ([0,1,2,3])
            squareInline = square.flatten()

            d = calculateD(squareInline)

            zeroValue = False
            # check on 0,0,0
            for k in range(len(d)):
                d[k] = math.ceil(d[k])
                if d[k] <= 0:
                    zeroValue = True

            if zeroValue == True:
                continue

            n = calculateN(d)

            partCount = 0
            # check on 0,0,0
            for k in range(len(n)):
                n[k] = math.ceil(n[k])
                partCount += n[k]
                if n[k] <= 0:
                    zeroValue = True

            if zeroValue == True:
                continue

            b = calculateB(n, secretBits[0:partCount])
            values = getValues(b)

            for k in range(len(b)):

                start = 0
                stop = len(b[k])

                # Remove charactes from index start to stop
                if len(secretBits) > stop:
                    secretBits = secretBits[0: start:] + secretBits[stop + 1::]
                elif len(secretBits) == 0:
                    secretMessageFinishStatus = True
            try:
                coverImage[i*3:i*3+3, j*3:j*3+3][0][1] += values[0]
                coverImage[i*3:i*3+3, j*3:j*3+3][1][0] += values[1]
                coverImage[i*3:i*3+3, j*3:j*3+3][1][1] += values[2]
            except:
                print("index_error, size(values) =", len(values))

    print("Success")
    return coverImage


def decode(blockCash):
    b = []
    cash = math.floor(
        ((blockCash[0][0]*2 + (blockCash[0][2]+blockCash[2][0])/2))/3)
    b.append(math.ceil(blockCash[0][1]-(blockCash[0][0]+blockCash[0][2])/2))
    b.append(math.ceil(blockCash[1][0]-(blockCash[0][0]+blockCash[2][0])/2))
    b.append(math.ceil(blockCash[1][1]-cash))

    return b


def processDecode(stegoImg):
    lenI = math.ceil(len(stegoImg)/2)
    lenJ = math.ceil(len(stegoImg[0])/2)
    secretMessageFinishStatus = False

    result = []

    # Разделил картинку по 2х2
    for i in range(lenI):

        if secretMessageFinishStatus == True:
            break

        for j in range(lenJ):

            if secretMessageFinishStatus == True:
                break

            # array 3x3
            block = stegoImg[i*3:i*3+3, j*3:j*3+3]

            try:
                if len(block[0]) != 3:
                    continue
            except IndexError:
                continue
                print("Block", block)
                print("Len", len(block))

            # array 2x2 from block
            square = block[0:2, 0:2]

            # array 2x2 convert to 1d ([0,1,2,3])
            squareInline = square.flatten()

            d = calculateD(squareInline)

            zeroValue = False
            # check on 0,0,0
            for k in range(len(d)):
                d[k] = math.ceil(d[k])
                if d[k] <= 0:
                    zeroValue = True

            if zeroValue == True:
                continue

            n = calculateN(d)

            partCount = 0

            # check on 0,0,0
            for k in range(len(n)):
                n[k] = math.ceil(n[k])
                partCount += n[k]
                if n[k] <= 0:
                    zeroValue = True

            if zeroValue == True:
                continue

            b = decode(block)

            for k in range(len(b)):
                if b[k] <= 0:
                    break
                b[k] = math.ceil(b[k])

            result = append(result, b)

    return result


# 1) Read image
image = cv2.imread("image.png")

# 2) Make Interpolation
coverImage = makeInterpolation(image)

# 3) Create secret message
# secretValue = 19225
# secretBit = to_bin(secretValue)
secretBit = '100110101011000101'
print(secretBit)
sizeSecret = len(secretBit)

coverImage = processStego(coverImage, secretBit)
result = processDecode(coverImage)

print(result)

# 3) Save image
print("Saving rusult...")
print(coverImage.shape)
cv2.imwrite("test.png", coverImage)


# 1) Проблема нулевого логарифма
# 2) Проблема остановки декодирования
# 3) Проблема раcшифровки
# 4)

import numpy as np
import cv2
import math
from numpy.core.defchararray import array


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


def split(a, n):
    def lol(lst, sz): return [lst[i:i+sz] for i in range(0, len(lst), sz)]
    return lol(a, n)


def makeInterpolation(array):

    iSize = array[0].size

    rows = []
    if iSize % 3 == 0:
        for i in range(iSize):
            cashAllNumbers = []
            slices = split(array[i], 3)

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

        finalResult = np.append(finalResult, cashAllNumbers, axis=1)

    img = np.array(finalResult[:, newjSize:])
    return img


data = np.array([[1, 2], [3, 4]])
result = makeInterpolation(data)
print(result)

from array import array
from hashlib import new
import math
import numpy as np
from scipy import ndimage


def interpolation(array):
    # Переменные для увелечения по cтолбцу (5х5) -> 10х5
    rows = []  # для конечного массива
    block = []  # Место для хранения блоков 3х
    columnRowLen, columnColumnLen = np.shape(array)
    i = 0  # для итерации
    j = 0  # для итерации

    # Увелечили из 5х5 в 10х5
    while columnColumnLen > i:
        cashRow = []

        while columnRowLen > j:
            block.append(array[i][j])

            # print("i = ", i, "j = ", j)
            # print("block append", block)

            # calculate lagrang and clean block
            if len(block) == 5:

                firstPart = [block[0], block[1], block[2]]
                secondPart = [block[2], block[3], block[4]]

                # add to row result
                for k, value in enumerate(lagrang(firstPart)):
                    cashRow.append(value)

                # add to row result
                for k, value in enumerate(lagrang(secondPart)):
                    cashRow.append(value)

                block = []

            # clean read array
            j = j + 1

        rows.append(cashRow)
        cashRow = []
        j = 0
        i += 1

    # Переменные для увелечения по cтолбцу (10х5) -> 10х10
    columnRowLen, columnColumnLen = np.shape(rows)
    matrix = []  # финальная матрица
    block = []  # место для хранения
    i = 0  # для итерации
    j = 0  # для итерации

    # Увелечили из 5х5 в 10х5
    while columnColumnLen > i:
        cashRow = []

        columnValues = [x[i] for x in rows]  # это числа столбцов
        while len(columnValues) > j:
            block.append(rows[j][i])

            # print("i = ", i, "j = ", j)
            # print("block append", block)

            # calculate lagrang and clean block
            if len(block) == 5:
                # print("Block:", block)
                # print("\n")
                firstPart = [block[0], block[1], block[2]]
                secondPart = [block[2], block[3], block[4]]

                # add to final result
                for k, value in enumerate(lagrang(firstPart)):
                    cashRow.append(value)

                # add to final result
                for k, value in enumerate(lagrang(secondPart)):
                    cashRow.append(value)

                block = []

            # clean read array
            j = j + 1

        matrix.append(cashRow)
        cashRow = []
        j = 0
        i += 1

    rotated = ndimage.rotate(np.array(matrix), 270)
    im = np.fliplr(rotated)
    return im


def calculateD(numbers):
    d = []
    # Проверка на опорную если он больше всех

    for k in range(len(numbers)):
        if k != 0:
            if numbers[k] > numbers[0]:
                d.append(numbers[k]-numbers[0])
            else:
                d.append(0)
    return d


def calculateN(d):
    n = []
    for k in range(len(d)):
        n.append(math.floor(math.log2(d[k])))
    return n


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


def mutation():
    maxValue = 0
    maxPixel = 255

    for j in range(100000000):
        zeroValue = False  # переменная для статуса нулевых значении
        randData = np.random.randint(1, 255, size=(5, 5))
        interData = interpolation(randData)
        block = interData[0:2, 0:2]
        newDataInline = block.flatten()
        dValues = calculateD(newDataInline)

        # Проверяем если все  3 значения равны нулю, значит ничего сюда не поместится
        for k in range(len(dValues)):
            dValues[k] = math.ceil(dValues[k])
            if dValues[k] <= 0:
                zeroValue = True

            # Пропускаем блок 2х2 и переходим к следующему
        if zeroValue == True:
            continue

        nValues = calculateN(dValues)
        value = sum(nValues)

        if value > maxValue:
            print("\n\n")
            print(f"{value} is more than {maxValue}")
            print("GeneratedData:\n ",interData[0:3, 0:3] )
            print("d - dvalues: ", dValues)
            print("n - values: ", nValues)
            maxValue = value

        randData = []


def findMax(data):
    return data[1]+data[3]


# start
mutation()

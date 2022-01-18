import numpy as np
import math
from PIL import Image


def split(a, n):
    def lol(lst, sz): return [lst[i:i+sz] for i in range(0, len(lst), sz)]
    return lol(a, n)


def lagrang(array):
    xk = [1, 3]
    result = []
    result.append(array[0])
    result.append(xk[0])
    result.append(array[1])
    result.append(xk[1])
    result.append(array[2])

    for k in range(len(xk)):
        cash1 = array[0] * ((xk[k]-2)*(xk[k]-4))/8
        cash2 = array[1] * (xk[k]*(xk[k]-4))/-4
        cash3 = array[2] * (xk[k]*(xk[k]-2))/8
        ck = cash1 + cash2 + cash3
        result[xk[k]] = math.floor(ck)
        if ck > 255:
            result[xk[k]] = 255
        if ck < 0:
            result[xk[k]] = 0
    return result


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
            if len(block) == 3:
                # print("Block:", block)
                # print("\n")

                # add to final result
                for k, value in enumerate(lagrang(block)):
                    cashRow.append(value)

                block = []

                # Проверка на последнюю итерацию
                if len(array[0])-1 != j:
                    j = j-1

            # clean read array
            j = j + 1

        rows.append(cashRow)
        cashRow = []
        j = 0
        i += 1
    
    # Переменные для увелечения по cтолбцу (10х5) -> 10х10
    columnRowLen, columnColumnLen = np.shape(rows)
    matrix = []  # финальная матрица
    block = [] # место для хранения
    i = 0 # для итерации 
    j = 0 # для итерации
    

    # Увелечили из 5х5 в 10х5
    while columnColumnLen > i:
        cashRow = []

        columnValues = [x[i] for x in rows]  # это числа столбцов
        while len(columnValues) > j:
            block.append(rows[j][i])

            # print("i = ", i, "j = ", j)
            # print("block append", block)

            # calculate lagrang and clean block
            if len(block) == 3:
                # print("Block:", block)
                # print("\n")

                # add to final result
                for k, value in enumerate(lagrang(block)):
                    cashRow.append(value)

                block = []

                # Проверка на последнюю итерацию
                if len(array[0])-1 != j:
                    j = j-1

            # clean read array
            j = j + 1

        matrix.append(cashRow)
        cashRow = []
        j = 0
        i += 1

    return np.array(matrix)


x = np.array([[1, 2, 3, 4, 5],
             [1, 2, 3, 4, 5],
             [1, 2, 3, 4, 5],
             [1, 2, 3, 4, 5],
             [1, 2, 3, 4, 5]])
x2 = np.array(interpolation(x))


# Save array as file ...
im = Image.fromarray(x2)
im.save("test_code.png")

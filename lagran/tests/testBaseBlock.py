import numpy as np
import math
from numpy.core.defchararray import array
from scipy import ndimage


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

    # rotation angle in degree
    rotated = ndimage.rotate(np.array(matrix), 270)
    im =  np.fliplr(rotated)
    return im


data = np.array([
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]])

x2 = interpolation(data)

def getBase(array):
    
    # first block
    firstBlock = []
    for k, v in enumerate(array[0:5, 0:5]):
        cash = []
        if k % 2 == 0:
            for i, j in enumerate(v):
                if i % 2 == 0:
                    cash.append(j)
            firstBlock.append(cash)
        cash = []
    
    # second block 
    secondBlock = []
    for k, v in enumerate(array[0:5, 5:10]):
        cash = []
        if k % 2 == 0:
            for i, j in enumerate(v):
                if i % 2 == 0:
                    cash.append(j)
            secondBlock.append(cash)
        cash = []

    # third block
    thirdBlock = []
    for k, v in enumerate(array[5:10, 0:5]):
        cash = []
        if k % 2 == 0:
            for i, j in enumerate(v):
                if i % 2 == 0:
                    cash.append(j)
            thirdBlock.append(cash)
        cash = []
    
    # fourth block 
    fourthBlock = []
    for k, v in enumerate(array[5:10, 5:10]):
        cash = []
        if k % 2 == 0:
            for i, j in enumerate(v):
                if i % 2 == 0:
                    cash.append(j)
            fourthBlock.append(cash)
        cash = []

    firstBlock = np.delete(firstBlock, 2, axis=1)
    thirdBlock = np.delete(thirdBlock, 2, axis=1)

    highBlock = np.concatenate((firstBlock, secondBlock),axis=1)
    lowBlock = np.concatenate((firstBlock, fourthBlock),axis=1)

    highBlock = np.delete(highBlock, 1, 0)
    block = np.concatenate((highBlock, lowBlock),axis=0)
    return np.array(block)

def getBaseImage(array):
    lenI = math.ceil(len(array)/10)
    lenJ = math.ceil(len(array[0])/10)
    baseImage = np.array([[]])
    
    for i in range(lenI):
        
        # just for init, dump values todo: beautify
        cashRow = np.array([
            [1,2,3],
            [1,2,3],
            [1,2,3],
            [1,2,3],
            [1,2,3]])

        for j in range(lenJ):
            
            forBaseBlock = array[i*10:i*10+10, j*10:j*10+10]
            baseBlock = getBase(forBaseBlock)
            
            if j == 0:
                cashRow = baseBlock
            else:
                cashRow = np.concatenate((cashRow, baseBlock),axis=1)
        
        if i == 0:
            baseImage = cashRow    
        else:
            baseImage = np.concatenate((baseImage, cashRow),axis=0)
        print(np.shape(baseImage))
   
    return baseImage


result = getBaseImage(x2)
print(result)
print(np.shape(result))
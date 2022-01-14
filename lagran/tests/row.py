from typing import final
import numpy as np
import cv2
import math
from numpy.core.fromnumeric import shape
from numpy.lib.function_base import append

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

def makeInterpolation(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    iSize = gray[0].size

    rows = []
    if iSize % 3 == 0:
        for i in range(iSize):
            cashAllNumbers = []
            slices = split(gray[i], wanted_parts=int(iSize/3))
            slices = []

            for k in range(len(gray[i])):
                if k % 2 == 0 or k == 0:
                    slices.append(gray[i][k:k+3])
                else:
                    continue

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
        slices = split(rows[:, i], wanted_parts=int(len(rows[0])/3))

        for k in range(len(rows[:, i])):
            if k % 2 != 0 or k == 0:
                slices.append(rows[:, i][k:k+3])
            else:
                continue

        for k in range(len(slices)):
            
            if len(slices[k]) != 3:
                continue

            # Вычисление Лагранджа из 3 чисел в 5 чисел
            cash5Numbers = lagrang(slices[k])
            
            # добавляем в кеш
            for j in range(len(cash5Numbers)):
                cashAllNumbers.append([cash5Numbers[j]])
            
        finalResult = np.append(finalResult, cashAllNumbers, axis=1)

    img = np.array(finalResult[:,newjSize:])
    return img

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
            result[xk[k]] = 255-math.floor(ck)
        if ck < 0:
            result[xk[k]] = 255+math.floor(ck)
    return result

# 1) Read image
image = cv2.imread("image.png")

# 2) Make Interpolation
finalImg = makeInterpolation(image)

# 3) Save image
print("Saving rusult...")
print(finalImg.shape)
cv2.imwrite("test.png", finalImg)


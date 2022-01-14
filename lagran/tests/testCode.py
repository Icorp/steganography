import numpy as np
import math
from PIL import Image


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


x = np.array([[1, 2, 3, 4, 5],
             [1, 2, 3, 4, 5],
             [1, 2, 3, 4, 5],
             [1, 2, 3, 4, 5],
             [1, 2, 3, 4, 5]])

result = []

block = []
i = 0
j = 0

while len(x) > i:
    cashRow = []

    while len(x[0]) > j:
        block.append(x[i][j])
        
        print("i = ", i, "j = ", j)
        print("block append", block)
        
        # calculate lagrang and clean block
        if len(block) == 3:
            print("Block:", block)
            print("\n")

            # add to final result
            for k, value in enumerate(lagrangV2(block)):
                cashRow.append(value)

            block = []

            # Проверка на последнюю итерацию
            if len(x[0])-1 != j:
                j = j-1

        # clean read array
        j = j + 1

    result.append(cashRow)
    cashRow = []
    j = 0
    i += 1

# Convert to np array
finalResult = np.array(result)

print("Финальный результат: \n", finalResult)
im = Image.fromarray(finalResult)
im.save("your_file.png")


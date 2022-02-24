from dataclasses import dataclass
import numpy as np
import math
import cv2
import copy as cp
from scipy import ndimage


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'


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


def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(
        image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
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


# Получает сколько битов можно отрезать
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


def getValues(b):
    values = []
    for k in range(len(b)):
        try:
            values.append(int(b[k], 2))
        except ValueError:
            values.append(0)
    return values


def decode(blockCash):
    b = []
    cash1 = math.floor((blockCash[0][0]+blockCash[0][2])/2)
    cash2 = math.floor((blockCash[0][0]+blockCash[2][0])/2)

    cash31 = math.floor((blockCash[0][2]+blockCash[2][0])/2)
    cash3 = math.floor(
        (math.floor(blockCash[0][0]*2 + cash31))/3)

    b.append(blockCash[0][1]-cash1)
    b.append(blockCash[1][0]-cash2)
    b.append(blockCash[1][1]-cash3)
    print("decode:")
    print(blockCash[0][1], "— (", blockCash[0][0],
          "+", blockCash[0][2], ")/2 =", b[0])
    print(blockCash[1][0], "— (", blockCash[0][0],
          "+", blockCash[2][0], ")/2 =", b[1])
    print(blockCash[1][1], "— (", blockCash[0][0], "* 2", "+(",
          blockCash[0][2], "+", blockCash[2][0], ")/2)/3 =", b[2])
    return b

def processStego(coverImage, secretBits):
    lenI = math.ceil(len(coverImage)/5)
    lenJ = math.ceil(len(coverImage[0])/5)
    copyOfSecretBits = cp.copy(secretBits)
    sizeSecret = format(len(copyOfSecretBits), '08b')    # длина секретного сообщения
    secretBits = sizeSecret+secretBits

    print("Начало внедрения")
    print("Длина секретного сообщения", len(secretBits))
    print("Длина секретного сообщения в битах", sizeSecret)
    print("Биты", copyOfSecretBits)
    print("Биты с размером секретного сообщения", secretBits)
    #   size 8 bit  011100110110010101100011011100100110010101110100
    #    00110000 + 011100110110010101100011011100100110010101110100

    # Статус для остановки процесса внедрения
    secretMessageFinishStatus = False

    for i in range(lenI):

        if secretMessageFinishStatus == True:
            break

        for j in range(lenJ):

            if secretMessageFinishStatus == True:
                break

            if secretBits == '':
                secretMessageFinishStatus = True
                break

            # array 3x3
            coverBlock = coverImage[i*5:i*5+5, j*5:j*5+5]

            block = coverBlock[0:3, 0:3]

            r, c = np.shape(block)
            if r != 3:
                continue

            if c != 3:
                continue

            # print("Block: \n")
            # print(block, "\n")

            # array 2x2 from block
            square = block[0:2, 0:2]

            # array 2x2 convert to 1d ([0,1,2,3])
            squareInline = square.flatten()
            # print("SquereInLine: ", squareInline)

            # Вычитываем пиксели
            d = calculateD(squareInline)

            zeroValue = False  # переменная для статуса нулевых значении

            # Проверяем если все  3 значения равны нулю, значит ничего сюда не поместится
            for k in range(len(d)):
                d[k] = math.ceil(d[k])
                if d[k] <= 0:
                    zeroValue = True
            
            # Пропускаем блок 2х2 и переходим к следующему
            if zeroValue == True:
                # print(bcolors.WARNING + "Warning: Один из d-значении равен нулю, пропускаю данный блок" + bcolors.ENDC)
                # print("\n")
                # print(block)
                # print("\n")
                continue

            # Вычитываем по сколько бит можно отрезать
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
            
            # Делим биты на части
            b = calculateB(n, secretBits[0:partCount])
            
            
            values = getValues(b)
            
            # Получаем числа которые нужно добавить в блок
            firstPlace = coverImage[i*5:i*5 + 5, j*5:j*5+5][0][1] + values[0]
            secondPlace = coverImage[i*5:i*5 + 5, j*5:j*5+5][1][0] + values[1]
            thirdPlace = coverImage[i*5:i*5 + 5, j*5:j*5+5][1][1] + values[2]
            
            if len(secretBits)>6:
                if b[0] == '':
                    break

                if b[1] == '':
                    break

                if b[2] == '':
                    break
            # print(firstPlace, secondPlace, thirdPlace)

            print("\nПроцесс: ", i, j)
            print("SecretBITS", secretBits)
            print("\td значения - ", d)
            print("\tn значения - ", n)
            print("\tb значения - ", b)
            print("\tvalues: ", values)

            # Проверки на перезаполнение
            if firstPlace > 255:
                # Пропускаем блок считая его недостаточным

                print("Переполнение в i =  ", i)
                print("Переполнение в j =  ", j)
                print('Значение ', firstPlace)
                break
                firstPlace = 255
                print("\n")
            if secondPlace > 255:
                # Пропускаем блок считая его недостаточным

                print("Переполнение в i =  ", i)
                print("Переполнение в j =  ", j)
                print('Значение ', secondPlace)
                break
                secondPlace = 255
                print("\n")
            if thirdPlace > 255:
                # Пропускаем блок считая его недостаточным

                print("Переполнение в i =  ", i)
                print("Переполнение в j =  ", j)
                print('Значение ', thirdPlace)
                break
                thirdPlace = 255
                print("\n")

            print("\nДо внедрения:\n", coverBlock)

            coverImage[i*5:i*5+5, j*5:j*5+5][0][1] = firstPlace
            coverImage[i*5:i*5+5, j*5:j*5+5][1][0] = secondPlace
            coverImage[i*5:i*5+5, j*5:j*5+5][1][1] = thirdPlace

            print("\nПосле внедрения:\n", coverImage[i*5:i*5+5, j*5:j*5+5])

            # Вычитываем биты которые были добавлены
            for k in range(len(b)):

                start = 0
                stop = len(b[k])-1

                # Remove charactes from index start to stop
                if len(secretBits) > stop:
                    secretBits = secretBits[0: start:] + secretBits[stop + 1::]
                elif len(secretBits) == 0:
                    secretMessageFinishStatus = True

    if secretMessageFinishStatus != True:
        print("Размер битов секретного сообщения", secretBits)
        print("Не достаточно место для встраивания секретного сообщения, биты:", secretBits)
        exit()
    print(f"{bcolors.WARNING}Процесс внедрения прошел успешно ...\n{bcolors.ENDC}")
    return coverImage

# Не нужная хрень


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

    highBlock = np.concatenate((firstBlock, secondBlock), axis=1)
    lowBlock = np.concatenate((firstBlock, fourthBlock), axis=1)

    highBlock = np.delete(highBlock, 1, 0)
    block = np.concatenate((highBlock, lowBlock), axis=0)
    return np.array(block)

# Не нужная хрень


def getBaseImage(array):
    lenI = math.ceil(len(array)/10)
    lenJ = math.ceil(len(array[0])/10)
    baseImage = np.array([[]])

    for i in range(lenI):

        # just for init, dump values todo: beautify
        cashRow = np.array([
            [1, 2, 3],
            [1, 2, 3],
            [1, 2, 3],
            [1, 2, 3],
            [1, 2, 3]])

        for j in range(lenJ):

            forBaseBlock = array[i*10:i*10+10, j*10:j*10+10]
            baseBlock = getBase(forBaseBlock)

            if j == 0:
                cashRow = baseBlock
            else:
                cashRow = np.concatenate((cashRow, baseBlock), axis=1)

        if i == 0:
            baseImage = cashRow
        else:
            baseImage = np.concatenate((baseImage, cashRow), axis=0)

    return baseImage

    lenI = math.ceil(len(stegoImage)/10)
    lenJ = math.ceil(len(stegoImage[0])/10)
    baseImage = np.array([[]])
    for i in range(lenI):

        # just for init, dump values todo: beautify
        cashRow = np.array([
            [1, 2, 3],
            [1, 2, 3],
            [1, 2, 3]])

        for j in range(lenJ):
            # array 3x3
            forBaseBlock = stegoImage[i*10:i*10+5, j*10:j*10+10]
            baseBlock = getBase(forBaseBlock)

            if j == 0:
                cashRow = baseBlock
            else:
                cashRow = np.concatenate((cashRow, baseBlock), axis=1)

        if i == 0:
            baseImage = cashRow
        else:
            baseImage = np.concatenate((baseImage, cashRow), axis=0)
        print(np.shape(baseImage))

    exit("exit")


def processDecode(stegoImage):
    lenI = math.ceil(len(stegoImage)/5)
    lenJ = math.ceil(len(stegoImage[0])/5)

    # Результат восстановления
    secretBits = ""
    sizeToStop = 0
    valueToStopDecode = False

    for i in range(lenI):

        # Выйти из цикла  если нашли конец сообщения
        if valueToStopDecode == True and len(secretBits) >= sizeToStop:
            break

        for j in range(lenJ):

            # Вычислить размер секретного сообщения
            if len(secretBits) >= 8 and valueToStopDecode == False:
                # 00110000
                sizeToStop = int(secretBits[0:8], 2)+8
                print("Size to stop:", sizeToStop)
                valueToStopDecode = True

            # Выйти из цикла  если нашли конец сообщения
            if valueToStopDecode == True and len(secretBits) >= sizeToStop:
                break

            # Для вывода в консоль
            blockForLog = cp.copy(stegoImage[i*5:i*5+5, j*5:j*5+5])

            # Block 5x5
            stegoBlock = stegoImage[i*5:i*5+5, j*5:j*5+5]
            block = stegoBlock[0:3, 0:3]

            r, c = np.shape(block)
            if r != 3:
                continue

            if c != 3:
                continue

            # array 2x2 from block
            square = block[0:2, 0:2]

            # array 2x2 convert to 1d ([0,1,2,3])
            squareInline = square.flatten()
            # print("SquereInLine: ", squareInline)

            # Вычитываем пиксели
            d = calculateD(squareInline)

            zeroValue = False  # переменная для статуса нулевых значении

            # Проверяем если все  3 значения равны нулю, значит ничего сюда не поместится
            for k in range(len(d)):
                d[k] = math.ceil(d[k])
                if d[k] <= 0:
                    zeroValue = True

            # Пропускаем блок 5x5 и переходим к следующему
            if zeroValue == True:
                # print(bcolors.WARNING + "Warning: Один из d-значении равен нулю, пропускаю данный блок" + bcolors.ENDC)
                # print("\n")
                # print(block)
                # print("\n")
                continue

            # Вычитываем по сколько бит можно отрезать
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

            firstCode = [stegoBlock[0][0], stegoBlock[0][2], stegoBlock[0][4]]

            # Вычисляем лагранж  между битами
            firstCodeLagrang = lagrang(firstCode)

            values = [0, 0, 0]

            # Если есть разница между лагранжем, то вычитаем значения
            if stegoBlock[0][1] != firstCodeLagrang[1]:
                values[0] = stegoBlock[0][1]-firstCodeLagrang[1]
                stegoBlock[0][1] = firstCodeLagrang[1]

            secondCode = [stegoBlock[0][0], stegoBlock[2][0], stegoBlock[4][0]]
            thirdCode = [stegoBlock[0][1], stegoBlock[2][1], stegoBlock[4][1]]

            secondCodeLagrang = lagrang(secondCode)
            thirdCodeLagrang = lagrang(thirdCode)

            if stegoBlock[1][0] != secondCodeLagrang[1]:
                values[1] = stegoBlock[1][0]-secondCodeLagrang[1]
                stegoBlock[1][0] = secondCodeLagrang[1]

            if stegoBlock[1][1] != thirdCodeLagrang[1]:
                values[2] = stegoBlock[1][1]-thirdCodeLagrang[1]
                stegoBlock[1][1] = thirdCodeLagrang[1]

            if blockForLog[1][1]-thirdCodeLagrang[1] < 0:

                thirdCode = [blockForLog[1][0],
                             blockForLog[1][2], blockForLog[1][4]]
                thirdCodeLagrang = lagrang(thirdCode)

                print("\nTry another way, horizontal")
                print("thirdRow: ", thirdCodeLagrang)
                print(blockForLog[1][1], "!=", thirdCodeLagrang[1],
                      "Output = ", blockForLog[1][1]-thirdCodeLagrang[1])
                values[2] = blockForLog[1][1]-thirdCodeLagrang[1]

            bits = [format(values[0], 'b'), format(
                values[1], 'b'), format(values[2], 'b')]

            # Заново проверяем блок для нахождения d и n значения, количество битов
            # array 2x2 from block
            square = stegoBlock[0:2, 0:2]

            # array 2x2 convert to 1d ([0,1,2,3])
            squareInline = square.flatten()
            # print("SquereInLine: ", squareInline)

            # Вычитываем пиксели
            d = calculateD(squareInline)

            # Вычитываем по сколько бит можно отрезать
            n = calculateN(d)

            # Оптимизировать эту хрень с условиями
            # Добавляем 0 дополнительные биты
            if values[0] == 0 and n[0] > 1:
                for k in range(n[0]-1):
                    bits[0] += "0"

            # Добавляем 0 дополнительные биты
            if values[1] == 0 and n[1] > 1:
                for k in range(n[1]-1):
                    bits[1] += "0"

            # Добавляем 0 дополнительные биты
            if values[2] == 0 and n[2] > 1:
                for k in range(n[2]-1):
                    bits[2] += "0"

            # Добавляем 0 дополнительные биты перед еденицой
            if bits[0][0] == "1" and len(bits[0]) < n[0]:
                cash = "0"

                for k in range(len(bits[0])):
                    cash += bits[0][k]

                bits[0] = cash

            # Добавляем 0 дополнительные биты перед еденицой
            if bits[1][0] == "1" and len(bits[1]) < n[1]:
                cash = "0"

                for k in range(len(bits[1])):
                    cash += bits[1][k]

                bits[1] = cash

            # Добавляем 0 дополнительные биты перед еденицой
            if bits[2][0] == "1" and len(bits[2]) < n[2]:
                cash = "0"

                for k in range(len(bits[2])):
                    cash += bits[2][k]

                bits[2] = cash

            if len(bits[0]) < n[0]:
                cash = ''
                for k in range(n[0]-len(bits[0])):
                    cash += "0"
                bits[0] = cash + bits[0]

            if len(bits[1]) < n[1]:
                cash = ''
                for k in range(n[1]-len(bits[1])):
                    cash += "0"
                bits[1] = cash + bits[1]

            if len(bits[2]) < n[2]:
                cash = ''
                for k in range(n[2]-len(bits[2])):
                    cash += "0"
                bits[2] = cash + bits[2]

            print("\nПРОЦЕСС: ", i, j, "\n")

            print(blockForLog)
            print("\n")
            print(blockForLog[0][1], "!=", firstCodeLagrang[1],
                  "Output = ", blockForLog[0][1] - firstCodeLagrang[1])
            print(blockForLog[1][0], "!=", secondCodeLagrang[1],
                  "Output = ", blockForLog[1][0] - secondCodeLagrang[1])
            print(blockForLog[1][1], "!=", thirdCodeLagrang[1],
                  "Output = ", blockForLog[1][1]-thirdCodeLagrang[1])
            print("\n")
            print("firstRow: ", firstCodeLagrang)
            print("secondRow: ", secondCodeLagrang)
            print("thirdRow: ", thirdCodeLagrang)
            print("values: ", values)

            print("\nn - значения", n)
            print("\nd - значения", d)
            print("bits: ", bits)

            for k in range(len(values)):
                secretBits += bits[k]

            # для дебага
            # if j == 123:
            #     exit()

    if secretBits == "":
        print("В изображении нет секрета или что-то пошло не так ...")
        exit()

    print("Декодирование прошла успешна")

    print("Секрет: ", secretBits[8:sizeToStop])
    print("Секрет: ", text_from_bits(
        secretBits[8:sizeToStop], errors='surrogatepass'))
    return secretBits


secretMessage = 'secret'
# 01110100011001010111001101110100001000000110000101101110011001000010000001110100011001010111001101110100
# 01101000 01110100011001010111001101110100001000000110000101101110011001000010000001110100011001010111001101110100
#                                                                    0000001110100011001010111001101110100

secretMessageInBit = "01001001011011100111010001100101011100100111001101110100011001010110110001101100011000010111001000100000010101010110110001110100011010010110110101100001011101000110010100100000010000110111010101110100"

image = cv2.imread("images/space_500x500.png")

# to grayScale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
grayImage = np.array(gray)

# Производим интерполяцию
x2 = np.array(interpolation(gray))

# Производим внедрение секретных  данных в изображение
stegoImage = processStego(x2, secretMessageInBit)

# Сохраняем стегоизображение как файл
cv2.imwrite("stego.png", stegoImage)

result = processDecode(stegoImage)

import numpy as np
import math
import cv2


# Числа для битов
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
            pass
    return values


def processStego(coverImage, secretBits):
    lenI = math.ceil(len(coverImage)/2)
    lenJ = math.ceil(len(coverImage[0])/2)

    # Статус для остановки процесса внедрения
    secretMessageFinishStatus = False

    # Разделил картинку по 2х2
    for i in range(lenI):

        if secretMessageFinishStatus == True:
            break

        for j in range(lenJ):

            if secretMessageFinishStatus == True:
                break
            if secretBits == '':
                secretMessageFinishStatus = True

            # array 3x3
            block = coverImage[i*3:i*3+3, j*3:j*3+3]

            r, c = np.shape(block)
            if r != 3:
                continue

            if c != 3:
                continue

            # print("Процесс: ", i, j)
            # print("Block: \n")
            # print(block, "\n")

            # array 2x2 from block
            square = block[0:2, 0:2]

            # array 2x2 convert to 1d ([0,1,2,3])
            squareInline = square.flatten()
            # print("SquereInLine: ", squareInline)

            # Вычитываем пиксели
            d = calculateD(squareInline)
            # print("D: ", d)

            zeroValue = False  # переменная для статуса нулевых значении

            # Проверяем если все  3 значения равны нулю, значит ничего сюда не поместится
            for k in range(len(d)):
                d[k] = math.ceil(d[k])
                if d[k] <= 0:
                    zeroValue = True

            # Пропускаем блок 2х2 и переходим к следующему
            if zeroValue == True:
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
            print(b)

            # Получаем числа которые нужно добавить в блок
            values = getValues(b)
            print("values: ", values)
            if b[0] != '':
                firstPlace = coverImage[i*3:i*3+3, j*3:j*3+3][0][1] + values[0]
            else:
                break

            if b[1] != '':
                secondPlace = coverImage[i*3:i*3 +
                                         3, j*3:j*3+3][1][0] + values[1]
            else:
                break

            if b[2] != '':
                thirdPlace = coverImage[i*3:i*3+3, j*3:j*3+3][1][1] + values[2]
            else:
                break
            # print(firstPlace, secondPlace, thirdPlace)

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

            print("\nДо внедрения:\n", block)

            coverImage[i*3:i*3+3, j*3:j*3+3][0][1] = firstPlace
            coverImage[i*3:i*3+3, j*3:j*3+3][1][0] = secondPlace
            coverImage[i*3:i*3+3, j*3:j*3+3][1][1] = thirdPlace

            print("\nПосле внедрения:\n", coverImage[i*3:i*3+3, j*3:j*3+3])

            print(secretBits[0:partCount])
            print(n)

            # Вычитываем биты которые были добавлены
            for k in range(len(b)):

                start = 0
                stop = len(b[k])

                # Remove charactes from index start to stop
                if len(secretBits) > stop:
                    secretBits = secretBits[0: start:] + secretBits[stop + 1::]
                elif len(secretBits) == 0:
                    secretMessageFinishStatus = True

    if secretMessageFinishStatus != True:
        print("Размер битов секретного сообщения", secretBits)
        print("Не достаточно место для встраивания секретного сообщения, биты:", secretBits)
        exit()

    print("\n Процесс внедрения прошел успешно ...")
    return coverImage


secretMessage = 'secret'

# 01110011 01100101 01100011 01110010 01100101 01110100
secretMessageInBit = "011100110110010101100011011100100110010101110100"

image = cv2.imread("test.png")
print(image.shape)

# to grayScale
grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
grayImage = np.array(grayImage)

result = processStego(grayImage, secretMessageInBit)

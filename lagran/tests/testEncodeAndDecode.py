import numpy as np
import math
import cv2

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


def decode(blockCash):
    b = []
    cash1 = math.floor((blockCash[0][0]+blockCash[2][0])/2)
    cash2 = math.floor(blockCash[0][0]+blockCash[0][2]/2)
    cash3 = math.floor(
        ((blockCash[0][0]*2 + (blockCash[0][2]+blockCash[2][0])/2))/3)

    b.append(blockCash[0][1]-cash1)
    b.append(blockCash[1][0]-cash2)
    b.append(blockCash[1][1]-cash3)
    print(b)
    return b


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
                break

            # array 3x3
            block = coverImage[i*3:i*3+3, j*3:j*3+3]

            r, c = np.shape(block)
            if r != 3:
                continue

            if c != 3:
                continue

            print("\nПроцесс: ", i, j)
            # print("Block: \n")
            # print(block, "\n")

            # array 2x2 from block
            square = block[0:2, 0:2]

            # array 2x2 convert to 1d ([0,1,2,3])
            squareInline = square.flatten()
            # print("SquereInLine: ", squareInline)

            # Вычитываем пиксели
            d = calculateD(squareInline)
            print("\td значения - ", d)

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
            print("\tn значения - ",n)

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
            print("\tb значения - ",b)

            # Получаем числа которые нужно добавить в блок
            values = getValues(b)
            print("\tvalues: ", values)

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

            print("Секретные биты до внедрения:",secretBits[0:partCount])
            
            # Вычитываем биты которые были добавлены
            for k in range(len(b)):

                start = 0
                stop = len(b[k])

                # Remove charactes from index start to stop
                if len(secretBits) > stop:
                    secretBits = secretBits[0: start:] + secretBits[stop + 1::]
                elif len(secretBits) == 0:
                    secretMessageFinishStatus = True
            
            print("Осталось внедрить:",secretBits[0:partCount])
    if secretMessageFinishStatus != True:
        print("Размер битов секретного сообщения", secretBits)
        print("Не достаточно место для встраивания секретного сообщения, биты:", secretBits)
        exit()
    print(f"{bcolors.WARNING}Процесс внедрения прошел успешно ...\n{bcolors.ENDC}")
    return coverImage


def processDecode(stegoImage):
    lenI = math.ceil(len(stegoImage)/2)
    lenJ = math.ceil(len(stegoImage[0])/2)

    for i in range(lenI):
        for j in range(lenJ):
            # array 3x3
            block = stegoImage[i*3:i*3+3, j*3:j*3+3]

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
            # print("D: ", d)

            zeroValue = False  # переменная для статуса нулевых значении

            # Проверяем если все  3 значения равны нулю, значит ничего сюда не поместится
            for k in range(len(d)):
                d[k] = math.ceil(d[k])
                if d[k] <= 0:
                    zeroValue = True

            # Пропускаем блок 3х3 и переходим к следующему
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
            b = decode(block)
            print("\nПроцесс: ", i, j)
            print("Блок который восстанавливаем \n",block)
            print(b)
            exit()
            # Получаем числа возможные секретного сообщения
            values = getValues(b)
            print("values: ", values)
            if b[0] != '':
                firstPlace = coverImage[i*3:i*3+3, j*3:j*3+3][0][1] + values[0]
            if b[1] != '':
                secondPlace = coverImage[i*3:i*3 +
                                         3, j*3:j*3+3][1][0] + values[1]
            if b[2] != '':
                thirdPlace = coverImage[i*3:i*3+3, j*3:j*3+3][1][1] + values[2]
            print(firstPlace, secondPlace, thirdPlace)

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

            coverImage[i*3:i*3+3, j*3:j*3+3][0][1] = firstPlace
            coverImage[i*3:i*3+3, j*3:j*3+3][1][0] = secondPlace
            coverImage[i*3:i*3+3, j*3:j*3+3][1][1] = thirdPlace

            print("Новый блок\n", coverImage[i*3:i*3+3, j*3:j*3+3])

            # print(secretBits[0:partCount])
            # print(n)

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
        print("Не достаточно место для встраивания секротного сообщения, биты:", secretBits)
        exit()

    print("\n Процесс внедрения прошел успешно ...")
    return coverImage


secretMessage = 's'
secretMessageInBit = "01110011"

image = cv2.imread("images/space_32x32.png")

# to grayScale
grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
grayImage = np.array(grayImage)


stegoImage = processStego(grayImage, secretMessageInBit)
result = processDecode(stegoImage)

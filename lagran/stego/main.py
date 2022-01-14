from pil import Image
import matplotlib.image as img
import sys
import numpy as np
import cv2
import random
np.set_printoptions(threshold=sys.maxsize)


# Nearest Neighbor Interpolation Algorithm
# dstH is the height of the new image; dstW is the width of the new image
def NN_interpolation(img, dstH, dstW):
    scrH, scrW, _ = img.shape
    retimg = np.zeros((dstH, dstW, 3), dtype=np.uint8)
    for i in range(dstH-1):
        for j in range(dstW-1):
            scrx = round(i*(scrH/dstH))
            scry = round(j*(scrW/dstW))
            retimg[i, j] = img[scrx, scry]
    return retimg


def convertToBit(img):
    # Превращаем в набор битов
    s = (len(img), len(img[0]))
    imageBits = np.zeros(s)
    for i in range(len(img)):
        for j in range(len(img[i])):
            if img[i][j] % 2 == 0:
                imageBits[i][j] = 1
            else:
                imageBits[i][j] = 0
    return imageBits


def genereteCoordinates():
    # генерируем рандомные биты
    i_coordinates = []
    j_coordinates = []

    for i in range(5):
        random.seed(i)
        i_coordinates.append(random.randint(0, 255))

    for j in range(5):
        random.seed(j+5)
        j_coordinates.append(random.randint(0, 255))
    return i_coordinates, j_coordinates


# Открываем изображение
im_path = 'image.jpg'
image = np.array(Image.open(im_path))

# Увеличиваем размер картинки 2х
image1 = NN_interpolation(image, image.shape[0]*2, image.shape[1]*2)
image1 = Image.fromarray(image1.astype('uint8')).convert('RGB')
image1.save('2x_image.jpg')

# Конвертируем в черно-белый цвет
img = Image.open('2x_image.jpg')
imgGray = img.convert('L')
imgGray.save('gray.jpg')

img = cv2.imread('gray.jpg', 0)
imgBits = convertToBit(img)

i_coordinates, j_coordinates = [0, 1, 2, 3, 4], [0, 0, 0, 0, 0]

random.seed(10)
secretMessageBit = []
for k in range(10):
    secretMessageBit.append(random.randint(0, 1))

print("I", i_coordinates)
print("J", j_coordinates)
print("SecretMessageBit", secretMessageBit)

coordinateBits = []
for b in range(len(secretMessageBit)-5):

    i_value = i_coordinates[b]
    j_value = j_coordinates[b]

    if int(imgBits[i_value][j_value]) != secretMessageBit[b]:
        if img[i_value][j_value] < 254:
            print("Before", img[i_value][j_value])
            img[i_value][j_value] += 1
            print("After", img[i_value][j_value])
        elif img[i_value][j_value] == 255:
            print("Before", img[i_value][j_value])
            img[i_value][j_value] -= 1
            print("After", img[i_value][j_value])

cv2.imwrite('stegoImage.jpg', img)
for i in range(len(i_coordinates)):
    i_value = i_coordinates[i]
    j_value = j_coordinates[i]
    print("PixelBeforeSave", img[i_value][j_value])

print()
stegoImage = cv2.imread('stegoImage.jpg', 0)
for i in range(len(i_coordinates)):
    i_value = i_coordinates[i]
    j_value = j_coordinates[i]
    print("StegoPixels", stegoImage[i_value][j_value])

stegoImgBits = convertToBit(img)
i_coordinates, j_coordinates = genereteCoordinates()
secretStego = []
for i in range(len(i_coordinates)):
    i_value = i_coordinates[i]
    j_value = j_coordinates[i]
    secretStego.append(int(stegoImgBits[i_value][j_value]))

print("Repair secret data", secretStego)
print("SecretMessageBit", secretMessageBit)

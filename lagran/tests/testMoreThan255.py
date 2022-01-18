import cv2
import numpy as np

image = cv2.imread("discord_16x16.png")

# to grayScale
grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
grayImage = np.array(grayImage)
print(grayImage)
grayImage[0][0] = 300
print(grayImage)
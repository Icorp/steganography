import numpy as np
import math

arr = np.array([
    [1, 2, 3, 4, 5], 
    [6, 7, 8, 9, 10],
    [11, 12, 13, 14, 15], 
    [16, 17, 18, 19, 20]])

# print(arr[0:2,0:2])
# print(arr[0:2,2:4])

# print(arr[2:4,0:2])
# print(arr[2:4,2:4])

def encode(arr):
    lenI=math.ceil(len(arr)/2)
    lenJ=math.ceil(len(arr[0])/2)
    for i in range(lenI):
        for j in range(lenJ):
            print(i)
            print(j)
            print(arr[i*3:i*3+3,j*3:j*3+3])

encode(arr)
import numpy as np
from numpy.core.fromnumeric import shape

arr = np.zeros((3,3))
arr2 = [[1],[2],[3]]

for k in range(3):
    arr = np.append(arr,arr2,axis=1)
print(arr)
print(arr2)

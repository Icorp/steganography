import numpy as np

b = np.random.randint(5,size=225)
# print(b[0:3])
# print(b[2:5])
# print(b[4:7])
print(b)
result = []
for k in range(len(b)):
    if k % 2 == 0 or k == 0:
        print(b[k:k+3])
        result.append(b[k:k+3])
    else:
        continue

print(len(result))

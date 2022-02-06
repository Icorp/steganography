a = "011100110110010101100011011100100110010101110100"
print(a)
start = 0
stop = 3

if len(a) > stop :
    a = a[0: start:] + a[stop + 1::]


print(a)
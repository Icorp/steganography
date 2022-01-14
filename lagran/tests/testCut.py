a = "12345678910"

start = 0
stop = 5
# Remove charactes from index 5 to 10
if len(a) > stop :
    a = a[0: start:] + a[stop + 1::]

print(a)
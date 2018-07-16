import random

for j in range(len(a)):
    for i in range(len(a)):
        try:
            if a[i] > a[i+1]:
                temp = a[i]
                a[i] = a[i+1]
                a[i+1] = temp

            
        except IndexError:
            pass

    print(a)

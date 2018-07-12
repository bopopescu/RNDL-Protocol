q = input("zahl 1: ")
r = input("zahl 2: ")
m = input("aktion: ")
q = int(q)
r = int(r)
l = []
if m == "multiplikation":
    l = q*r

if m == "addition":
    l = q+r
    
if m == "subtraktion":
    l = q-r

if m == "division":
    l = q/r

print("ergebnis = " + str(l))




    






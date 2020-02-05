import random

# random getal 0-10
getalPy = random.randint(0,10)
getalRaden = None

# lus raden
while getalRaden != getalPy:
    # vraag getal
    getal = input("Raad het getal tussen 0 en 10 -> ")
    # validatie
    try:
        # omzetten naar integer
        getalRaden = int(getal)
        # getal geraden ?
        if getalRaden == getalPy:
            print("Proficiat! U hebt het getal geraden")
        else:
            print("Verkeerd! Probeer nog een keer")
    except ValueError:
        print("%s is geen getal !"%getal)
        
print("uit de lus")

'''
import random

getalPy = random.randint(0,10)

while True:
    getal=input("Geef getal -> ")
    try:
        if int(getal) == getalPy:
            break
    except:
    pass

print("geraden!")
'''

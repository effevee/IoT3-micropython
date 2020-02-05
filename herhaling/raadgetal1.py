import random

# random getal 0-10
getalPy = random.randint(0,1000)

# lus raden
while True:
    getal = input("Raad het getal [0-1000] -> ")

    try:
        geraden = int(getal)
        if geraden == getalPy:
            break
        elif geraden > getalPy:
            print("Te groot. Probeer nog een keer")
        else:
            print("Te klein. Probeer nog een keer")
    except ValueError:
        print("%s is geen getal !"%getal)
        
print("Juist geraden!")
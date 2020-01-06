import urandom
import utime
from machine import Pin

# random getal 0-10
getalPy = urandom.randint(0,1000)
getalRaden = None

# led pinnen initaliseren
ROOD = 26
BLAUW = 27
pr = Pin(ROOD,Pin.OUT)
pb = Pin(BLAUW,Pin.OUT)
pr.value(0)
pb.value(0)

# lus raden
while True:
    getal = input("Raad het getal [0-1000] -> ")

    try:
        geraden = int(getal)
        if geraden == getalPy:
            print("Juist geraden!")
            pr.value(1)
            pb.value(1)
            # nieuw getal na 5 sec
            utime.sleep(5)
            pr.value(0)
            pb.value(0)
            getalPy = urandom.randint(0,1000)
        elif geraden > getalPy:
            print("Te groot. Probeer nog een keer")
            pr.value(1)
            pb.value(0)
        else:
            print("Te klein. Probeer nog een keer")
            pr.value(0)
            pb.value(1)
    
    except ValueError:
        print("%s is geen getal !"%getal)

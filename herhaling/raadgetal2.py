import urandom
from machine import Pin
import utime

# random getal 0-10
getalPy = urandom.randint(0,1000)

# led pinnen initaliseren
ROOD = 32
BLAUW = 33
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
            # nieuw getal
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
        
    finally:
        pr.value(0)
        pb.value(0)
       

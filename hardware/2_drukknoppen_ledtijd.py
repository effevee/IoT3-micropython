from machine import Pin
import utime

# variabelen
GPIO_LED = 21
GPIO_RECHTS = 19
GPIO_LINKS = 18

# initialisatie drukknoppen (met pullup) en led
button_links = Pin(GPIO_LINKS, Pin.IN, Pin.PULL_UP)
button_rechts = Pin(GPIO_RECHTS, Pin.IN, Pin.PULL_UP)
led = Pin(GPIO_LED, Pin.OUT)

# oneindige lus
teller = 0
while True:
    # led blinken als geen toets gedrukt werd.
    while button_links.value() and button_rechts.value():
        led.value(1)
        utime.sleep(teller*0.01)
        led.value(0)
        utime.sleep(1)
    # oude teller bewaren 
    teller_save = teller
    # linker knop gedrukt
    if button_links.value() == 0:
        teller -= 2
        if teller < 0:
            teller = 0
    # rechter knop gedrukt
    if button_rechts.value() == 0:
        teller += 2
        if teller > 1024:
            teller = 1024
    # teller afdrukken indien gewijzigd
    if teller != teller_save:
        print('Teller=%d'%teller)
        teller_save = teller
    # efkes wachten
    utime.sleep(0.10)
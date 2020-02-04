from machine import Pin,TouchPad
import utime

# variabelen
calib_touch = []
PIN_TOUCH0 = 4
PIN_LED = 21
bTouch = False

# touch & LED initialiseren
tp = TouchPad(Pin(PIN_TOUCH0))
led = Pin(PIN_LED, Pin.OUT)

# los calibreren
print('Calibratie los - 10 metingen')
for i in range(0,10):
    waarde = tp.read()
    print('Waarde %d : %d'%(i,waarde))
    calib_touch.append(waarde)

# gemiddelde waarde
calib_val = sum(calib_touch) // len(calib_touch)

# lus
while True:
    # lees waarde
    waarde = tp.read()
    twaarde = waarde/calib_val
    # toon waarde
    print('Touchwaarde %.1f'%(twaarde))
    # led aan of uit
    if not bTouch and twaarde < 0.4:
        led.value(not led.value())
        bTouch = True
    elif twaarde >= 0.4:
        bTouch = False

    # even wachten
    utime.sleep_ms(500)

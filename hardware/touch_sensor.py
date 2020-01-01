from machine import Pin,TouchPad
import utime

# variabelen
calib_touch = []
PIN_TOUCH0 = 4

# touch initialiseren
tp = TouchPad(Pin(PIN_TOUCH0))

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
    waarde = tp.read()
    print('Touchwaarde %.1f'%(waarde/calib_val))
    utime.sleep_ms(500)

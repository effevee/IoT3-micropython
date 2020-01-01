from machine import Pin
import utime

GPIO_BUTTON = 19
button = Pin(GPIO_BUTTON, Pin.IN, Pin.PULL_UP)

try:
    while True:
        # buttom standaard hoog door pullup weerstand
        # eerste waarde
        first = button.value()
        # even wachten
        utime.sleep(0.01)
        # tweede waarde
        second = button.value()
        # knop gedrukt        
        if first and not second:
            print('Button pressed')
        elif not first and second:
            print('Button released')

except Exception as e:
    print("Drukknop probleem %s"%e)
    
finally:
    print('Cleanup')
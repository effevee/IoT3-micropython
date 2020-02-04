from machine import Pin
import utime
import urandom

# constanten
GPIO_BUTTON = 19
GPIO_LED = 21
MAX_TIMES = 5
MIN_REACT = 100
PENALTY_REACT = 5000

# declaraties
button = Pin(GPIO_BUTTON, Pin.IN, Pin.PULL_UP)
led = Pin(GPIO_LED, Pin.OUT)

try:
    times = 0
    # lus 5 pogingen
    while times < MAX_TIMES:
        # led aanzetten na random tijd
        wait = urandom.randint(2,15)
        utime.sleep(wait)
        led.value(1)
        # start tijd
        start_time = utime.ticks_ms()
        # lus wacht op reactie
        while True:
            # buttom standaard hoog door pullup weerstand
            if button.value() == 0:
                react_time = utime.ticks_diff(utime.ticks_ms(), start_time)
                # te vroeg gedrukt
                if react_time < MIN_REACT:
                    react_time = PENALTY_REACT
                # led uit
                led.value(0)
                # reactietijd tonen
                print('Reactie tijd %.0f ms'%react_time)
                break
            # even slapen
            utime.sleep(0.01)
        # volgende poging
        times += 1

except Exception as e:
    print("Drukknop probleem %s"%e)
    
finally:
    print('Cleanup')
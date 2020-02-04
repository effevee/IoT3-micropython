from machine import Pin,PWM
import utime

# variabelen
GPIO_RECHTS = 19
GPIO_LINKS = 18
GPIO_LED = 21
debounce_time_ms = 10

# initialisatie drukknoppen (met pullup)
button_links = Pin(GPIO_LINKS, Pin.IN, Pin.PULL_UP)
button_rechts = Pin(GPIO_RECHTS, Pin.IN, Pin.PULL_UP)
pwm = PWM(Pin(GPIO_LED),freq=100)
pwm.duty(0)


try:
    # oneindige lus
    teller = 0
    teller_save = teller
    button_links_vorig = 1
    button_rechts_vorig = 1
    while True:
        # test linker knop (stijgende flank)
        if button_links.value() == 0 and button_links_vorig == 1:
            teller -= 10
            if teller < 0:
                teller = 0
            pwm.duty(teller)
        # test rechter knop (stijgende flank)
        if button_rechts.value() == 0 and button_rechts_vorig == 1:
            teller += 10
            if teller > 1023:
                teller = 1023
            pwm.duty(teller)
        # toon teller        
        if teller != teller_save:
            print('Teller=%d'%teller)
            teller_save = teller
        # stand buttons bewaren
        button_links_vorig = button_links.value()
        button_rechts_vorig = button_rechts.value()
        # debounce
        utime.sleep_ms(debounce_time_ms)

except Exception as e:
    print('Probleem %s'%e)

finally:
    # pwm afsluiten
    pwm.deinit()
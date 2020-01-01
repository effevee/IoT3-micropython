from machine import Pin
import utime

# variabelen
GPIO_RECHTS = 19
GPIO_LINKS = 18
debounce_time_ms = 10

# initialisatie drukknoppen (met pullup)
button_links = Pin(GPIO_LINKS, Pin.IN, Pin.PULL_UP)
button_rechts = Pin(GPIO_RECHTS, Pin.IN, Pin.PULL_UP)

# oneindige lus
teller = 0
teller_save = teller
button_links_vorig = 1
button_rechts_vorig = 1
while True:
    # test linker knop (stijgende flank)
    if button_links.value() == 0 and button_links_vorig == 1:
        teller -= 2
        if teller < 0:
            teller = 0
    # test rechter knop (stijgende flank)
    if button_rechts.value() == 0 and button_rechts_vorig == 1:
        teller += 2
        if teller > 1023:
            teller = 1023
    # toon teller        
    if teller != teller_save:
        print('Teller=%d'%teller)
        teller_save = teller
        
    # stand buttons bewaren
    button_links_vorig = button_links.value()
    button_rechts_vorig = button_rechts.value()
    
    # debounce
    utime.sleep_ms(debounce_time_ms)

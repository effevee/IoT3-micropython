from machine import Pin
import uasyncio as asyncio

# variabelen
GPIO_LED = 21
GPIO_RECHTS = 19
GPIO_LINKS = 18

# initialisatie drukknoppen (met pullup)
led = Pin(GPIO_LED, Pin.OUT)
knop_links = Pin(GPIO_LINKS, Pin.IN, Pin.PULL_UP)
knop_rechts = Pin(GPIO_RECHTS, Pin.IN, Pin.PULL_UP)

class gvars:
    teller = 0
    debounce_time = 10 # ms
    
async def links_gedrukt():
    while True:
        # links gedrukt ?
        if knop_links.value() == 0:
            # teller verminderen
            gvars.teller -= 2
            if gvars.teller < 0:
                gvars.teller = 0
            # toon teller
            print('Teller=%d'%(gvars.teller))
            # debounce
            while knop_links.value() == 0:
                await asyncio.sleep_ms(gvars.debounce_time)
        # even wachten
        await asyncio.sleep_ms(gvars.debounce_time)
        

async def rechts_gedrukt():
    while True:
        # rechts gedrukt ?
        if knop_rechts.value() == 0:
            # teller vermeerderen
            gvars.teller += 2
            if gvars.teller > 1024:
                gvars.teller = 1024
            # toon teller
            print('Teller=%d'%(gvars.teller))
            # debounce
            while knop_rechts.value() == 0:
                await asyncio.sleep_ms(gvars.debounce_time)
        # even wachten
        await asyncio.sleep_ms(gvars.debounce_time)


async def flash_led():
    while True:
        # led aan voor teller * 0.01 sec
        if gvars.teller > 0:
            led.value(1)
        await asyncio.sleep_ms(int(gvars.teller*10))
        # led uit voor 1000 ms
        led.value(0)
        await asyncio.sleep_ms(1000)
        

async def print_priemgetal(maximum):
    # lus priemgetallen
    for getal in range(2,maximum):
        # lus check getal is priemgetal
        is_priem = True
        for deler in range(2,getal):
            # getal deelbaar door deler ?
            if (getal % deler) == 0:
                is_priem = False
                break
            # even wachten
            await asyncio.sleep_ms(5)
        # priemgetal printen
        if is_priem :
            print('Priemgetal: %d'%getal)
            
try:
    # event loop scheduler initialiseren
    loop = asyncio.get_event_loop()
    # taken op de event loop queue zetten
    loop.create_task(links_gedrukt())
    loop.create_task(rechts_gedrukt())
    loop.create_task(flash_led())
    loop.create_task(print_priemgetal(10000))
    # taken laten uitvoeren
    loop.run_forever()

except Exception as e:
    print('Probleem met asyncio - %s'%e)

finally:
    # event loop scheduler afsluiten
    loop.close()
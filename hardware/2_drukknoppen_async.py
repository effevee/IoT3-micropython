from machine import Pin
import uasyncio as asyncio

# variabelen
GPIO_RECHTS = 19
GPIO_LINKS = 18

# initialisatie drukknoppen (met pullup)
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
                asyncio.sleep_ms(gvars.debounce_time)
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
                asyncio.sleep_ms(gvars.debounce_time)
        # even wachten
        await asyncio.sleep_ms(gvars.debounce_time)


loop = asyncio.get_event_loop()
loop.create_task(links_gedrukt())
loop.create_task(rechts_gedrukt())
loop.run_forever()
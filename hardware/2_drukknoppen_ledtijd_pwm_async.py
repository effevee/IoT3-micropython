from machine import Pin, PWM
import uasyncio as asyncio

# variabelen
GPIO_LED = 21
GPIO_RECHTS = 19
GPIO_LINKS = 18

# initialisatie drukknoppen (met pullup)
led = PWM(Pin(GPIO_LED), freq=50)
knop_links = Pin(GPIO_LINKS, Pin.IN, Pin.PULL_UP)
knop_rechts = Pin(GPIO_RECHTS, Pin.IN, Pin.PULL_UP)

class gvars:
    teller = 512
    debounce_time = 10 # ms
    
async def links_gedrukt():
    while True:
        # links gedrukt ?
        if knop_links.value() == 0:
            # teller verminderen
            gvars.teller -= 50
            if gvars.teller < 0:
                gvars.teller = 0
            # toon teller
            print('Teller=%d'%(gvars.teller))
            # led aansturen
            led.duty(gvars.teller)
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
            gvars.teller += 50
            if gvars.teller > 1023:
                gvars.teller = 1023
            # toon teller
            print('Teller=%d'%(gvars.teller))
            # led aansturen
            led.duty(gvars.teller)
            # debounce
            while knop_rechts.value() == 0:
                await asyncio.sleep_ms(gvars.debounce_time)
        # even wachten
        await asyncio.sleep_ms(gvars.debounce_time)

try:
    # event loop scheduler initialiseren
    loop = asyncio.get_event_loop()
    # taken op de event loop queue zetten
    loop.create_task(links_gedrukt())
    loop.create_task(rechts_gedrukt())
    # taken laten uitvoeren
    loop.run_forever()

except Exception as e:
    print('Probleem met asyncio - %s'%e)

finally:
    # event loop scheduler afsluiten
    loop.close()
    # pwm led afsluiten
    led.deinit()
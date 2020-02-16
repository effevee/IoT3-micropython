import uasyncio as asyncio

# led pins
RED = 21
BLUE = 19
GREEN = 5
YELLOW = 16

async def flash_led(pin, interval):
    from machine import Pin
    led = Pin(pin, Pin.OUT, value=0)
    while True:
        if led.value():
            led.off()
        else:
            led.on()
        await asyncio.sleep_ms(interval)

try:
    # event loop scheduler initialiseren
    loop = asyncio.get_event_loop()
    # taken op de event loop queue zetten
    loop.create_task(flash_led(RED, 125))
    loop.create_task(flash_led(BLUE, 250))
    loop.create_task(flash_led(GREEN, 500))
    loop.create_task(flash_led(YELLOW, 1000))
    # taken laten uitvoeren
    loop.run_forever()

except Exception as E:
    print('Problem with asyncio', E)
    
finally:
    loop.close()
    
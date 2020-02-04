# Do not use this code in real projects! Read
# http_server_simplistic_commented.py for details.
import uasyncio as asyncio

counter = 0

def connect2wifi():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('<SSID>', '<PWD>')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

async def flash_buildin_led(interval):
    from machine import Pin
    led = Pin(13, Pin.OUT, value=0)
    while True:
        if led.value():
            led.off()
        else:
            led.on()
        await asyncio.sleep_ms(interval)

        
async def handle_client(reader, writer):
    global counter
    # wait for client connection
    request = await reader.read()
    # get ip address of client
    addr = writer.get_extra_info('peername')
    print('Got a connection from %s' % str(addr))
    print('Content = %s' % request.decode())
    # create response
    counter += 1
    response = """<html><body>Hello """ + str(counter) + """ from MicroPython!</body></html>"""
    print(response)
    # send response
    await writer.awrite('HTTP/1.1 200 OK\r\n\r\n' + response + '\r\n\r\n')
    # close writer
    await writer.aclose()


# connect ESP to wifi network
connect2wifi()
# event loop scheduler initialiseren
loop = asyncio.get_event_loop()
# taken op de event loop queue zetten
loop.create_task(asyncio.start_server(handle_client, '0.0.0.0', 80))
loop.create_task(flash_buildin_led(500))
# taken laten uitvoeren
loop.run_forever()


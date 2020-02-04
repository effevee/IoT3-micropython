from machine import Pin,DAC
import utime
import math

# variabelen
DAC_GPIO = 25
buf = []

# initialiseren DAC
dac = DAC(Pin(DAC_GPIO))

# sinusbuffer opvullen
for i in range(0,100):
    buf.append(128 + int(127 * math.sin(2 * math.pi * i / 100)))

# zaagtand naar DAC
j = 0
while True:
    # waarde naar DAC
    val = buf[j]
    print(val)
    dac.write(val)
    # volgende waarde
    j+=1
    if j >= 100:
        j = 0
    # 10 ms wachten - 100 * 10ms = 1 s
    utime.sleep_ms(10)

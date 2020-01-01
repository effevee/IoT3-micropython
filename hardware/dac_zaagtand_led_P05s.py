from machine import Pin,DAC
import utime

# variabelen
DAC_GPIO = 25
buf = []

# initialiseren DAC
dac = DAC(Pin(DAC_GPIO))

# zaagtandbuffer opvullen
for i in range(0,100):
    buf.append(i*2)
    
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
    # 5 ms wachten - 100 * 5ms = 0.5 s
    utime.sleep_ms(5)

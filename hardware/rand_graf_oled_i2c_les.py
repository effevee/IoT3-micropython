from machine import I2C,Pin
import ssd1306
import utime
import random

i2c = I2C(scl=Pin(12),sda=Pin(13))
oled=ssd1306.SSD1306_I2C(128,64,i2c)

histo = [0]*32
hist_pos = 0

while True:
    oled.fill(0)
    n=random.randint(0,100)
    #schalen op 63:
    ns=int((n/100.0)*63)
    #om te tekenen vanaf de basis
    nsb=63-ns
    if hist_pos >= len(histo):
        hist_pos=0
        histo = [0]*32
    histo[hist_pos]=nsb
    j=0
    for i in histo:
        print(i)
        oled.fill_rect(4*j,63-i,4,i,1)#parameters:x,y,w,h,kleur
        j=j+1
    oled.show()
    utime.sleep_ms(500)
    hist_pos=hist_pos+1

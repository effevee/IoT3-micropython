from machine import I2C,Pin
import ssd1306
import utime
import urandom

# I2C en oled initialiseren
i2c = I2C(scl=Pin(12), sda=Pin(13))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# histogram initialiseren
histo = []
hist_pos = 0
# oneindige lus
while True:
    # scherm wissen
    oled.fill(0)
    oled.show()
    # random getal
    getal = urandom.randint(0,63)
    # bewaren in lijst
    histo.append(getal)
    print(histo)
    # staafpositie ophogen
    hist_pos += 1
    if hist_pos >= 32:
        histo.pop(0)
    # herteken histogram
    i = 0
    oled.fill(0)
    for j in histo:
        oled.fill_rect(i*4,63-j,4,j,1)
        i+=1
    oled.show()
    # even wachten
    utime.sleep_ms(500)


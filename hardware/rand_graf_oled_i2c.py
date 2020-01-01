from machine import I2C,Pin
import ssd1306
import utime
import urandom

# I2C en oled initialiseren
i2c = I2C(scl=Pin(12), sda=Pin(13))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

   
# histogram initialiseren
histo = []
hist_pos = 32

# oneindige lus
while True:
    # hist positie ophogen
    hist_pos += 1
    if hist_pos >= 32:
        hist_pos = 0
        histo = []
        oled.fill(0)
        oled.show()
    # random getal
    getal = urandom.randint(0,63)
    # bewaren in lijst
    histo.append(getal)
    print(histo)
    # teken staaf
    x = 0 + hist_pos*4
    y = 63 - getal
    w = 4
    h = getal
    oled.fill_rect(x, y, w, h, 1)
    oled.show()
    # even wachten
    utime.sleep_ms(500)


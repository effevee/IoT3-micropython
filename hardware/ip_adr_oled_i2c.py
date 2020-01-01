from machine import I2C,Pin
import ssd1306
import utime
import simpleWifi

# I2C en oled initialiseren
i2c = I2C(scl=Pin(12), sda=Pin(13))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# schermbuffer wissen
oled.fill(0)
# tekst in schermbuffer
oled.text("IP-adres ESP32",0,0)

# wifi object aanmaken
myWifi = simpleWifi.Wifi()
# connecteren met wifi
if myWifi.open():
    # toon IP adres
    oled.text(myWifi.get_IPdata()[0],0,9)
else:
    oled.text("Probleem met wifi",0,9)

# schermbuffer tonen
for pos in range(0,13):
    # balk opbouwen
    oled.text("#", pos*10, 20)
    # schermbuffer tonen          
    oled.show()          
    # even wachten
    utime.sleep(1)
# oled uitschakelen
oled.poweroff()
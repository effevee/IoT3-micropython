from machine import I2C, Pin

# I2C initialiseren 
i2c = I2C(scl=Pin(12),sda=Pin(13))

# toon I2C adressen slaves
print(i2c.scan())

# oled zit op dec 60 - hex 3C
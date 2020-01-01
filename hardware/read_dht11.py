# modules
import dht
import machine
import utime

DHT11_GPIO=15

# dht11 sensor initialiseren
sensor = dht.DHT11(machine.Pin(DHT11_GPIO))

# oneindige lus
while True:
    # sensor uitlezen
    sensor.measure()
    # resultaten tonen
    print('Temperatuur: %.0f°C - vochtigheid: %.0f%%' % (sensor.temperature(), sensor.humidity()))
    # wachten foor volgende meting
    utime.sleep(5)
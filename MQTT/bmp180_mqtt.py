# modules
from bmp180 import BMP180
from machine import I2C, Pin
import time
from umqtt.robust import MQTTClient

# I2C bus initialiseren
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=20000)

# bmp180 sensor initialiseren
sensor3 = BMP180(i2c)
sensor3.oversample_sett = 2
sensor3.baseline = 101325     # Pa

# lees bmp180 sensor
temp = sensor3.temperature
press = sensor3.pressure
altitude = sensor3.altitude

# toon waarden
print("Temperature: {0:.1f} C".format(temp))
print("Pressure: {0:.0f} mbar".format(press/100))
print("Altitude: {0:.0f} m".format(altitude))

# MQTT client initialiseren
mqtt_server = '192.168.1.22'
# mqtt_server = '172.24.0.118'
mqtt_client = MQTTClient('52dc166c-2de7-43c1-88ff-f80211c7a8f6', mqtt_server)
mqtt_client.connect()

while True:
  # bmp180 uitlezen
  t = sensor3.temperature   # 閹虹煰
  p = sensor3.pressure        # Pa
  a = sensor3.altitude          # m
  # waarden tonen in console
  print("Temperature {0:.1f} C - Pressure {1:.0f} mbar - Altitude {2:.0f} m".format(t,p/100,a))
  # waarden publishen naar mqtt server
  mqtt_client.publish('house/sensor3/temperature', str(t))
  mqtt_client.publish('house/sensor3/pressure', str(p))
  mqtt_client.publish('house/sensor3/altitude', str(a))
  
  # 5 seconden wachten
  time.sleep(5)


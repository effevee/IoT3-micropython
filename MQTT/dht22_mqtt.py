# modules
import dht
import machine
import time
from umqtt.robust import MQTTClient

# dht22 sensor initialiseren
sensor2 = dht.DHT22(machine.Pin(15))

# MQTT client initialiseren
mqtt_server = '192.168.1.22'
# mqtt_server = '172.24.0.118'
mqtt_client = MQTTClient('52dc166c-2de7-43c1-88ff-f80211c7a8f6', mqtt_server)
mqtt_client.connect()

while True:
  # dht22 uitlezen
  sensor2.measure()
  t = sensor2.temperature()
  h = sensor2.humidity()
  # waarden tonen in console
  print("Temperature {0:2}C - Humidity  {1:2}%".format(t,h))
  # waarden publishen naar mqtt server
  mqtt_client.publish('house/sensor2/temperature', str(t))
  mqtt_client.publish('house/sensor2/humidity', str(h))
  # 5 seconden wachten
  time.sleep(5)
  

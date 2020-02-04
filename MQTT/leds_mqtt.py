# modules
import machine
import time
from umqtt.robust import MQTTClient

# leds initialiseren
led_green = Pin(25, Pin.OUT, value=0)
led_yellow = Pin(26, Pin.OUT, value=0)
led_red = Pin(27, Pin.OUT, value=0)

# MQTT client initialiseren
mqtt_server = '192.168.1.22'
# mqtt_server = '172.24.0.118'
mqtt_clientID = '52dc166c-2de7-43c1-88ff-f80211c7a8f6'
mqtt_topic = b'house/led/#'

def sub_cb(topic,state):
  
  if topic == b'house/led/green':
      if state == b'on' :
        led_green.value(1)
      else :
        led_green.value(0)
  elif topic == b'house/led/yellow':
      if state == b'on' :
        led_yellow.value(1)
      else :
        led_yellow.value(0)
  elif topic == b'house/led/red':
      if state == b'on' :
        led_red.value(1)
      else :
        led_red.value(0)
  
  
def main(server=mqtt_server):
    
    mqtt_client = MQTTClient(mqtt_clientID, mqtt_server)
    # mqtt berichten gaan naar deze callback functie
    mqtt_client.set_callback(sub_cb)
    # connecteer  op mqtt server
    mqtt_client.connect()
    # subscribe op de topics
    mqtt_client.subscribe(mqtt_topic)
    # status mqtt connectie
    print("Verbonden met mqtt %s, geabonneerd op %s topic" % (mqtt_server, mqtt_topic))

    try:
        while True:
            # wacht op mqtt messages
            mqtt_client.wait_msg()
    finally:
      # verbreek mqtt connectie
      mqtt_client.disconnect()

main()

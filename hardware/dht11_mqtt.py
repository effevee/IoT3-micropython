# modules
import dht
import machine
import time
import simpleWifi
import sys
from umqtt.robust import MQTTClient

#BROKER='172.24.0.122'
BROKER='192.168.1.22'
DHT11_GPIO=15
LED_NORM=23
LED_WARN=22
LED_ALAR=21
TEMP_WARNING=25
TEMP_ALARM=35
TOPIC_TEMP='esp/frank_16/temperature'
TOPIC_HUM='esp/frank_16/humidity'
TOPIC_TEMP_MESSAGE='esp/frank_16/temp/message'

mqtt_cl = None

# dht11 sensor initialiseren
dht11 = dht.DHT11(machine.Pin(DHT11_GPIO))

# leds initialiseren
leds = [machine.Pin(LED_NORM, machine.Pin.OUT, value=0), machine.Pin(LED_WARN, machine.Pin.OUT, value=0), machine.Pin(LED_ALAR, machine.Pin.OUT, value=0)]

# wifi object aanmaken
myWifi = simpleWifi.Wifi()
# connecteren met wifi
if not(myWifi.open()):
    myWifi.get_status()
    sys.exit()
# tonen status wifi
myWifi.get_status()

# MQTT client initialiseren
try:
    # mqtt client aanmaken
    mqtt_cl=MQTTClient('esp_frank_16',BROKER)
    # connecteren op mqtt broker
    mqtt_cl.connect()
    # oneindige lus
    while True:
        # dht11 uitlezen
        dht11.measure()
        t = dht11.temperature()
        h = dht11.humidity()
        # temperatuur controle
        m = 'Temp normal'
        leds[0].value(1)
        leds[1].value(0)
        leds[2].value(0)
        if t > TEMP_ALARM:
            m = 'Temp alarm'
            leds[0].value(0)
            leds[1].value(0)
            leds[2].value(1)
        elif t > TEMP_WARNING:
            m = 'Temp warning'
            leds[0].value(0)
            leds[1].value(1)
            leds[2].value(0)
        # waarden tonen in console
        print("Temperature {0:2}C - Humidity  {1:2}% - {2} ".format(t,h,m))
        # waarden publishen naar mqtt server
        mqtt_cl.publish(TOPIC_TEMP, str(t))
        mqtt_cl.publish(TOPIC_HUM, str(h))
        mqtt_cl.publish(TOPIC_TEMP_MESSAGE, m)
        # 5 seconden wachten
        time.sleep(5)

except Exception as e:
    print('Problemen met MQTT - %s'%e)
    
finally:
    if mqtt_cl != None:
        mqtt_cl.disconnect()
    myWifi.close()
  

# modules
import dht
import machine
import utime
import simpleWifi
import sys
from umqtt.robust import MQTTClient
import usocket

# constanten
DHT11_GPIO=15
BROKER='172.24.0.122'
#BROKER='192.168.1.22'
TOPIC_TEMP='esp/frank_16/temperature'
TOPIC_HUM='esp/frank_16/humidity'

# variabelen
mqtt_cl=None
PORT = 7800
SERVER_ADR='172.24.0.122'
#SERVER_ADR='192.168.1.22'
s=None

# wifi object aanmaken
myWifi = simpleWifi.Wifi()
# connecteren met wifi
if not(myWifi.open()):
    print("Probleem met wifi")    
    myWifi.get_status()
    sys.exit()
# tonen status wifi
myWifi.get_status()

# MQTT client en socket initialiseren
try:
    # mqtt client aanmaken
    mqtt_cl=MQTTClient('esp_frank_16',BROKER)
    # connecteren op mqtt broker
    mqtt_cl.connect()
    # dht11 sensor initialiseren
    sensor = dht.DHT11(machine.Pin(DHT11_GPIO))
    # socket initialiseren
    s=usocket.socket()
    s.connect(usocket.getaddrinfo(SERVER_ADR,PORT)[0][-1])
    # oneindige lus
    while True:
        # dht11 uitlezen
        sensor.measure()
        t = sensor.temperature()
        h = sensor.humidity()
        # waarden tonen in console
        print("Temperature %.0f°C - Humidity %.0f%%" % (t,h))
        # waarden publishen naar mqtt server
        mqtt_cl.publish(TOPIC_TEMP, str(t))
        mqtt_cl.publish(TOPIC_HUM, str(h))
        # waarde STOP opvragen
        s.write("stop?\n")
        ans=int(s.recv(4).decode('utf-8'))
        # moeten we stoppen ?
        if ans == 1:
            break
        # 5 seconden wachten
        utime.sleep(5)

except Exception as e:
    print('communicatie problemen - %s'%e)
    
finally:
    if mqtt_cl != None:
        mqtt_cl.disconnect()
    if s != None:
        s.close()
    myWifi.close()
    sys.exit()
  

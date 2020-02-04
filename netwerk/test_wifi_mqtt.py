import random
import simpleWifi
import utime
import sys
from umqtt.robust import MQTTClient

BROKER='172.24.0.100'
#BROKER='192.168.1.22'
TOPIC='esp/frank_16/getal'
TIME=10
mqtt_cl=None

myWifi=simpleWifi.Wifi()
if not(myWifi.open()):
    myWifi.get_status()
    sys.exit()
myWifi.get_status()

try:
    mqtt_cl=MQTTClient('esp_frank_16',BROKER)
    mqtt_cl.connect()
    while True:
        getal=random.randint(0,100)
        mqtt_cl.publish(TOPIC,str(getal))
        utime.sleep(TIME)

except Exception as e:
    print('Problemen met MQTT - %s'%e)

finally:
    if myWifi.get_status()==1:
        if mqtt_cl!=None:
            mqtt_cl.close()
        myWifi.close()
    
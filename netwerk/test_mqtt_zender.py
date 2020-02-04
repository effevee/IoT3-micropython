import simpleWifi
import utime
import sys
from umqtt.robust import MQTTClient

#BROKER='172.24.0.122'
BROKER='192.168.1.22'
TOPIC='esp/frank_16/IP'
TIME=30
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
        IP_data=myWifi.get_IPdata()
        mqtt_cl.publish(TOPIC,IP_data[0])
        utime.sleep(TIME)
except Exception as e:
    print('Problemen met MQTT - %s'%e)
finally:
    mqtt_cl.disconnect()
    myWifi.close()
    
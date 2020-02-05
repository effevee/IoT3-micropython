import simpleWifi
import utime
import sys
import tools
from umqtt.robust import MQTTClient

#BROKER='172.24.0.122'
BROKER='192.168.1.22'
TOPIC1='esp/frank_16/IP'
TOPIC2='esp/frank_16/FREERAM'
TOPIC3='esp/frank_16/FREESPACE'
TOPIC4='esp/frank_16/TOTALSPACE'
TIME=90
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
        # IP adres
        IP_data=myWifi.get_IPdata()
        mqtt_cl.publish(TOPIC1,IP_data[0])
        # vrije ram
        FreeRam=tools.mem_space()
        mqtt_cl.publish(TOPIC2,str(FreeRam[1]))
        # vrije fs ruimte
        FS_space=tools.fs_space()
        mqtt_cl.publish(TOPIC3,str(FS_space[1]))
        # totale fs ruimte
        mqtt_cl.publish(TOPIC4,str(FS_space[0]))
        # wachten
        utime.sleep(TIME)
except Exception as e:
    print('Problemen met MQTT - %s'%e)
finally:
    mqtt_cl.disconnect()
    myWifi.close()
    
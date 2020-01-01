import simpleWifi
import sys
from umqtt.robust import MQTTClient

BROKER='172.24.0.122'
#BROKER='192.168.1.22'
TOPIC1='esp/frank_16/bericht'
mqtt_cl = None

def messages(topic,msg):
    ''' toont de messages van de broker '''
    print(msg.decode('utf-8')) # decode van bytes naar string


# wifi object aanmaken
myWifi = simpleWifi.Wifi()
# connecteren met wifi
if not(myWifi.open()):
    myWifi.get_status()
    sys.exit()
# tonen status wifi
myWifi.get_status()


try:
    # mqtt client aanmaken
    mqtt_cl=MQTTClient('esp_frank_16',BROKER)
    # callback functie instellen
    mqtt_cl.set_callback(messages)
    # connecteren op mqtt broker
    mqtt_cl.connect()
    # subscriben op topic
    mqtt_cl.subscribe(TOPIC1)
    # wachten op broker berichten
    while True:
        mqtt_cl.wait_msg()
        
except Exception as e:
    print('Problemen met MQTT - %s'%e)
    
finally:
    if mqtt_cl != None:
        mqtt_cl.disconnect()
    myWifi.close()

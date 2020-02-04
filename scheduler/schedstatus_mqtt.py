import simpleWifi
import sys
import utime
from umqtt.robust import MQTTClient
from machine import Pin

def mqttMsg(topic,msg):
    ''' ontvang de mqtt berichten en zet LED1 aan of uit '''
    msg = msg.decode("UTF-8")
    pLed1.value(int(msg))
    return

# constanten
#BROKER = "192.168.1.22" #IP Broker
BROKER = "172.24.0.100" #IP Broker
ID = "esp_frank_1604"  #moet uniek zijn voor je netwerk
TOPIC1 = "sched/frank1604/LED1"

# led1 initialiseren
pLed1 = Pin(32,Pin.OUT)
pLed1.value(0)

# wifi initialiseren
mqttCl = None
myWifi = simpleWifi.Wifi()

if not(myWifi.open()):
    myWifi.get_status()
    sys.exit()
myWifi.get_status()


try:
    # mqtt client aanmaken
    mqttCl=MQTTClient(ID,BROKER)
    # callback functie instellen voor ontvangen berichten
    mqttCl.set_callback(mqttMsg)
    # connectie maken met mqtt broker
    mqttCl.connect()
    # subscriben op TOPIC
    mqttCl.subscribe(TOPIC1)
    # wachten op mqtt berichten
    while True:
        mqttCl.wait_msg()
        utime.sleep(10)

except Exception as e:
    print("mqtt of netwerk probleem - %s"%e)

finally:
    # led uit
    pLed1.value(0)
    # als wifi aan
    if myWifi.get_status() == 1:
        # als mqtt client aan
        if mqttCl != None:
            # mqtt client afzetten
            mqttCl.disconnect()
        # wifi afzetten
        myWifi.close()
            

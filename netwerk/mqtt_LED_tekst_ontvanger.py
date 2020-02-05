import simpleWifi
import sys
from umqtt.robust import MQTTClient
from machine import Pin

#BROKER='172.24.0.122'
BROKER='192.168.1.22'
GPIO_LED1=21
GPIO_LED2=22
GPIO_LED3=23

# klasse voor globale variabelen die gebruikt worden in messages
class gvars:
    TOPIC='esp/frank_16/bericht'
    TOPIC_LED1='esp/frank_16/LED1'
    TOPIC_LED2='esp/frank_16/LED2'
    TOPIC_LED3='esp/frank_16/LED3'
    led1=Pin(GPIO_LED1,Pin.OUT)
    led2=Pin(GPIO_LED2,Pin.OUT)
    led3=Pin(GPIO_LED3,Pin.OUT)
    
def messages(topic,msg):
    ''' toont de messages van de broker of stuurt de LED aan '''
    t = topic.decode('utf-8')
    m = msg.decode('utf-8')
    if t == gvars.TOPIC:
        print(msg.decode('utf-8')) # decode van bytes naar string
    elif t == gvars.TOPIC_LED1:
        if m == 'true':
            print('LED rood on')
            gvars.led1.value(1)
        else:  #false
            print('LED rood off')
            gvars.led1.value(0)
    elif t == gvars.TOPIC_LED2:
        if m == 'true':
            print('LED geel on')
            gvars.led2.value(1)
        else:  #false
            print('LED geel off')
            gvars.led2.value(0)
    elif t == gvars.TOPIC_LED3:
        if m == 'true':
            print('LED groen on')
            gvars.led3.value(1)
        else:  #false
            print('LED groen off')
            gvars.led3.value(0)

# LEDs initialiseren
gvars.led1.value(0)
gvars.led2.value(0)
gvars.led3.value(0)

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
    # subscriben op topics
    mqtt_cl.subscribe(gvars.TOPIC)
    mqtt_cl.subscribe(gvars.TOPIC_LED1)
    mqtt_cl.subscribe(gvars.TOPIC_LED2)
    mqtt_cl.subscribe(gvars.TOPIC_LED3)
    # wachten op broker berichten
    while True:
        mqtt_cl.wait_msg()
except Exception as e:
    print('Problemen met MQTT - %s'%e)
finally:
    mqtt_cl.disconnect()
    myWifi.close()

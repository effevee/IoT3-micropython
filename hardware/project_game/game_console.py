import simpleWifi
import utime
import sys
from umqtt.robust import MQTTClient
from machine import Pin,TouchPad

# constanten
#BROKER='172.24.0.122'
BROKER='192.168.1.22'
TOPIC='game/move'
TIME=100
PIN_TOUCH0=4
PIN_TOUCH5=12
FACTOR=0.5

# variabelen
mqtt_cl=None
tpLinks=None
tpRechts=None

# calibratie touchpin
def calibTouchPin(tp):
    global TIME
    calib_touch=[]
    for i in range(0,10):
        calib_touch.append(tp.read())
        utime.sleep_ms(TIME)
    return sum(calib_touch) // len(calib_touch)

# wifi initialisatie
myWifi=simpleWifi.Wifi()
if not(myWifi.open()):
    myWifi.get_status()
    sys.exit()
myWifi.get_status()


try:
    
    # mqtt initialisatie
    mqtt_cl=MQTTClient('esp_frank_16',BROKER)
    mqtt_cl.connect()
    
    # touchpin initialisatie
    tpLinks=TouchPad(Pin(PIN_TOUCH5))
    tpRechts=TouchPad(Pin(PIN_TOUCH0))
    
    # touchpin calibratie
    drempelLinks=int(calibTouchPin(tpLinks)*FACTOR)
    drempelRechts=int(calibTouchPin(tpRechts)*FACTOR)
    
    while True:
        
        # touchpin uitlezen
        vLinks=tpLinks.read()
        vRechts=tpRechts.read()
        
        # move code
        if (vLinks<=drempelLinks and vRechts<=drempelRechts) or (vLinks>drempelLinks and vRechts>drempelRechts):
            Dx=0
        elif vLinks<=drempelLinks:
            Dx=-1
        else:
            Dx=1
        print(Dx)    
        
        # move code doorsturen naar mqtt broker
        mqtt_cl.publish(TOPIC,str(Dx))
        
        # even wachten
        utime.sleep_ms(TIME)
        
except Exception as e:
    print('Problemen met MQTT - %s'%e)
finally:
    mqtt_cl.disconnect()
    myWifi.close()
    

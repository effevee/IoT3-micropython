from machine import Pin
import utime
import urandom
import simpleWifi
import sys
from umqtt.robust import MQTTClient

# constanten
GPIO_BUTTON = 19
GPIO_LED = 21
MAX_TIMES = 5
MIN_REACT = 100
PENALTY_REACT = 5000

#BROKER='172.24.0.122'
BROKER='192.168.1.22'
TOPIC='esp/frank_16/reactie'

# declaraties
button = Pin(GPIO_BUTTON, Pin.IN, Pin.PULL_UP)
led = Pin(GPIO_LED, Pin.OUT)
mqtt_cl=None

# Wifi opzetten
myWifi=simpleWifi.Wifi()
if not(myWifi.open()):
    myWifi.get_status()
    sys.exit()
myWifi.get_status()

try:
    # MQTT opzetten
    mqtt_cl=MQTTClient('esp_frank_16',BROKER)
    mqtt_cl.connect()
    # lus 5 pogingen
    times = 0
    while times < MAX_TIMES:
        # led aanzetten na random tijd
        wait = urandom.randint(2,15)
        utime.sleep(wait)
        led.value(1)
        # start tijd
        start_time = utime.ticks_ms()
        # lus wacht op reactie
        while True:
            # buttom standaard hoog door pullup weerstand
            if button.value() == 0:
                react_time = utime.ticks_diff(utime.ticks_ms(), start_time)
                # te vroeg gedrukt
                if react_time < MIN_REACT:
                    react_time = PENALTY_REACT
                # led uit
                led.value(0)
                # reactietijd tonen
                print('Reactie tijd %.0f ms'%react_time)
                # reactietijd publishen
                mqtt_cl.publish(TOPIC,str(round(react_time,0)))
                # uit oneidige lus
                break
            # even slapen
            utime.sleep(0.01)
        # volgende poging
        times += 1

except Exception as e:
    print("Drukknop probleem %s"%e)
    
finally:
    print('Cleanup')
    if mqtt_cl !=None:
        mqtt_cl.disconnect()
    myWifi.close()

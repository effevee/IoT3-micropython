
#hardware platform: FireBeetle-ESP32
#Result: Blink
#The information below shows blink is unavailble for the current version.
#IO0 IO4 IO10 IO12~19 IO21~23 IO25~27
#Except the connection between IO2 and onboard LED, other pins need to connect to external LEDs. 

import time
from machine import Pin
led1=Pin(21,Pin.OUT)        #create LED object from pin21,Set Pin21 to output
led2=Pin(22,Pin.OUT)        #create LED object from pin22,Set Pin22 to output


for t in range(10):
  led1.value(1)            #Set led turn on
  led2.value(0)            #Set led turn off
  time.sleep(0.5)
  led1.value(0)            #Set led turn off
  led2.value(1)            #Set led turn on
  time.sleep(0.5)

led2.value(0)




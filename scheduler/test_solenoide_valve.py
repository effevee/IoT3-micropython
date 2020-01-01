import time
from machine import Pin

VALVE_PIN=21
valve=Pin(VALVE_PIN,Pin.OUT)

while True:
  #valve closed
  valve.value(0)
  print("valve close")
  time.sleep(5)
  #valve open 
  valve.value(1)
  print("valve open")
  time.sleep(5)

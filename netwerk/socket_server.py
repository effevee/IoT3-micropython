import simpleWifi
import sys
import usocket
from machine import Pin,PWM

PORT=7950
LED1=21
s=None
pwm=None

# led initialiseren
pwm = PWM(Pin(LED1),freq=100)

# wifi object aanmaken
myWifi = simpleWifi.Wifi()
# connecteren met wifi
if not(myWifi.open()):
    print("Probleem met wifi")    
    myWifi.get_status()
    sys.exit()

myWifi.get_status()

try:
    addr = usocket.getaddrinfo('0.0.0.0',PORT)[0][-1]
    s = usocket.socket()
    s.bind(addr)
    s.listen(1)
    while True:
        c,caddr = s.accept()
        data = c.recv(4) 
        intensity = int(data) #duty cycle 0-100
        print('Connectie met {} - duty cycle {} %'.format(caddr,intensity)) 
        # intensiteit van LED1 aanpassen met PWM
        pwm.duty(intensity)
        c.close()
except Exception as e:
    print("Socket probleem %s"%e)
finally:
    if s != None:
        s.close()
    if pwm != None:
        pwm.deinit()
    myWifi.close()
        
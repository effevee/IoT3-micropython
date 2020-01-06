import simpleWifi
import sys
import usocket
import utime
import urandom

PORT=9700
#SERVER_ADR="172.24.0.122"
SERVER_ADR="192.168.1.22"
s=None

# wifi object aanmaken
myWifi = simpleWifi.Wifi()
# connecteren met wifi
if not(myWifi.open()):
    print("Probleem met wifi")    
    myWifi.get_status()
    sys.exit()

myWifi.get_status()

try:
    s = usocket.socket()
    s.connect(usocket.getaddrinfo(SERVER_ADR,PORT)[0][-1])
    while True:
        # stuur IP adres
        IP_DATA = myWifi.get_IPdata()
        msg = "IP:"+IP_DATA[0]+"\n"
        s.write(msg)
        # stuur random getal
        RND_GETAL = urandom.randint(0,20)
        msg = "RANDOM:"+str(RND_GETAL)+"\n"
        s.write(msg)
        utime.sleep(1)
except Exception as e:
    print("Socket probleem %s"%e)
finally:
    if s != None:
        s.close()
    myWifi.close()
        
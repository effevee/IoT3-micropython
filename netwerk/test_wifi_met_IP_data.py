import simpleWifi
import utime

# wifi object aanmaken
myWifi = simpleWifi.Wifi()
# connecteren met wifi
if myWifi.open():
    print("Verbonden")
    # toon IP adres
    print(myWifi.get_IPdata())
    # slapen gedurende 2 min
    utime.sleep(120)
else:
    print("Probleem met wifi")

# als wifi status > 0
if myWifi.get_status()>0:
    # wifi afsluiten
    myWifi.close()
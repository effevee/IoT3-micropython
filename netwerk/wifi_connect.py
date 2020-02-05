import simpleWifi

# wifi object aanmaken
myWifi = simpleWifi.Wifi()
# connecteren met wifi
if myWifi.open():
    print("Verbonden")
    # toon IP adres
    print(myWifi.get_IPdata())
else:
    print("Probleem met wifi")

#myWifi.get_status()

import simpleWifi

# wifi object aanmaken
myWifi = simpleWifi.Wifi()

# connecteren met wifi
myWifi.open()

myWifi.get_IPdata()

#myWifi.close()
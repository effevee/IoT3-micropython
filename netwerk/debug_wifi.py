import network

SSID = '<SSID>'
PWD = '<PWD>'

net = network.WLAN(network.STA_IF)
net.active(True)
if not net.isconnected():
    net.connect(SSID, PWD)
    while not net.isconnected():
        pass

print(net.isconnected())
print(net.ifconfig())

#net.disconnect()
import network

SSID = 'DS9'
PWD = 'TrustN01TrustN01'

net = network.WLAN(network.STA_IF)
net.active(True)
if not net.isconnected():
    net.connect(SSID, PWD)
    while not net.isconnected():
        pass

print(net.isconnected())
print(net.ifconfig())

#net.disconnect()
# Do not use this code in real projects! Read
# http_server_simplistic_commented.py for details.
import network
import usocket as socket




# connect to wifi network
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect('<SSID>', '<PWD>')
# wait for wifi connection
while not wifi.isconnected():
    pass
# print connection details
print('Wifi connection successful')
print(wifi.ifconfig())



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 80))
s.listen(1)
print("Listening, connect your browser to http://<this_host>/")

counter = 0
while True:
    conn, addr = s.accept()
    request = conn.recv(1024)
    print("Request")
    print(request.decode('utf-8'))
    counter += 1
    response = (str) ("""<html><body>Hello """ + str(counter) + """ from MicroPython!</body></html>""")
    print(response)
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()

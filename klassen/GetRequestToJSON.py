import usocket as socket
import ujson
# from simpleWifi import Wifi

def http_get(url):
    result = ''
    # 3x splitsen op /
    _, _, host, path = url.split('/', 3)
    # IP adres van webserver opvragen
    addr = socket.getaddrinfo(host, 80)[0][-1]
    # maken van socket instance
    s = socket.socket()
    # connectie maken met webserver
    s.connect(addr)
    # vraag verzenden naar webserver
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(100)
        if data:
            result += str(data, 'utf8')
        else:
            return result
    s.close()
    

def toJson(string):
    # zoek index van begin json string
    pos = string.index("[{")
    # haal json string uit string vanaf pos
    jsString = string[pos:-1]
    # maak json object
    return ujson.loads(jsString)
    

# # testcode
# url = 'http://download.waterinfo.be/tsmdownload/KiWIS/KiWIS?service=kisters&type=queryServices&request=getTimeseriesValues&datasource=1&format=json&ts_id=35031042,34999042&metadata=true&period=P12h'
# wf = Wifi()
# status = wf.open()
# print(status)
# if status:
#     # open waterinfo neerslagdata
#     res = http_get(url)
#     jsObj = toJson(res)
#     print(jsObj[0]["station_name"])
#     for m in jsObj[0]["data"]:
#         print(m)
# else:
#     print("Probleem met wifi")

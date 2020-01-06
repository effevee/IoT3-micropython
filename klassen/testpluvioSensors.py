from pluvioSensors import pluvioWebWaterInfo
import sys

url = "http://download.waterinfo.be/tsmdownload/KiWIS/KiWIS?service=kisters&type=queryServices&request=getTimeseriesValues&datasource=1&format=json&ts_id=35031042,34999042&metadata=true&period=P24h"

pluvio1 = pluvioWebWaterInfo(url, "waterinfo.be neerslag laatste 24 uur", True)

res = pluvio1.start()
if res[0] == -1:
    print('probleem starten sensor')
    sys.exit()

res = pluvio1.meet()
print("%s -> %0.3f mm"%(pluvio1.getInfo(), res[1]))

pluvio1.stop()
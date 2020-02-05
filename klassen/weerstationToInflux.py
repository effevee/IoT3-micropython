from tempSensors import tempNTC3950, tempDHT11
from humSensors import humDHT11
from pluvioSensors import pluvioWebWaterInfo
import time
from influxdbTools import influxdbPutData


# rij voor de sensoren en statussen
sens = []
stats = []
url = "http://download.waterinfo.be/tsmdownload/KiWIS/KiWIS?service=kisters&type=queryServices&request=getTimeseriesValues&datasource=1&format=json&ts_id=35031042,34999042&metadata=true&period=P24h"

# maken instance voor influxdb
influx = influxdbPutData("172.24.0.100", 8086, "weerstat_frank", "weerstation", "device", "waarde", debug=True)

# maak van instances en plaatsen in rij sens
hum1 = humDHT11(23, 'DHT11 humidity', False)
sens.append(hum1)

temp1 = tempDHT11(23, 'DHT11 temperature', False)
sens.append(temp1)

temp2 = tempNTC3950(36, 100000, 100000, 'NTC 3950-100K', False)
sens.append(temp2)

pluvio1 = pluvioWebWaterInfo(url, "waterinfo.be neerslag laatste 24 uur", False)
sens.append(pluvio1)

# opstarten van de sensoren
for s in sens:
    res = s.start()
    stats.append(res[0])
    
# de sensoren laten meten
try:
    while True:
        for x in range(0, len(sens)):
            # geen probleem bij opstart sensor
            if stats[x] >= 0:
                # meten
                res = sens[x].meet()
                # tonen resultaat
                print(sens[x].getInfo()+":"+str(res[1]))
                # datastructuur influx db opvullen
                influx.makeDataStringFieldisNumber(sens[x].getInfo(), res[1])
        # data wegschrijven naar influx db
        influx.writeToInfluxdb()
        # wachten voor volgende metingen
        time.sleep(20)

except Exception as E:
    print("probleem bij meten ", E)

finally:
    for x in range(0, len(sens)):
        # als sensor goed is opgestart
        if stats[x] >= 0:
            # sensor stoppen
            sens[x].stop()
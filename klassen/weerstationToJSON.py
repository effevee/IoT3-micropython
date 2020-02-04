from tempSensors import tempNTC3950, tempDHT11
from humSensors import humDHT11
from pluvioSensors import pluvioWebWaterInfo
import time
from jsonLog import dataJsonFile
from tijd import localTime


# rij voor de sensoren en statussen
sens = []
stats = []
url = "http://download.waterinfo.be/tsmdownload/KiWIS/KiWIS?service=kisters&type=queryServices&request=getTimeseriesValues&datasource=1&format=json&ts_id=35031042,34999042&metadata=true&period=P24h"

# maken instance voor dataJsonFile
jf = dataJsonFile('weerstat_frank.json', debug=True)

# maak instance voor localTime en initaliseer
lt = localTime(+1, debug=False)
lt.startInternetTime()

# maak van instances en plaatsen in rij sens
hum1 = humDHT11(23, 'DHT11 humidity', debug=False)
sens.append(hum1)

temp1 = tempDHT11(23, 'DHT11 temperature', debug=False)
sens.append(temp1)

temp2 = tempNTC3950(36, 10000, 100000, 'NTC 3950-100K', debug=False)
sens.append(temp2)

pluvio1 = pluvioWebWaterInfo(url, "waterinfo.be neerslag laatste 24 uur", debug=False)
sens.append(pluvio1)

# opstarten van de sensoren
for s in sens:
    res = s.start()
    stats.append(res[0])
    print(s.teller)
    
# de sensoren laten meten
try:
    while True:
        # json file openen
        if jf.openFile(bToevoegen=True):
            # door sensor lijst lopen
            for x in range(0, len(sens)):
                # geen probleem bij opstart sensor
                if stats[x] >= 0:
                    # meten
                    res = sens[x].meet()
                    # meting gelukt
                    if res[0] >= 0:
                        # tonen resultaat
                        tijd = lt.getLocalTime()[1]
                        info = sens[x].getInfo()
                        waarde = res[1]
                        print('%s - %s -> %s'%(tijd, info, str(waarde)))
                        # resultaat in json file
                        jf.schrijf(tijd, info, waarde)
            # json bestand sluiten
            jf.closeFile()
            # 15 min wachten voor volgende metingen
            time.sleep(900)

except Exception as E:
    print("probleem bij sensor, tijd of json ", E)

finally:
    for x in range(0, len(sens)):
        # als sensor goed is opgestart
        if stats[x] >= 0:
            # sensor stoppen
            sens[x].stop()
            print(s.teller)
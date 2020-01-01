from sensor import Sensor
from simpleWifi import Wifi
from GetRequestToJSON import http_get, toJson


class pluvioWebWaterInfo(Sensor):
    
    ''' neerslaggegevens via webservice van waterinfo.be '''
    
    def __init__(self, query, info, debug=False):
        super().__init__(info, debug)
        self.__query = query
        self.wf = None
    
    def start(self):
        try:
            self.wf = Wifi()
            if self.wf.open():
                Sensor.teller +=1
                return (0, 1)
            else:
                return (-1, -1)
        except Exception as E:
            if self.debug:
                print("fout bij opstarten van wifi", E)
            return (-1, -1)
    
    def meet(self):
        try:
            neerslagStations = []
            # haal resultaat van server (string)
            res = http_get(self.__query)
            # zet string om in JSON object
            jsObj = toJson(res)
            # aantal stations
            numStations = len(jsObj)
            # lopen door de stations
            for x in range(0, numStations):
                # ophalen data station
                stData = jsObj[x]["data"]
                neerslagWaarde = 0
                # lopen door de rij met data
                for d in stData:
                    # soms zit er geen waarde in
                    if d[-1] != None:
                        neerslagWaarde += d[-1]
                # per station de neerslag waarde toevoegen           
                neerslagStations.append(neerslagWaarde)        
            # gemiddelde neerslag van alle stations
            if numStations > 0:
                return (0, sum(neerslagStations)/numStations)
            else:
                return (-1, -1)
        except Exception as E:
            if self.debug:
                print("fout bij meten van neerslag", E)
            return (-1, -1)
    
    def stop(self):
        try:
            self.wf.close()
            if Sensor.teller > 0:
                Sensor.teller -= 1
            return (0, 1)
        except Exception as E:
            if self.debug:
                print("fout bij stoppen van wifi")
                print(E)
            return (-1, -1)

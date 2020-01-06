from sensor import Sensor
from machine import Pin
import utime
import dht

class humDHT11(Sensor):
    
    ''' De DHT11 is een digitale temperatuur en vochtigheidsensor. De sensor is vrij eenvoudig te gebruiken
        maar vereist een zorgvuldige timing om data te lezen. Dit is echter opgevangen via een bestaande
        bibliotheek. Opgelet : laat 2 seconden tussen de metingen! '''
    
    def __init__(self, pinDHT, info, debug=False):
        super().__init__(info,debug)
        self.__dht = None
        self.__pin = pinDHT
    
    def start(self):
        try:
            self.__dht = dht.DHT11(Pin(self.__pin))
            if self.debug == True:
                print("DHT11 is gestart")
            return (0, 1)
        except Exception as E:
            if self.debug == True:
                print("fout bij opstart van DHT11")
                print(E)
            return (-1, -1)
    
    def meet(self):
        try:
            somHum = 0
            for j in range(0,5):
                self.__dht.measure()
                somHum += self.__dht.humidity()
                utime.sleep(1)
            gemHum = somHum / 5
            return (0, gemHum)
        except Exception as E:
            if self.debug:
                print("fout bij meten van DHT11")
                print(E)
            return (-1, -1)
    
    def stop(self):
        try:
            del self.__dht
            self.__info = ""
            if self.debug == True:
                print("DHT11 is gestopt")
            return (0, 1)
        except Exception as E:
            if self.debug:
                print("fout bij stoppen van DHT11")
                print(E)
            return (-1, -1)

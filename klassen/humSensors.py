from sensor import Sensor
from machine import Pin, I2C
import utime
import dht
import am2320


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
            Sensor.teller +=1
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
            if Sensor.teller > 0:
                Sensor.teller -= 1
            return (0, 1)
        except Exception as E:
            if self.debug:
                print("fout bij stoppen van DHT11")
                print(E)
            return (-1, -1)
        

class humAM2320(Sensor):
    
    ''' De AM2320 is een digitale temperatuur en vochtigheidsensor met een I2C interface.
        De sensor is vrij eenvoudig te gebruiken maar vereist een zorgvuldige timing om data te lezen.
        Dit is echter opgevangen via de bestaande bibliotheek am2320 die je via upip op kan laden.'''
    
    def __init__(self, pinSCL, pinSDA, info, debug=False):
        super().__init__(info,debug)
        self.__scl = pinSCL
        self.__sda = pinSDA
        self.__i2c = None
        self.__am2320 = None
    
    def start(self):
        try:
            self.__i2c = I2C(scl = Pin(self.__scl), sda = Pin(self.__sda))
            self.__am2320 = am2320.AM2320(self.__i2c)
            if self.debug == True:
                print("AM2320 is gestart")
            Sensor.teller +=1
            return (0, 1)
        except Exception as E:
            if self.debug == True:
                print("fout bij opstart van AM2320")
                print(E)
            return (-1, -1)
    
    def meet(self):
        try:
            somHum = 0
            humOK = 0
            for j in range(0,5):
                self.__am2320.measure()
                hum = self.__am2320.humidity()
                if self.debug:
                    print(hum)
                if hum != 32.0:
                    # enkel goede metingen gebruiken
                    somHum += hum
                    humOK += 1
                utime.sleep(1)
            if humOK == 0:
                # geen enkele goede meting
                return (-1, -1)
            else:
                gemHum = somHum / humOK
                return (0, gemHum)
        except Exception as E:
            if self.debug:
                print("fout bij meten van AM2320")
                print(E)
            return (-1, -1)
    
    def stop(self):
        try:
            del self.__am2320
            del self.__i2c
            self.__info = ""
            if self.debug == True:
                print("AM2320 is gestopt")
            if Sensor.teller > 0:
                Sensor.teller -= 1
            return (0, 1)
        except Exception as E:
            if self.debug:
                print("fout bij stoppen van AM2320")
                print(E)
            return (-1, -1)

from sensor import Sensor
from machine import Pin, ADC, I2C
import utime
import dht
import math
import onewire
import ds18x20
import am2320


class tempNTC3950(Sensor):
    
    ''' De NTC 3950 thermistor is een analoge sensor waarbij de weerstand daalt
        bij stijgende temperatuur. NTC staat voor Negatieve Temperatuur Coefficient '''
    
    def __init__(self, pinADC, waardeWeerstand, waardeNTC, info, debug=False):
        super().__init__(info,debug)
        self.__pinADC = pinADC
        self.__weerstand = waardeWeerstand
        self.__weerstandNTC = waardeNTC
        self.__ntc = None
    
    def start(self):
        try:
            self.__ntc = ADC(Pin(self.__pinADC))
            self.__ntc.atten(ADC.ATTN_11DB)
            if self.debug == True:
                print("ntc3950 is gestart")
            return (0, 1)
        except Exception as E:
            if self.debug == True:
                print("fout bij het starten van ntc3950")
                print(E)
            return (-1, -1)
    
    def meet(self):
        somV0 = 0
        try:
            for j in range(0,5):
                somV0 += self.__ntc.read()
                utime.sleep_ms(20)
            gemV0 = 3.3 * float(somV0) / (5 * 4095)#spanning over weerstand
            if self.debug:
                print(somV0)
                print(gemV0)
            ntcWeerstand = self.__weerstand * (3.3 / gemV0 - 1)#Weerstand van de ntc
            if self.debug:
                print(ntcWeerstand)
            #temperatuur met vereenvoudigde Steinhart formule 1/T = 1/T0 + 1/3950ln(R/R0) (met T in Kelvin)
            resSteinhart = 1.0 / 298.15 + (1.0 / 3950.0) * math.log(ntcWeerstand / self.__weerstandNTC)
            temp = 1.0 / resSteinhart - 273.0
            return (1, temp)
        except Exception as E:
            if self.debug == True:
                print("fout bij meten van ntc3950")
                print(E)
            return (-1, -1)
    
    def stop(self):
        try:
            del self.__ntc
            if self.debug == True:
                print("ntc3950 is gestopt")
            return (0, 1)
        except Exception as E:
            print("fout bij stoppen van ntc3950")
            print(E)
            return (-1, -1)
            


class tempDHT11(Sensor):
    
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
            return (0, 1, 1)
        except Exception as E:
            if self.debug == True:
                print("fout bij opstart van DHT11")
                print(E)
            return (-1, -1, -1)
    
    def meet(self):
        try:
            somTemp = 0
            somHum = 0
            for j in range(0,5):
                self.__dht.measure()
                somTemp += self.__dht.temperature()
                somHum += self.__dht.humidity()
                utime.sleep(1)
            gemTemp = somTemp / 5
            gemHum = somHum / 5
            return (0, gemTemp, gemHum)
        except Exception as E:
            if self.debug:
                print("fout bij meten van DHT11")
                print(E)
            return (-1, -1, -1)
    
    def stop(self):
        try:
            del self.__dht
            self.__info = ""
            if self.debug == True:
                print("DHT11 is gestopt")
            return (0, 1, 1)
        except Exception as E:
            if self.debug:
                print("fout bij stoppen van DHT11")
                print(E)
            return (-1, -1, -1)


class tempDHT22(Sensor):
    
    ''' De DHT22 is een digitale temperatuur en vochtigheidsensor die nauwkeuriger is dan de DHT11.
        De sensor is vrij eenvoudig te gebruiken maar vereist een zorgvuldige timing om data te lezen.
        Dit is echter opgevangen via een bestaande bibliotheek. Opgelet : laat 2 seconden tussen de metingen! '''
    
    def __init__(self, pinDHT, info, debug=False):
        super().__init__(info,debug)
        self.__dht = None
        self.__pin = pinDHT
    
    def start(self):
        try:
            self.__dht = dht.DHT22(Pin(self.__pin))
            if self.debug == True:
                print("DHT22 is gestart")
            return (0, 1, 1)
        except Exception as E:
            if self.debug == True:
                print("fout bij opstart van DHT22")
                print(E)
            return (-1, -1, -1)
    
    def meet(self):
        try:
            somTemp = 0
            somHum = 0
            for j in range(0,5):
                self.__dht.measure()
                somTemp += self.__dht.temperature()
                somHum += self.__dht.humidity()
                utime.sleep(1)
            gemTemp = somTemp / 5
            gemHum = somHum / 5
            return (0, gemTemp, gemHum)
        except Exception as E:
            if self.debug:
                print("fout bij meten van DHT122")
                print(E)
            return (-1, -1, -1)
    
    def stop(self):
        try:
            del self.__dht
            self.__info = ""
            if self.debug == True:
                print("DHT22 is gestopt")
            return (0, 1, 1)
        except Exception as E:
            if self.debug:
                print("fout bij stoppen van DHT22")
                print(E)
            return (-1, -1, -1)


class tempLM35(Sensor):
    
    ''' LM35 is een analoge temperatuur sensor met een lineair
        verloop tussen 0°C en 150°C. 0°C komt overeen met 0 mV.
        De temperatuur stijging is 10mV/°C '''
        
    def __init__(self, pinADC, info, debug=False):
        super().__init__(info,debug)
        self.__pinADC = pinADC
        self.__lm35 = None
    
    def start(self):
        try:
            self.__lm35 = ADC(Pin(self.__pinADC))
            self.__lm35.atten(ADC.ATTN_11DB)
            if self.debug == True:
                print("LM35 is gestart")
            return (0, 1)
        except Exception as E:
            if self.debug == True:
                print("fout bij het starten van LM35")
                print(E)
            return (-1, -1)
    
    def meet(self):
        somV0 = 0
        try:
            for j in range(0,5):
                somV0 += self.__lm35.read()
                utime.sleep_ms(20)
            gemV0 = 5.0 * float(somV0) / (5 * 4095)#spanning over weerstand
            if self.debug:
                print(somV0)
                print(gemV0)
            # 10 mV/°C
            temp = gemV0 * 1000.0 / 10.0
            return (1, temp)
        except Exception as E:
            if self.debug == True:
                print("fout bij meten van LM35")
                print(E)
            return (-1, -1)
    
    def stop(self):
        try:
            del self.__lm35
            if self.debug == True:
                print("LM35 is gestopt")
            return (0, 1)
        except Exception as E:
            print("fout bij stoppen van LM35")
            print(E)
            return (-1, -1)


class tempDS18x20(Sensor):
    
    ''' De DS18B20 is een digitale temperatuur sensor die met het onewire protocol
        uitgelezen wordt. Iedere sensor heeft een unieke 64 bit code waardoor de ESP
        verschillende van deze sensors kan uitlezen via slechts 1 GPIO pin
        Opgelet : deze klasse leest slechts de 1ste sensor uit ! '''
    
    def __init__(self, pinDS, info, debug=False):
        super().__init__(info,debug)
        self.__pinDS = pinDS
        self.__DS = None
        self.__roms = [] # lijst gevonden sensoren
        
    def start(self):
        try:
            self.__DS = ds18x20.DS18X20(onewire.OneWire(Pin(self.__pinDS)))
            self.__roms = self.__DS.scan()
            if self.debug == True:
                print("DS18B20 is gestart")
                print("Gevonden sensor(en): ", self.__roms)
            return (0, 1)
        except Exception as E:
            if self.debug == True:
                print("fout bij opstart van DS18B20")
                print(E)

    def meet(self):
        somTemp = 0
        gemTemp = 0
        try:
            for j in range(0,5):
                self.__DS.convert_temp()
                utime.sleep_ms(750)
                somTemp += self.__DS.read_temp(self.__roms[0])
            gemTemp = float(somTemp) / 5
            if self.debug:
                print(somTemp)
                print(gemTemp)
            return (1, gemTemp)
        except Exception as E:
            if self.debug == True:
                print("fout bij meten van DS18B20")
                print(E)
            return (-1, -1)
    
    def stop(self):
        try:
            del self.__DS
            self.__roms = []
            if self.debug == True:
                print("DS18B20 is gestopt")
            return (0, 1)
        except Exception as E:
            print("fout bij stoppen van DS18B20")
            print(E)
            return (-1, -1)
        

class tempAM2320(Sensor):
    
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
            return (0, 1, 1)
        except Exception as E:
            if self.debug == True:
                print("fout bij opstart van AM2320")
                print(E)
            return (-1, -1, -1)
    
    def meet(self):
        try:
            somTemp = 0
            somHum = 0
            for j in range(0,5):
                self.__am2320.measure()
                somTemp += self.__am2320.temperature()
                somHum += self.__am2320.humidity()
                utime.sleep(1)
            gemTemp = somTemp / 5
            gemHum = somHum / 5
            return (0, gemTemp, gemHum)
        except Exception as E:
            if self.debug:
                print("fout bij meten van AM2320")
                print(E)
            return (-1, -1, -1)
    
    def stop(self):
        try:
            del self.__am2320
            del self.__i2c
            self.__info = ""
            if self.debug == True:
                print("AM2320 is gestopt")
            return (0, 1, 1)
        except Exception as E:
            if self.debug:
                print("fout bij stoppen van AM2320")
                print(E)
            return (-1, -1, -1)


import machine
import utime
import simpleStat

class distanceHCSR04:
    
    def __init__(self,trigPin,echoPin,aantalMetingen=5,snelheidGeluid=434):
        """constructor HC-SR04 sensor"""
        self.trigPin = trigPin
        self.trig = None         # om het pin object van de trigger in te stoppen
        self.echoPin = echoPin
        self.echo = None         # om het pinobject van de echo in te stoppen
        self.snelheid = snelheidGeluid
        self.timeout = 30        # timeout (ms) komt ongeveer overeen met 5m
        self.aantalMetingen = aantalMetingen
        self.debug = True
        
    def start(self):
        """Initialisatie HCSR04 sensor"""
        try:
            self.trig = machine.Pin(self.trigPin,machine.Pin.OUT)
            self.trig.value(0)
            self.echo = machine.Pin(self.echoPin,machine.Pin.IN)
            return True
        except Exception as E:
            if self.debug:
                print("HC-SR04 start fout: ",E)
            return False
        
    def meet1Maal(self):
        """Meet 1 afstand (cm) met de HC-SR04 sensor"""
        try:
            # startpuls trigger 10 us hoog
            self.trig.value(1)
            utime.sleep_us(10)
            self.trig.value(0)
            # meet tijd dat echo puls hoog blijft
            t = machine.time_pulse_us(self.echo,1,self.timeout*1000)
            if t < 0:
                return -1
            # return afstand
            return self.snelheid * t * 100 / (2 * 1000 * 1000) # in cm
        except Exception as E:
            if self.debug:
                print("HC-SR04 meet1Maal fout: ",E)
            return -1
            
    def meet(self):
        """Meet afstand met de HC-SR04 sensor"""
        try:
            tel = 0
            meetwaarden = []
            # lus metingen
            while tel < self.aantalMetingen:
                waarde = self.meet1Maal()
                if waarde > 0:
                    meetwaarden.append(waarde)
                # teller ophogen
                tel+=1
                # wachten voor volgende meting
                utime.sleep_ms(self.timeout*2)
            return simpleStat.AvgCleanList(meetwaarden)[1]
        except Exception as E:
            if self.debug:
                print("HC-SR04 meet fout: ",E)
            return -1
    
    def stop(self):
        """Stoppen van de HC-SR04 sensor"""
        try:
            del self.trig
            del self.echo
            return True
        except Exception as E:
            if self.debug:
                print("HC-SR04 stop fout: ",E)
            return False

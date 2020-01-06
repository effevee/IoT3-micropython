class Sensor:
#OPM privaat (__) werkt niet bij micropython
    
    def __init__(self,info,debug=False):
        self.__info = info
        self.debug = debug
    
    def start(self):#pins toevoegen in child
        pass
    
    def meet(self):#meet implementeren in child
        pass
    
    def stop(self):#pins verwijderen in child
        pass
    
    def getInfo(self):
        return self.__info
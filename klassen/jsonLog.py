import ujson

class meetData:
    """structuur om meetdata in te plaatsen"""
    
    def __init__(self,timestamp,info,waarde):
        self.t = timestamp
        self.info = info
        self.val = waarde
    
class dataJsonFile:
    """toevoegen van data in een json file of data uit een json file halen"""
    
    def __init__(self,locatie,debug=False):
        self.__loc = locatie
        self.__file = None
        self.debug = debug
    
    def openFile(self,bToevoegen=True):
        try:
            methode = "r"
            if bToevoegen:
                methode = "a"
            self.__file = open(self.__loc,methode)
            return True
        except Exception as E:
            if self.debug:
                print(E)
            return False
    
    def schrijf(self,tijd,info,waarde):
        try:
            obj = meetData(tijd,info,waarde)
            ujson.dump(obj.__dict__,self.__file)
            self.__file.write("\n")
            return True
        except Exception as E:
            if self.debug:
                print(E)
            return False
    
    def closeFile(self):
        try:
            self.__file.close()
        except Exception as E:
            if self.debug:
                print(E)
            return False
    
import machine
import utime

class HPDL1414:
    
    def __init__(self, ds0, ds1, da0, da1, da2, da3, da4, da5, da6, wrp):
        """constructor HPDL-1414 display
           - 2 digit select pins to identify one of the 4 digits of the display
           - 7 data pins to identify the character to display
           - 1 write pin to identify if the display is on or off
           - built-in character set goes from ascii 32 (space) to ascii 95 (_)"""
        try:
            self.ds0 = ds0
            self.ds1 = ds1
            self.ds = [None, None]
            self.da0 = da0
            self.da1 = da1
            self.da2 = da2
            self.da3 = da3
            self.da4 = da4
            self.da5 = da5
            self.da6 = da6
            self.da = [None, None, None, None, None, None, None]
            self.wrp = wrp
            self.wr = None
            self.min_ascii = 32
            self.max_ascii = 95
            self.debug = True
        except Exception as E:
            if self.debug:
                print("HPDL-1414 __init__ fout: ",E)
            return False
        
    def start(self):
        """Initialise HPDL-1414 display"""
        try:
            # make pin objects
            self.ds[0] = machine.Pin(self.ds0, machine.Pin.OUT)
            self.ds[1] = machine.Pin(self.ds1, machine.Pin.OUT)
            self.da[0] = machine.Pin(self.da0, machine.Pin.OUT)
            self.da[1] = machine.Pin(self.da1, machine.Pin.OUT)
            self.da[2] = machine.Pin(self.da2, machine.Pin.OUT)
            self.da[3] = machine.Pin(self.da3, machine.Pin.OUT)
            self.da[4] = machine.Pin(self.da4, machine.Pin.OUT)
            self.da[5] = machine.Pin(self.da5, machine.Pin.OUT)
            self.da[6] = machine.Pin(self.da6, machine.Pin.OUT)
            self.wr = machine.Pin(self.wrp, machine.Pin.OUT)
            # initialise pin objects
            for d in range(0, 1):
                self.ds[d].value(0)
            for a in range(0, 6):
                self.da[a].value(0)
            self.wr.value(1)    
            return True
        except Exception as E:
            if self.debug:
                print("HPDL-1414 start fout: ",E)
            return False

    def show(self, on):
        """show/hide HPDL-1414 display"""
        try:
            utime.sleep_ms(1)
            if on:
                self.wr.value(0)
            else:
                self.wr.value(1)
            utime.sleep_ms(1)
            return True
        except Exception as E:
            if self.debug:
                print("HPDL-1414 show fout: ",E)
            return False
            
    def write_char(self, dig, char):
        """write character char on position digit of HPDL-1414"""
        try:
            # convert dig to binary list for digit select
            digit = []
            digit = [int(x) for x in list('{0:0b}'.format(dig))]
            if self.debug:
                print('digit select: ', dig, digit)
            # convert char to binary list for data input
            data = []
            data = [int(x) for x in list('{0:0b}'.format(ord(char)))]
            if len(data) < 7:
                data.insert(0, 0)
            if self.debug:
                print('data input: ', char, data)
            # write char to position dig on display
            self.show(False)
            for d in range(0,1):
                self.ds[d].value(digit[d])
            for a in range(0,6):
                self.da[a].value(data[a])
            self.show(True)    
            return True
        except Exception as E:
            if self.debug:
                print("HPDL-1414 write_char fout: ",E)
            return False
    
    def stop(self):
        """stoppen HPDL-1414 display"""
        try:
            self.show(False)
            del self.digit
            del self.data
            del self.write
            return True
        except Exception as E:
            if self.debug:
                print("HPDL-1414 stop fout: ",E)
            return False
        
import machine
import utime

class HPDL1414_p:

    """single HPDL-1414 display - parallel connections to µC - 10 pins required
       - 2 digit select pins to identify one of the 4 digits of the display
       - 7 data pins to identify the character to display
       - 1 write pin to control the setup of the display (active low)
       the built-in character set goes from ascii 32 (space) to ascii 95 (_)"""

    def __init__(self, ds0, ds1, da0, da1, da2, da3, da4, da5, da6, wrp, debug=True):
        """constructor single HPDL-1414 display """
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
            self.debug = debug
        
        except Exception as E:
            if self.debug:
                print("HPDL-1414 __init__ error: ",E)
        
    
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
            # clear display
            self.clear()
        
        except Exception as E:
            if self.debug:
                print("HPDL-1414 start error: ",E)

    
    def write_char(self, dig, char):
        """write char on position dig of HPDL-1414 display"""
        try:
            # check valid character
            if ord(char) < self.min_ascii or ord(char) > self.max_ascii:
                char = "?"
            # convert dig to binary list for digit select
            digit = []
            digit = [int(x) for x in list('{0:0b}'.format(dig))]
            if len(digit) < 2:
                digit.insert(0, 0)
            digit.reverse() # LSB first
             # convert char to binary list for data input
            data = []
            data = [int(x) for x in list('{0:0b}'.format(ord(char)))]
            if len(data) < 7:
                data.insert(0, 0)
            data.reverse()  # LSB first  
            if self.debug:
                print('digit: ', dig, digit, '\tdata: ', char, data)
            # set pins in right order to write char on display
            # step 1 : digit select
            for d in range(0, 2):
                self.ds[d].value(digit[d])
            # step 2 : write enable
            utime.sleep_us(15)
            self.wr.value(0)
            # step 3 : data for character
            for a in range(0, 7):
                self.da[a].value(data[a])
            # step 4 : write disable
            utime.sleep_us(60)
            self.wr.value(1)    
        
        except Exception as E:
            if self.debug:
                print("HPDL-1414 write_char error: ",E)
    
    
    def clear(self):
        """ clear HPDL-1414 display """
        for d in range(3, -1, -1):
            self.write_char(d, " ")
            
    
    def stop(self):
        """stop HPDL-1414 display"""
        try:
            self.clear()
            del self.ds
            del self.da
            del self.wr
        
        except Exception as E:
            if self.debug:
                print("HPDL-1414 stop error: ",E)


class HPDL1414_s:

    """multiple HPDL-1414 displays - serial connections to µC with 2 or more SN74HC595 shift register ICs - 3 pins required
       - 1 data pin (SN74HC595 SER pin 14) to input 8 bits of data
       - 1 clock pin (SN74HC595 SRCLK pin 11) to shift the data bits into the register
       - 1 latch pin (SN74HV595 RCLK pin 12) to copy the 8 data bits into the latch register and set the output pins
       
       the SN74HC595 shift registers are daisy chained :
       shift #1  shift #2  µController
       ========  ========  =========== 
        QH'    --> SER    --> gpio pin
        SRCLK  --> SRCLK  --> gpio pin
        RCLK   --> RCLK   --> gpio pin
        OE#    --> OE#    --> GND
        GND    --> GND    --> GND
        SRCLR# --> SRCLR# --> VCC
        VCC    --> VCC    --> VCC
       
       the HPDL-1414 displays are connected as follows :
       HPDL-1414  shift #1  shift #2
       =========  ========  ========
        D0 (all) --> QA
        D1 (all) --> QB
        D2 (all) --> QC
        D3 (all) --> QD
        D4 (all) --> QE
        D5 (all) --> QF
        D6 (all) --> QG
        A0 (all) -----------> QA
        A1 (all) -----------> QB
        WR (#0)  -----------> QC
        WR (#1)  -----------> QD
        WR (#2)  -----------> QE
        WR (#3)  -----------> QF
        WR (#4)  -----------> QG
        WR (#5)  -----------> QH
       more displays can be controlled by adding another daisy chained SN74HC595 shift register
       
       the built-in character of the HPDL1414 set goes from ascii 32 (space) to ascii 95 (_)"""

    def __init__(self, data_pin, clock_pin, latch_pin, nbr_displays=5, debug=True):
        """constructor multiple HPDL-1414 displays """
        try:
            self.data = data_pin
            self.clock = clock_pin
            self.latch = latch_pin
            if nbr_displays > 6:
                nbr_displays = 6
            self.displays = nbr_displays
            self.digits = nbr_displays * 4
            self.da = None
            self.cl = None
            self.la = None
            self.min_ascii = 32
            self.max_ascii = 95
            self.debug = debug
        
        except Exception as E:
            if self.debug:
                print("HPDL-1414 __init__ error: ",E)

    
    def start(self):
        """Initialise HPDL-1414 display"""
        try:
            # make pin objects
            self.da = machine.Pin(self.data, machine.Pin.OUT)
            self.cl = machine.Pin(self.clock, machine.Pin.OUT)
            self.la = machine.Pin(self.latch, machine.Pin.OUT)
            # initialise pin objects
            self.da.value(0)
            self.cl.value(0)
            self.la.value(0)
            # clear displays
            self.clear()
        
        except Exception as E:
            if self.debug:
                print("HPDL-1414 start error: ",E)

    
    def shift_data(self, data):
        """ helper function to put data (list of 16 bit values) in the shift registers and to the output pins
            the SN74HC595 shift registers will be filled as follows:
              shift register #1       shift register #2
            ======================= =======================
            QA QB QC QD QE QF QG QH QA QB QC QD QE QF QG QH <-- SN74HC595
             |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
             v  v  v  v  v  v  v  v  v  v  v  v  v  v  v  v
            D0 D1 D2 D3 D4 D5 D6  x A0 A1 W0 W1 W2 W3 W4 W5 <-- HPDL1414
            ======================= =======================
            15 14 13 12 11 10  9  8  7  6  5  4  3  2  1  0 <-- bit positions (shift in reverse order !!!)
        """
        # set latch low to begin shifting
        self.la.value(0)
        # shift bits from bit list into the shift registers
        for bit in data:
            self.cl.value(0)
            self.da.value(bit)
            self.cl.value(1)
        # set latch high to set data to output pins
        self.la.value(1)
        self.cl.value(0)
        self.da.value(0)


    def write_char(self, dig, char):
        """write char on position dig of HPDL-1414 display"""
        try:
            # check valid character
            if ord(char) < self.min_ascii or ord(char) > self.max_ascii:
                char = "?"
            # create write binary list
            write = [1]*6
            for w in range(self.displays):
                if (dig // 4) == w:
                    write[5 - w] = 0  # write bits are in reverse order on shift register
            # convert dig to binary list
            digit = []
            digit = [int(x) for x in list('{0:0b}'.format(3 - (dig % 4)))]  # digit bits are in reverse order on shift register
            if len(digit) < 2:
                digit.insert(0, 0)
             # convert char to binary list
            data = []
            data = [int(x) for x in list('{0:0b}'.format(ord(char)))]
            while len(data) < 8:
                data.insert(0, 0)
            # set pins in right order to write char on display
            # step 1 : digit select
            bits = [0]*16
            bits[0:6] = [1]*6   # write disable 
            bits[6:8] = digit   # digit select
            if self.debug:
                print('digit: ', dig, '\tcharacter: ', char, '\tset address  ', bits)
            self.shift_data(bits)
            # step 2 : write enable
            utime.sleep_us(15)
            bits[0:6] = write   # write enable
            if self.debug:
                print('digit: ', dig, '\tcharacter: ', char, '\twrite enable ', bits)
            self.shift_data(bits)
            # step 3 : data for character
            bits[8:16] = data   # character data
            if self.debug:
                print('digit: ', dig, '\tcharacter: ', char, '\tset character', bits)
            self.shift_data(bits)
            # step 4 : write disable
            utime.sleep_us(60)
            bits[0:6] = [1]*6   # write disable 
            if self.debug:
                print('digit: ', dig, '\tcharacter: ', char, '\twrite disable', bits)
            self.shift_data(bits)
        
        except Exception as E:
            if self.debug:
                print("HPDL-1414 write_char error: ",E)
            
    
    def clear(self):
        """ clear HPDL-1414 displays """
        for d in range(self.digits):
            self.write_char(d, " ")

    
    def stop(self):
        """stop HPDL-1414 display"""
        try:
            self.clear()
            del self.da
            del self.cl
            del self.la
        
        except Exception as E:
            if self.debug:
                print("HPDL-1414 stop error: ",E)

import HPDL1414display
import utime

# pins
DS0 = 17
DS1 = 16
DA0 = 32
DA1 = 33
DA2 = 25
DA3 = 26
DA4 = 27
DA5 = 14
DA6 = 12
WR0 = 19
WR1 = 18
WR2 = 5

# teststring
NBRDIGITS = 12
TEXT = "           ... LINSKE, GELUKKIG NIEUWJAAR EN VEEL FIETSGENOT GEWENST VANWEGE JE ALLERLIEFSTE COLLEGA ...           "
SCROLLDELAY = 100 # ms

# instantiate HPDL1414 displays
dp0 = HPDL1414display.HPDL1414_p(DS0, DS1, DA0, DA1, DA2, DA3, DA4, DA5, DA6, WR0, debug=False)
dp1 = HPDL1414display.HPDL1414_p(DS0, DS1, DA0, DA1, DA2, DA3, DA4, DA5, DA6, WR1, debug=False)
dp2 = HPDL1414display.HPDL1414_p(DS0, DS1, DA0, DA1, DA2, DA3, DA4, DA5, DA6, WR2, debug=False)

dp0.start()
dp1.start()
dp2.start()

try:
    # loop to display the scrolling teststring
    pos = 0
    while True:
        dp0.write_char(3, TEXT[pos])
        dp0.write_char(2, TEXT[pos+1])
        dp0.write_char(1, TEXT[pos+2])
        dp0.write_char(0, TEXT[pos+3])
        
        dp1.write_char(3, TEXT[pos+4])
        dp1.write_char(2, TEXT[pos+5])
        dp1.write_char(1, TEXT[pos+6])
        dp1.write_char(0, TEXT[pos+7])
        
        dp2.write_char(3, TEXT[pos+8])
        dp2.write_char(2, TEXT[pos+9])
        dp2.write_char(1, TEXT[pos+10])
        dp2.write_char(0, TEXT[pos+11])
        
        utime.sleep_ms(SCROLLDELAY)
        
        pos += 1
        if (pos + NBRDIGITS) > len(TEXT):
            pos = 0

except KeyboardInterrupt as e:
    print("programma onderbroken met Ctrl-C")
    
finally:
    # stop display
    dp0.stop()
    dp1.stop()
    dp2.stop()

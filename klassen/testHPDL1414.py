import HPDL1414display
import utime

# pins
DS0 = 25
DS1 = 33
DA0 = 26
DA1 = 27
DA2 = 14
DA3 = 12
DA4 = 0
DA5 = 4
DA6 = 13
WRI = 32

# teststring
TEXT = "    I LOVE MY HPDL-1414 DISPLAY ...                         "
SCROLLDELAY = 2000  # ms

# instantiate HPDL1414 display
display = HPDL1414display.HPDL1414(DS0, DS1, DA0, DA1, DA2, DA3, DA4, DA5, DA6, WRI)
display.start()

display.write_char(0,"A")

"""# loop to display the scrolling teststring
for pos in range(0, len(TEXT)-4):
    display.show(False)
    display.write_char(3, TEXT[pos])
    display.write_char(2, TEXT[pos+1])
    display.write_char(1, TEXT[pos+2])
    display.write_char(0, TEXT[pos+3])
    display.show(True)
    utime.sleep_ms(SCROLLDELAY)
    
"""    
    
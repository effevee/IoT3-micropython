import HPDL1414display
import utime

# pins
DATA = 19
CLOCK = 18
LATCH = 5

# teststring
TEXT = "           ... LINSKE, GELUKKIG NIEUWJAAR EN VEEL FIETSGENOT GEWENST VANWEGE JE ALLERLIEFSTE COLLEGA ...           "
#TEXT = "ABCDEFGHIJKL"
SCROLLDELAY = 200 # ms

# instantiate HPDL1414 displays
dp = HPDL1414display.HPDL1414_s(DATA, CLOCK, LATCH, 5, debug=False)

dp.start()

try:
    # loop to display the scrolling teststring
    pos = 0
    while True:
        for p in range(dp.digits):
            dp.write_char(p, TEXT[pos+p])
        
        utime.sleep_ms(SCROLLDELAY)
        
        pos += 1
        if (pos + dp.digits) > len(TEXT):
            pos = 0

except KeyboardInterrupt as e:
    print("programma onderbroken met Ctrl-C")
    
finally:
    # stop display
    dp.stop()

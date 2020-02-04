from machine import Pin, ADC
import utime

# variabelen
PIN_ADC = 36   # pin SVP
licht_waarden = []
fcalib = None

# ADC pin initialiseren
adc = ADC(Pin(PIN_ADC))
# 11 dB attenuation means full 0 - 3.3V range
adc.atten(adc.ATTN_11DB)

# calibratie donker
print('Dek de sensor af, de waarde wordt 10 maal gemeten')
utime.sleep(10)
for m in range(0,10):
    # lees lichtwaarden van 0 tot 4095 (12bit ADC)
    licht = adc.read()
    print('Meetwaarde: %d - Spanning: %0.2fV'%(licht, (licht*3.3/4095.0)))
    licht_waarden.append(licht)
    utime.sleep(0.5)

# calibratie licht
print('Richt de sensor naar het licht, de waarde wordt 10 maal gemeten')
utime.sleep(10)
for m in range(0,10):
    # lees lichtwaarden van 0 tot 4095 (12bit ADC)
    licht = adc.read()
    print('Meetwaarde: %d - Spanning: %0.2fV'%(licht, (licht*3.3/4095.0)))
    licht_waarden.append(licht)
    utime.sleep(0.5)

# toon waarden
print(licht_waarden)

# min en max opslaan in calibratie bestand
try:
    fcalib = open('calib_licht.txt','w')
    min_waarde = min(licht_waarden)
    max_waarde = max(licht_waarden)
    fcalib.write('min:'+str(min_waarde)+'\n')
    fcalib.write('max:'+str(max_waarde)+'\n')
    
except Exception as e:
    print('Probleem met bestand %s'%e)
    
finally:
    if fcalib != None:
        fcalib.close()

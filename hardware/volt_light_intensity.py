from machine import Pin, ADC
import utime

# variabelen
PIN_ADC = 36   # pin SVP

# ADC pin initialiseren
adc = ADC(Pin(PIN_ADC))
# 11 dB attenuation means full 0 - 3.3V range
adc.atten(adc.ATTN_11DB)

# min en max opslaan in calibratie bestand
try:
    # lus meetwaarden
    while True:
        # ophalen meetwaarde
        licht = adc.read()
        # berekenen procent
        spanning = 3.3 * licht / 4095
        # toon resultaat
        print('Meetwaarde: %d - Spanning: %0.2fV'%(licht,spanning))
        # even wachten
        utime.sleep_ms(1000)
    
except Exception as e:
    print('Probleem met bestand %s'%e)
    
finally:
    adc.deinit()
from machine import Pin, ADC
import utime

# variabelen
PIN_ADC = 36   # pin SVP
fcalib = None

# ADC pin initialiseren
adc = ADC(Pin(PIN_ADC))
# 11 dB attenuation means full 0 - 3.3V range
adc.atten(adc.ATTN_11DB)

# min en max opslaan in calibratie bestand
try:
    # ophalen limieten
    fcalib = open('calib_licht.txt','r')
    limieten = {}
    for line in fcalib.readlines():
        line=line.replace('\n','')
        koppel=line.split(':')
        limieten.update({koppel[0]:koppel[1]})
    fcalib.close()
    #print(limieten)
    min_waarde = int(limieten['min'])
    max_waarde = int(limieten['max'])
    
    # lus meetwaarden
    while True:
        # ophalen meetwaarde
        licht = adc.read()
        # berekenen procent
        procent_licht = 100.0 * (licht - min_waarde) / (max_waarde - min_waarde)
        # toon resultaat
        print('Meetwaarde: %d - Procent: %0.2f%%'%(licht,procent_licht))
        # even wachten
        utime.sleep_ms(1000)
    
except Exception as e:
    print('Probleem met bestand %s'%e)
    
finally:
    if fcalib != None:
        fcalib.close()
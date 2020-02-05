from tempSensors import tempNTC3950, tempDHT11, tempLM35, tempDS18x20, tempAM2320
from humSensors import humDHT11
import sys
import utime

# sensors instances
ntc = tempNTC3950(36, 10000, 100000, 'NTC 3950-100K', False)
dht = tempDHT11(23, 'DHT11 temp ', False)
dhv = humDHT11(23, 'DHT11 vocht ', False)

# sensors starten
res = ntc.start()
if res[0] == -1:
    print('probleem starten sensor')
    sys.exit()

res = dht.start()
if res[0] == -1:
    print('probleem starten sensor')
    sys.exit()

res = dhv.start()
if res[0] == -1:
    print('probleem starten sensor')
    sys.exit()


'''lm35 = tempLM35(39, 'LM35      ', False)
lm35.start()

ds18 = tempDS18x20(32, 'DS18B20   ', False)
ds18.start()

am1 = tempAM2320(22, 21, 'AM2320     ', False)
am1.start() '''

# meten
for i in range(0, 10):
    print('Meting #%d'%i)
    
    nt = ntc.meet()
    print('Sensor %s \t temperatuur %0.2f °C'%(ntc.getInfo(), nt[1]))
    
    dh = dht.meet()
    print('Sensor %s \t temperatuur %.0f °C'%(dht.getInfo(), dh[1]))
    
    dv = dhv.meet()
    print('Sensor %s \t temperatuur %.0f %%'%(dhv.getInfo(), dv[1]))

    utime.sleep(1)
    print(' ')
    '''lm = lm35.meet()
    print('Sensor %s \t temperatuur %0.2f °C'%(lm35.getInfo(), lm[1]))
    ds = ds18.meet()
    print('Sensor %s \t temperatuur %0.2f °C'%(ds18.getInfo(), ds[1]))
    am = am1.meet()
    print('Sensor %s \t temperatuur %0.2f °C \t vochtigheid %.0f %%'%(am1.getInfo(), am[1], am[2]))
    print(' ')'''

    
# sensors stoppen
ntc.stop()
dht.stop()
dhv.stop()
'''lm35.stop()
ds18.stop()
am1.stop()'''

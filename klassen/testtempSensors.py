from tempSensors import tempNTC3950, tempDHT11, tempLM35, tempDS18x20, tempAM2320
from humSensors import humDHT11, humAM2320
import sys
import utime

# sensors instances
ntc = tempNTC3950(36, 100000, 112000, 'NTC 3950-100K', False)
dh1 = tempDHT11(23, 'DHT11 temp ', False)
dh2 = humDHT11(23, 'DHT11 vocht ', False)
lm35 = tempLM35(39, 'LM35      ', True)
ds18 = tempDS18x20(32, 'DS18B20   ', False)
am1 = tempAM2320(22, 21, 'AM2320 temp ', False)
am2 = humAM2320(22, 21, 'AM2320 vocht ', False)

# sensors starten
res = ntc.start()
if res[0] == -1:
    print('probleem starten sensor')
    sys.exit()

res = dh1.start()
if res[0] == -1:
    print('probleem starten sensor')
    sys.exit()

res = dh2.start()
if res[0] == -1:
    print('probleem starten sensor')
    sys.exit()

res = lm35.start()
if res[0] == -1:
    print('probleem starten sensor')
    sys.exit()

res = ds18.start()
if res[0] == -1:
    print('probleem starten sensor')
    sys.exit()

res = am1.start()
if res[0] == -1:
    print('probleem starten sensor')
    sys.exit()

res = am2.start()
if res[0] == -1:
    print('probleem starten sensor')
    sys.exit()

# sensors metingen
for i in range(0, 10):
    print('Meting #%d'%i)
    print('Sensor %s \t %.2f °C'%(ntc.getInfo(), ntc.meet()[1]))
    print('Sensor %s \t %.2f °C'%(dh1.getInfo(), dh1.meet()[1]))
    print('Sensor %s \t %.0f %%'%(dh2.getInfo(), dh2.meet()[1]))
    print('Sensor %s \t %.2f °C'%(lm35.getInfo(), lm35.meet()[1]))
    print('Sensor %s \t %.2f °C'%(ds18.getInfo(), ds18.meet()[1]))
    print('Sensor %s \t %.2f °C'%(am1.getInfo(), am1.meet()[1]))
    print('Sensor %s \t %.0f %%'%(am2.getInfo(), am2.meet()[1]))
    print(' ')
    
# sensors stoppen
ntc.stop()
dh1.stop()
dh2.stop()
lm35.stop()
ds18.stop()
am1.stop()
am2.stop()

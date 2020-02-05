import ultraSoundSensor
import utime

TRIGPIN = 22
ECHOPIN = 23

afst_sensor = ultraSoundSensor.distanceHCSR04(TRIGPIN, ECHOPIN)
afst_sensor.start()

while True:
    d = int(afst_sensor.meet())
    if d < 4:
        break
    else:
        print('Afstand = %d cm'%d)
        utime.sleep(1)
    
afst_sensor.stop()
    

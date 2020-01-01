import ultraSoundSensor
import utime

TRIGPIN = 22
ECHOPIN = 23

afst_sensor = ultraSoundSensor.distanceHCSR04(TRIGPIN, ECHOPIN)
afst_sensor.start()

while True:
    print('Afstand = %d cm'%int(afst_sensor.meet()))
    utime.sleep(1)
    
afst_sensor.stop()
    

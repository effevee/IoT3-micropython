from machine import Pin,DAC
import utime
import wave

# variabelen
DAC_GPIO = 25

# initialiseren DAC
dac = DAC(Pin(DAC_GPIO))


def play(filename):
    f = wave.open(filename, 'r')
    total_frames = f.getnframes()
    framerate = f.getframerate()
    print(total_frames)
    print(framerate)

    for position in range(0, total_frames, framerate):
        f.setpos(position)
        for s in f.readframes(framerate):
            dac.write(s)
            utime.sleep_us(int(8000/framerate))
        #utime.sleep_us(1)
        

play('pcm0808m.wav')
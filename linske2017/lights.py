import machine
import neopixel
import utime
import ujson
import urandom
import math

# globale variabelen
class gvars:
    animation_schemes = ["solid", "chase", "smooth", "cycle", "bounce", "fade", "blank", "rgbloop","strobe",
                         "cyclon", "kitt2000", "twinkle", "sparkle", "runninglight", "rainbow", "comet"]
    animation = "bounce"
    periodMS = 250
    color_schemes = [
        ["regenboog", [[255,0,0], [255,127,0], [255,255,0], [0,255,0], [0,0,255], [75,0,130],[148,0,211]]],
        ["blauw-rood", [[0,0,255], [16,0,128], [32,0,64], [64,0,32], [128,0,16], [255,0,0]]],
        ["rood-groen", [[255,0,0], [128,16,0], [64,32,0], [32,64,0], [16,128,0], [0,255,0]]],
        ["blauw-wit", [[0,0,255], [16,16,255], [32,32,255], [64,64,255], [128,128,255], [255,255,255]]] ]
    color = "regenboog"
    colors = None
    mirror = True
    current_color = 0

# Static configuration that never changes
PIXEL_PIN   = machine.Pin(4, machine.Pin.OUT)  # Pin connected to the NeoPixels.
PIXEL_COUNT = 16                               # Number of NeoPixels.


# Mirror the colors to make a ramp up and ramp down with no repeated colors.
def mirror(values):
    # Add the input values in reverse order to the end of the array.
    # However slice off the very first and very last items (the [1:-1] syntax)
    # to prevent the first and last values from repeating.
    # For example an input of:
    #  [1, 2, 3]
    # Returns:
    #  [1, 2, 3, 2]
    # Instead of returning:
    #  [1, 2, 3, 3, 2, 1]
    # Which would duplicate 3 and 1 as you loop through the elements.
    values.extend(list(reversed(values))[1:-1])
    return values

# Linear interpolation helper:
def _lerp(x, x0, x1, y0, y1):
    return y0 + (x - x0) * ((y1 - y0)/(x1 - x0))

# Animation functions:
def blank(config, np, pixel_count):
    np.fill((0,0,0))
    np.write()

def solid(config, np, pixel_count):
    colors = config['colors']
    elapsed = utime.ticks_ms() // config['period_ms']
    current = elapsed % len(colors)
    np.fill(colors[current])
    np.write()

def chase(config, np, pixel_count):
    colors = config['colors']
    elapsed = utime.ticks_ms() // config['period_ms']
    for i in range(pixel_count):
        current = (elapsed+i) % len(colors)
        np[i] = colors[current]
    np.write()

def smooth(config, np, pixel_count):
    # Smooth pulse of all pixels at the same color.  Interpolates inbetween colors
    # for smoother animation.
    colors = config['colors']
    period_ms = config['period_ms']
    ticks = utime.ticks_ms()
    step = ticks // period_ms
    offset = ticks % period_ms
    color0 = colors[step % len(colors)]
    color1 = colors[(step+1) % len(colors)]
    color = (int(_lerp(offset, 0, period_ms, color0[0], color1[0])),
             int(_lerp(offset, 0, period_ms, color0[1], color1[1])),
             int(_lerp(offset, 0, period_ms, color0[2], color1[2])))
    np.fill(color)
    np.write()

def cycle(config, np, pixel_count):
    # current color
    colors = config['colors']
    # build iterate list
    pos = []
    pos.extend(range(0, pixel_count))
    # iterate
    for i in pos:
        np.fill(colors[gvars.current_color])
        np[i] = (0, 0, 0)
        np.write()
        utime.sleep_ms(config['period_ms'])
    # next color
    gvars.current_color += 1
    if gvars.current_color >= len(colors):
        gvars.current_color = 0
    
def bounce(config, np, pixel_count):
    # current color
    colors = config['colors']
    color = colors[gvars.current_color]
    # build iterate list
    pos = []
    pos.extend(range(0, pixel_count))
    pos.extend(list(reversed(pos))[1:-1])
    # iterate
    for i in pos:
        np.fill(colors[gvars.current_color])
        np[i] = (0, 0, 0)
        np.write()
        utime.sleep_ms(config['period_ms'])
    # next color
    gvars.current_color += 1
    if gvars.current_color >= len(colors):
        gvars.current_color = 0

def fade(config, np, pixel_count):
    # current color
    colors = config['colors']
    color = colors[gvars.current_color]
    r_step = color[0] // pixel_count
    g_step = color[1] // pixel_count
    b_step = color[2] // pixel_count
    # build iterate list
    pos = []
    pos.extend(range(0, pixel_count))
    pos.extend(list(reversed(pos))[1:-1])
    # iterate
    for i in pos:
        new_color = ((color[0] - (i * r_step), color[1] - (i * g_step), color[2] - (i * b_step)))
        np.fill(new_color)
        np.write()
        utime.sleep_ms(config['period_ms'])
    # next color
    gvars.current_color += 1
    if gvars.current_color >= len(colors):
        gvars.current_color = 0

def rgbloop(config, np, pixel_count):
    # build iterate list
    val = []
    val.extend(range(0, 255, 5))
    val.extend(list(reversed(val))[1:-1])
    # iterate colors
    for c in ['r', 'g', 'b']:
        # iterate values
        for i in val:
            if c == 'r':
                np.fill((i,0,0))
            elif c == 'g':
                np.fill((0,i,0))
            elif c == 'b':
                np.fill((0,0,i))
            np.write()
            utime.sleep_ms(config['period_ms'])
            
def strobe(config, np, pixel_count):
    for i in range(5):
        colors = config['colors']
        color = colors[gvars.current_color]
        np.fill(color)
        np.write()
        utime.sleep_ms(config['period_ms'])
        np.fill((0,0,0))
        np.write()
        utime.sleep_ms(config['period_ms'])
        gvars.current_color += 1
        if gvars.current_color >= len(colors):
            gvars.current_color = 0

def cylon(config, np, pixel_count):
    # current color
    colors = config['colors']
    color = colors[gvars.current_color]
    # build iterate list
    pos = []
    pos.extend(range(0, pixel_count-2))
    pos.extend(list(reversed(pos))[1:-1])
    # iterate
    for i in pos:
        np.fill((0,0,0))
        np[i] = (color[0] // 5, color[1] // 5, color[2] // 5)
        np[i+1] = (color[0], color[1], color[2])
        np[i+2] = np[i]
        np.write()
        utime.sleep_ms(config['period_ms'])
    # next color
    gvars.current_color += 1
    if gvars.current_color >= len(colors):
        gvars.current_color = 0
        
def kitt2000(config, np, pixel_count):
    # current color
    colors = config['colors']
    color = colors[gvars.current_color]
    # build iterate list
    pos = []
    pos.extend(range(0, (pixel_count//2)-2))
    pos.extend(list(reversed(pos))[1:-1])
    # iterate
    for i in pos:
        np.fill((0,0,0))
        np[i] = (color[0] // 5, color[1] // 5, color[2] // 5)
        np[pixel_count-i-1] = np[i]
        np[i+1] = (color[0], color[1], color[2])
        np[pixel_count-i-2] = np[i+1]
        np[i+2] = np[i]
        np[pixel_count-i-3] = np[i]
        np.write()
        utime.sleep_ms(config['period_ms'])
    # next color
    gvars.current_color += 1
    if gvars.current_color >= len(colors):
        gvars.current_color = 0

def twinkle(config, np, pixel_count):
    # current color
    colors = config['colors']
    color = colors[gvars.current_color]
    # iterate
    np.fill((0,0,0))
    for i in range(pixel_count // 3):
        pos = urandom.randint(0, pixel_count-1)
        np[pos] = (color[0], color[1], color[2])
    np.write()
    utime.sleep_ms(config['period_ms'])
    # next color
    gvars.current_color += 1
    if gvars.current_color >= len(colors):
        gvars.current_color = 0

def sparkle(config, np, pixel_count):
    # current color
    colors = config['colors']
    color = colors[gvars.current_color]
    # random pixel on
    pos = urandom.randint(0, pixel_count-1)
    np[pos] = (color[0], color[1], color[2])
    np.write()
    # wait
    utime.sleep_ms(config['period_ms'])
    # pixel off
    np[pos] = ((0,0,0))
    np.write()
    # next color
    gvars.current_color += 1
    if gvars.current_color >= len(colors):
        gvars.current_color = 0

def runninglight(config, np, pixel_count):
    # current color
    colors = config['colors']
    color = colors[gvars.current_color]
    # iterate with sine wave
    pos = 0
    for i in range(pixel_count*2):
        pos +=1
        for j in range(pixel_count):
            r = ((math.sin(j + pos) * 127 + 128) / 255) * color[0]
            g = ((math.sin(j + pos) * 127 + 128) / 255) * color[1]
            b = ((math.sin(j + pos) * 127 + 128) / 255) * color[2]
            np[j] = ((int(r), int(g), int(b)))
        np.write()
        utime.sleep_ms(config['period_ms'])
    # next color
    gvars.current_color += 1
    if gvars.current_color >= len(colors):
        gvars.current_color = 0

def rainbow(config, np, pixel_count):
    # 5 cycles for all colors
    for j in range(256*5):
        for i in range(pixel_count):
            color = wheel(((i * 256 // pixel_count) + j) & 255)
            np[i] = color
        np.write()
        utime.sleep_ms(config['period_ms'])

def wheel(wheelpos):
    r, g, b = 0, 0, 0
    if wheelpos < 85:
        r = wheelpos*3
        g = 255 - wheelpos*3
        b = 0
    elif wheelpos < 170:
        wheelpos -= 85
        r = 255 - wheelpos*3
        g = 0
        b = wheelpos*3
    else:
        wheelpos -= 170
        r = 0
        g = wheelpos*3
        b = 255 - wheelpos*3
    return (r,g,b)

def comet(config, np, pixel_count):
    # current color
    colors = config['colors']
    color = colors[gvars.current_color]
    # build iterate list
    pos = []
    pos.extend(range(0, pixel_count))
    # iterate
    for i in pos:
        np.fill((0,0,0))
        for j in range(4):
            r = color[0] // ((3-j)*5+1)
            g = color[1] // ((3-j)*5+1)
            b = color[2] // ((3-j)*5+1)
            p = (i + j) % pixel_count
            np[p] = (r, g, b)
        np.write()
        utime.sleep_ms(config['period_ms'])
    # next color
    gvars.current_color += 1
    if gvars.current_color >= len(colors):
        gvars.current_color = 0


# Initialize the neopixels and turn them off
np = neopixel.NeoPixel(PIXEL_PIN, PIXEL_COUNT)
np.fill((0,0,0))
np.write()

with open('config.json', 'r') as infile:
    config = ujson.load(infile)

# Determine the animation function to call
animation = globals().get(config['animation'], blank)

# Main loop

try:
    while True:
        animation(config, np, PIXEL_COUNT)
        utime.sleep(0.01)

except Exception as e:
    print('Problem with animation: %s' % e)

finally:
    np.fill((0,0,0))
    np.write()    


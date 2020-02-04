from machine import Pin
import neopixel
import network
import ujson
import utime
import urandom
import math
import sys
import uasyncio as asyncio


# Static configuration that never changes
PIXEL_PIN   = 4   # Pin connected to the NeoPixels.
ANIM_PIN    = 21  # Pin pushbutton for cycling animations
PIXEL_COUNT = 16  # Number of NeoPixels.
SSID        = '<SSID>'
WIFI_PW     = '<PWD>'

# globale variabelen
class gvars:
    animation_schemes = ["solid", "chase", "smooth", "cycle", "bounce", "fade", "rgbloop", "strobe", "cylon",
                         "kitt2000", "twinkle", "sparkle", "runninglight", "rainbow", "comet", "blank"]
    color_schemes = {
        "regenboog": [[255,0,0], [255,127,0], [255,255,0], [0,255,0], [0,0,255], [75,0,130],[148,0,211]],
        "kleurenwiel": [[255,0,0], [255,127,0], [255,255,0], [127,255,0], [0,255,0], [0,255,127], [0,255,255], [0,127,255], [0,0,255], [127,0,255], [255,0,255], [255,0,127]],
        "blauw-rood": [[0,0,255], [16,0,128], [32,0,64], [64,0,32], [128,0,16], [255,0,0]],
        "rood-groen": [[255,0,0], [128,16,0], [64,32,0], [32,64,0], [16,128,0], [0,255,0]],
        "blauw-wit": [[0,0,255], [16,16,255], [32,32,255], [64,64,255], [128,128,255], [255,255,255]] }
    current_color = 0


###########################################################################
# setup code
###########################################################################

# initialise neopixels
def init_neopixels(np_pin, np_count):
    # initialise neopixels
    np = neopixel.NeoPixel(Pin(np_pin, Pin.OUT), np_count)
    np.fill((0,0,0))
    np.write()
    return np

# initialise pushbutton
def init_animation_button(btn_pin):
    # initialise animation button
    btn = Pin(btn_pin, Pin.IN, Pin.PULL_UP)
    return btn

# connect ESP to wifi network if o-possible
def connect2wifi(ssid, wifi_pw):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        teller = 0
        print('Trying to connect to wireless network...')
        wlan.connect(ssid, wifi_pw)
        while not wlan.isconnected():
            teller += 1
            utime.sleep_ms(500)
            if teller < 20:
                pass
            else:
                break
    if wlan.isconnected():
        print('network config:', wlan.ifconfig())
        return wlan
    else:
        print('Could not connect to wireless network')
        return None

# get config from json file
def get_json_config():
    with open('config.json', 'r') as infile:
        config = ujson.load(infile)
    return config

###########################################################################
# web interface code
###########################################################################

# build web page
def web_page(config):
    html = '''<!DOCTYPE html>
<html>
<head>
  <title>Linskes luchtje</title>
  <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
</head>
<body>
  <div class="container">
    <div class="row">
      <div class="col-lg-8 col-lg-offset-2">
        <div class="jumbotron">
          <h1>Linskes luchtje</h1>
          <p class="lead">(c)2019 - Uwe liefste collega Effevee :P</p>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-lg-4 col-lg-offset-3">
        <form method="POST">
          <div class="form-group">
            <label for="animation">Animatie type</label>
            <select class="form-control" name="animation">''' + html_animation_options(config['animation']) + '''
            </select>
          </div>
          <div class="form-group">
            <label for="periodMS">Animatie snelheid (ms)</label>
            <input type="number" class="form-control" name="periodMS" value=''' + str(config['period_ms']) + '''>
          </div>
          <div class="form-group">
            <label for="colors">Kleurenschema</label>
            <select class="form-control" name="color_scheme">''' + html_colors_options(config['color_scheme']) + '''
            </select>
          </div>
          <div class="checkbox">
            <label>
              <input type="checkbox" name="mirror"''' + html_mirror(config['mirror_colors']) + '''>
              Kleuren spiegelen
            </label>
          </div>
          <button class="btn btn-lg btn-primary" type="submit" id="update">Update luchtje</button>
        </form>  
      </div>
    </div>
  </div>
</body>
</html>'''
    return html

# fill options of the animation select
def html_animation_options(animation):
    pos_selected = gvars.animation_schemes.index(animation)
    option_string = "\n"
    for i in range(len(gvars.animation_schemes)):
        if pos_selected == i:
            option_string += '<option value="' + gvars.animation_schemes[i] + '" selected>' + capitalize(gvars.animation_schemes[i]) + '</option>\n'
        else:
            option_string += '<option value="' + gvars.animation_schemes[i] + '">' + capitalize(gvars.animation_schemes[i]) + '</option>\n'
    return option_string
 
# fill options of the colors select
def html_colors_options(color):
    option_string = "\n"
    c_keys = list(gvars.color_schemes.keys())
    for i in range(len(c_keys)):
        if c_keys[i] == color:
            option_string += '<option value="' + c_keys[i] + '" selected>' + capitalize(c_keys[i]) + '</option>\n'
        else:
            option_string += '<option value="' + c_keys[i] + '">' + capitalize(c_keys[i]) + '</option>\n'
    return option_string

# capitalize option
def capitalize(option):
    return option[0].upper() + option[1:]

# fill mirror checkbox
def html_mirror(mirror):
    mirror_string = ""
    if mirror:
        mirror_string=" checked"
    return mirror_string

# save new global vars from request to json file
def save_json_config(request):
    # parse request
    pos = request.find('animation=')
    if pos > -1:
        # fetch the parameters line from the request
        param_line = request[pos:]
        # split into list of different parameters
        params = list(param_line.split('&'))
        # extract different parameters
        key, animation = params[0].split('=')
        key, period_ms = params[1].split('=')
        key, color_scheme = params[2].split('=')
        colors = gvars.color_schemes[color_scheme]
        if len(params)>3:
            mirror_colors = True
        else:
            mirror_colors = False
        # build config dictionary for json
        config = {}
        config['animation'] = animation
        config['period_ms'] = int(period_ms)
        config['color_scheme'] = color_scheme
        config['colors'] = colors
        config['mirror_colors'] = mirror_colors
        # dump dictionary to json file
        with open('config.json', 'w') as outfile:  
            ujson.dump(config, outfile)    
    return

# handle the webpage requests
async def handle_client(reader, writer):
    # wait for client connection
    request = await reader.read(1024)
    # get ip address of client
    addr = writer.get_extra_info('peername')
    print('Got a connection from %s' % str(addr))
    # decode request
    request = request.decode('utf-8')
    print('Content = %s' % request)
    # extract new global vars from request and save to json file
    save_json_config(request)
    # get new global vars from json file
    config = get_json_config()
    # create response
    response = web_page(config)
    # send response
    await writer.awrite('HTTP/1.1 200 OK\r\n\r\n' + response + '\r\n\r\n')
    # close client connection
    await writer.aclose()

###########################################################################
# animation code
###########################################################################
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

# get colors and mirror if necessary
def get_colors(config):
    colors = config['colors']
    if config['mirror_colors']:
        mirror(colors)
    return colors

# Animation functions:
async def blank(config, np, pixel_count):
    np.fill((0,0,0))
    np.write()
    await asyncio.sleep_ms(1000)

async def solid(config, np, pixel_count):
    colors = get_colors(config)
    elapsed = utime.ticks_ms() // config['period_ms']
    current = elapsed % len(colors)
    np.fill(colors[current])
    np.write()
    await asyncio.sleep_ms(0)

async def chase(config, np, pixel_count):
    colors = get_colors(config)
    elapsed = utime.ticks_ms() // config['period_ms']
    for i in range(pixel_count):
        current = (elapsed+i) % len(colors)
        np[i] = colors[current]
    np.write()
    await asyncio.sleep_ms(0)

async def smooth(config, np, pixel_count):
    # Smooth pulse of all pixels at the same color.  Interpolates inbetween colors
    # for smoother animation.
    colors = get_colors(config)
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
    await asyncio.sleep_ms(0)

async def cycle(config, np, pixel_count):
    # current color
    colors = get_colors(config)
    # build iterate list
    pos = []
    pos.extend(range(0, pixel_count))
    # iterate
    for i in pos:
        np.fill(colors[gvars.current_color])
        np[i] = (0, 0, 0)
        np.write()
        await asyncio.sleep_ms(config['period_ms'])
    # next color
    gvars.current_color += 1
    if gvars.current_color >= len(colors):
        gvars.current_color = 0
    
async def bounce(config, np, pixel_count):
    # current color
    colors = get_colors(config)
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
        await asyncio.sleep_ms(config['period_ms'])
    # next color
    gvars.current_color += 1
    if gvars.current_color >= len(colors):
        gvars.current_color = 0

async def fade(config, np, pixel_count):
    # current color
    colors = get_colors(config)
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
        await asyncio.sleep_ms(config['period_ms'])
    # next color
    gvars.current_color += 1
    if gvars.current_color >= len(colors):
        gvars.current_color = 0

async def rgbloop(config, np, pixel_count):
    # build iterate list
    val = []
    val.extend(range(0, 255, 5))
    val.extend(list(reversed(val))[1:-1])
    # iterate colors up & down
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
            await asyncio.sleep_ms(20)
            
async def strobe(config, np, pixel_count):
    # current color on
    colors = get_colors(config)
    color = colors[gvars.current_color]
    np.fill(color)
    np.write()
    await asyncio.sleep_ms(config['period_ms'])
    # current color off
    np.fill((0,0,0))
    np.write()
    await asyncio.sleep_ms(config['period_ms'])
    # next color
    gvars.current_color += 1
    if gvars.current_color >= len(colors):
        gvars.current_color = 0

async def cylon(config, np, pixel_count):
    # current color
    colors = get_colors(config)
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
        await asyncio.sleep_ms(config['period_ms'])
    # next color
    gvars.current_color += 1
    if gvars.current_color >= len(colors):
        gvars.current_color = 0
        
async def kitt2000(config, np, pixel_count):
    # current color
    colors = get_colors(config)
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
        await asyncio.sleep_ms(config['period_ms'])
    # next color
    gvars.current_color += 1
    if gvars.current_color >= len(colors):
        gvars.current_color = 0

async def twinkle(config, np, pixel_count):
    # current color
    colors = get_colors(config)
    color = colors[gvars.current_color]
    # iterate
    np.fill((0,0,0))
    for i in range(pixel_count // 3):
        pos_selected = gvars.animation_schemes.index(config['animation'])
        pos = urandom.randint(0, pixel_count-1)
        np[pos] = (color[0], color[1], color[2])
    np.write()
    await asyncio.sleep_ms(config['period_ms'])
    # next color
    gvars.current_color += 1
    if gvars.current_color >= len(colors):
        gvars.current_color = 0

async def sparkle(config, np, pixel_count):
    # current color
    colors = get_colors(config)
    color = colors[gvars.current_color]
    # random pixel on
    pos = urandom.randint(0, pixel_count-1)
    np[pos] = (color[0], color[1], color[2])
    np.write()
    # wait
    await asyncio.sleep_ms(config['period_ms'])
    # pixel off
    np[pos] = ((0,0,0))
    np.write()
    # next color
    gvars.current_color += 1
    if gvars.current_color >= len(colors):
        gvars.current_color = 0

async def runninglight(config, np, pixel_count):
    # current color
    colors = get_colors(config)
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
        await asyncio.sleep_ms(config['period_ms'])
    # next color
    gvars.current_color += 1
    if gvars.current_color >= len(colors):
        gvars.current_color = 0

async def rainbow(config, np, pixel_count):
    # 5 cycles for all colors
    for j in range(256*5):
        for i in range(pixel_count):
            color = wheel(((i * 256 // pixel_count) + j) & 255)
            np[i] = color
        np.write()
        await asyncio.sleep_ms(0)

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

async def comet(config, np, pixel_count):
    # current color
    colors = get_colors(config)
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
        await asyncio.sleep_ms(config['period_ms'])
    # next color
    gvars.current_color += 1
    if gvars.current_color >= len(colors):
        gvars.current_color = 0


async def play_animation(config, np, pixel_count):
    while True:
        config = get_json_config()
        animation = globals().get(config['animation'], blank)
        await animation(config, np, pixel_count)


async def switch_animation(btn, config):
    while True:
        if not btn.value():
            # get current config
            config = get_json_config()
            # set next animation
            current_animation = gvars.animation_schemes.index(config['animation'])
            current_animation += 1
            if current_animation > len(gvars.animation_schemes) - 2:
                current_animation = 0
            config['animation'] = gvars.animation_schemes[current_animation]
            print(config)
            # dump dictionary to json file
            with open('config.json', 'w') as outfile:  
                ujson.dump(config, outfile)
        await asyncio.sleep_ms(250)

###########################################################################
# main section
###########################################################################

try:
    # initialise neopixels
    np = init_neopixels(PIXEL_PIN, PIXEL_COUNT)
    # initialise animation button
    btn = init_animation_button(ANIM_PIN)
    # connect to wifi network
    wlan = connect2wifi(SSID, WIFI_PW)
    # get config from json file
    config = get_json_config()
    # event loop scheduler initialiseren
    loop = asyncio.get_event_loop()
    # taken op de event loop queue zetten
    loop.create_task(asyncio.start_server(handle_client, '' , 80))
    loop.create_task(play_animation(config, np, PIXEL_COUNT))
    loop.create_task(switch_animation(btn, config))
    # taken laten uitvoeren
    loop.run_forever()
    
except Exception as e:
    print('Probleem %s' % e)
    
finally:
    # neopixels off
    np.fill((0,0,0))
    np.write()
    # close event loop
    loop.close()
    # disconnect from wlan
    if wlan != None:
        wlan.disconnect()
    # soft reset esp
    sys.exit()

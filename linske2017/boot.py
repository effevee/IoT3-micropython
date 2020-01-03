# This file is executed on every boot (including wake-boot from deepsleep)

# turn off vendor OS debug messages
import esp
esp.osdebug(None)

#import uos, machine
#uos.dupterm(None, 1) # disable REPL on UART(0)

# run garbage collector
import gc
gc.collect()

#import webrepl
#webrepl.start()

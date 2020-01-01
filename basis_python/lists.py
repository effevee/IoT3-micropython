
dranklijst = []
vakken = ['RPi1', 'RPi2', 'RPi3', 'ESP32', 'WP1', 'WP2', 'EHBO1', 'EHBO2']
vak_detail = ['ESP32',60,True]

print(vakken)
print(vakken[0])
print(vak_detail)
print(vak_detail[0])
print(vakken[3])
print(vak_detail[-2])
print(vakken[1:5])
print(vakken[3:6])
print(vak_detail[:2])
print(vakken[-4:])

print(vakken)
vakken[4] = 'FPGA'
print(vakken)
vakken[vakken.index('WP2')] = 'C#'
print(vakken)
vakken[vakken.index('FPGA'):vakken.index('C#')+1] = ['WP1', 'WP2']
print(vakken)

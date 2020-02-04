zin_deel1 = 'MicroPython op de ESP32'
zin_deel2 = 'is leuk!'

print(zin_deel1 + ' ' + zin_deel2)
print('%s %s'%(zin_deel1, zin_deel2))

lower_zin_deel1 = zin_deel1.lower()
print(lower_zin_deel1)
print(zin_deel1.lower().islower())

upper_zin_deel2 = zin_deel2.upper()
print(upper_zin_deel2)

# lengte van een string
print(len(zin_deel1))
print(len(zin_deel2))

# eerste karakter van een string
print(zin_deel1[0])
print(zin_deel1[7])

# laatste karakter van een string
print(zin_deel1[-1])

# delen van een string
print(zin_deel1[0:5])

# index van een karakter in een string
print(zin_deel1.index('P'))
print(zin_deel2.index('u'))
print(zin_deel1.index('ESP'))
#print(zin_deel2.index('ESP'))
print(zin_deel2.find('ESP'))

# delen van een string vervangen
print(zin_deel1.replace('32', '64'))
print(zin_deel2.replace('leuk', 'fun'))

# lees inhoud van tekstfile lijn per lijn
try:
    pins={}
    pins_file=open('pins.txt','r')
    for line in pins_file.readlines():
        line=line.replace('\n','')
        koppel=line.split(':')
        pins.update({koppel[0]:koppel[1]})

except OSError as err:
    print('Probleem met lezen bestand - %s'%err)
    
except Exception as err:
    print('Onbekende fout - %s'%err)
   
finally:   
    pins_file.close()
    

print(pins)
for key,value in pins.items():
    print('%s -> %s'%(key,value))
    

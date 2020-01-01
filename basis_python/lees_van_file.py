# lees inhoud van een tekstfile naar lijst
pins_file=open('pins.txt','r')
print(pins_file.readlines())
pins_file.close()

# lees inhoud van tekstfile lijn per lijn
try:
    pins_file=open('pins.txt','r')
    for line in pins_file.readlines():
        print(line.replace('\n',''))

except OSError as err:
    print('Probleem met lezen bestand - %s'%err)
    
except Exception as err:
    print('Onbekende fout - %s'%err)
   
finally:   
    pins_file.close()

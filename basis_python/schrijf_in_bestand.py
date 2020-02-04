pins_file=None

try:
    pins_file=open('pins.txt','a')
    pins_file.write('pin14:in\n')

except OSError as err:
    print('Probleem met openen bestand - %s'%err)

except Exception as err:
    print('Onbekende fout - %s'%err)
    
finally:
    try:
        pins_file.close()
    except:
        print('Fout bij afsluiten bestand')
        
        

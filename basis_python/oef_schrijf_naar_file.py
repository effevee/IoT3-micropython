def write_dict_to_file(dictionary):
    # bestand openen om te schrijven
    try:
        pins_file=open('pins.txt','a')
        print(dictionary)
        for key,value in dictionary.items():
            print(key,value)
            pins_file.write('%s:%s\n'%(key,value))

    except OSError as err:
        print('Probleem met openen bestand - %s'%err)

    except Exception as err:
        print('Onbekende fout - %s'%err)
    
    finally:
        try:
            pins_file.close()
        except:
            print('Fout bij afsluiten bestand')
        

write_dict_to_file({'pin18':'in','pin20':'out'})

    
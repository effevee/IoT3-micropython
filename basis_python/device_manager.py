'''
Device Manager
(c)2018 Frank Vergote
Versie 1.0

Code om de inhoud van de bestanden en folders op het ESP32 device te beheren
Ondersteunt volgende functies :
- verwijderen en hernoemen van bestanden en folders
- aanmaken van nieuwe folder
- veranderen van folder
- inhoud tonen van een bestand
'''

# modules
import uos
import uerrno
import ure

# globale variabelen
lijst=[]
pwd='/'
optie=''

# naar root folder
uos.chdir(pwd)


def show_error(message):
    ''' Toont fout <message> op het scherm '''
    print(' ')
    print('*** FOUT ==> ' + message + ' ***')
    print(' ')


def get_number():
    ''' vraagt een volgnummer van het bestand of folder en kontroleert
        of het geldig is. Wordt als returnwaarde meegegeven '''
    global lijst
    # lus om geldig nummer te vragen
    nummer=''
    while nummer=='':
        nummer=input('Geeft het nummer van het bestand/folder : ')
        if nummer.isdigit():
            num=int(nummer)
            if num>0 and num<=len(lijst):
                return num
            
        # fout
        show_error('Ongeldig nummer!')
        nummer=''
        

def get_option():
    ''' vraagt een optie uit het menu en kontroleert of het geldig is.
        Wordt als returnwaarde meegegeven '''
    global optie
    # lus om geldig nummer te vragen
    option=''
    while option=='':
        option=input('Maak uw keuze : ')
        # enkel 1ste karakter
        if len(option)>1:
            option=option[0]
        # geldige letter ?
        if option in 'MmCcDdRrVvQq':
            return option.upper()
        # fout
        show_error('Ongeldige optie!')
        option=''
        

def get_name():
    ''' vraagt een bestand/folder naam en kontroleert of die geldig is.
        Wordt als returnwaarde meegegeven '''
    # regex compileren (omgekeerde logica -> NIET letters of cijfers of .)
    invalid_chars = ure.compile('[^A-Za-z0-9\.]')
    # lus om geldige naam te vragen
    name=''
    while name=='':
        name=input('Geef de nieuwe bestand/folder naam : ')
        # ongeldige letters in naam ?
        if invalid_chars.search(name)==None:
            return name
        # fout
        show_error('Ongeldige bestand/folder naam. Enkel letters of cijfers!')
        name=''


def get_files(pad=pwd):
    ''' maakt een lijst van bestanden en folders in <pad>
        Als <pad> niet ingegeven is wordt de root genomen '''
    global lijst,pwd
    # lijst opvullen
    lijst=[]
    try:
        lijst=uos.listdir(pad)
    except OSError as err:
        show_error('Pad bestaat niet! - %s'%err)
        return
    # bovenliggende folder entry in begin lijst ?
    if len(pwd)>1:
        lijst.insert(0,'..')



def get_file_stats(nummer=0):
    ''' haalt het type (F/D) en grootte van het bestand met volgnummer <nummer> op.
        Voor folders wordt als grootte <dir> doorgegeven '''
    global lijst,pwd
    # bovenliggende folder ?
    if lijst[nummer-1]=='..':
        return 'D','<dir>'
    # aanpassen pad met / achteraan indien nodig
    if pwd[-1:]!='/':
        pad=pwd+'/'
    else:
        pad=pwd
    # haal status op
    try:
        stats=uos.stat(pad+lijst[nummer-1])
    except OSError as err:
        show_error('Ongeldig bestand of folder! - %s'%err)
        return '',''
    # bestand of folder    
    if stats[0]==32768:      #bestand
        return 'F',str(stats[6])
    elif stats[0]==16384:    #folder
        return 'D','<dir>'  
    
    return '',''


def show_files():
    ''' toont de bestanden en folders van <lijst> in een directory formaat
        met volgnummer, bestandsnaam en grootte.
        Als het bestand een folder is wordt de grootte vervangen door <dir> '''
    global lijst
    # Toont de lijst met vestanden
    teller=1
    while teller<=len(lijst):
        stats=get_file_stats(teller)
        print('%d \t %s \t\t\t\t %s'%(teller,lijst[teller-1],stats[1]))
        teller+=1


def make_dir(dirname=''):
    ''' Maakt een nieuwe folder <dirname> aan in de huidige folder.'''
    global pwd
    # maak de folder aan
    try:
        uos.mkdir(dirname)
        # update huidige folder
        get_files(pwd)
    except OSError as err:
        if err.args[0]==uerrno.EEXIST:
            show_error('Folder bestaat reeds! - %s'%err)
        elif err.args[0]==uerrno.EINVAL:
            show_error('Ongeldige foldernaam! - %s'%err)
        else:
            show_error('Onbekende fout - %s'%err)
    except Exception as err:
        show_error('Onbekende fout - %s'%err)


def change_dir(nummer=0):
    ''' Past de huidige directory aan uit de <lijst> met volgnummer <nummer>.
        Opgelet: dit is enkel mogelijk voor bestaande folders in de huidige directory.'''
    global lijst, pwd
    # haal status bestand op
    stats=get_file_stats(nummer)
    if stats[0]=='F':      #bestand
        show_error('Dit is geen folder.')
        return
    elif stats[0]=='D':    #folder
        try:
            uos.chdir(lijst[nummer-1])
            # update huidige folder
            pwd=uos.getcwd()
            get_files(pwd)
        except OSError as err:
            show_error('Veranderen van huidige folder mislukt! - %s'%err)


def delete_file(nummer=0):
    ''' Verwijdert het bestand of folder uit de <lijst> met volgnummer <nummer>.
        Opgelet: voor het verwijderen van een folder moet die leeg zijn.'''
    global lijst,pwd
    # haal status bestand op
    stats=get_file_stats(nummer)
    # verwijder bestand/folder
    if stats[0]=='F':      #bestand
        try:
            uos.remove(lijst[nummer-1])
        except OSError as err:
            show_error('Verwijderen van bestand mislukt! - %s'%err)
            return
    elif stats[0]=='D':    #folder
        try:
            uos.rmdir(lijst[nummer-1])
        except OSError as err:
            show_error('Verwijderen van folder mislukt. Is de folder wel leeg ? - %s'%err)
            return
    # update lijst
    get_files(pwd)
    

def rename_file(nummer=0,filename=''):
    ''' Hernoemt het bestand of folder uit de <lijst> met volgnummer <nummer> naar <filename>.'''
    global lijst,pwd
    # hernoem bestand/folder
    try:
        uos.rename(lijst[nummer-1],filename)
    except OSError as err:
        if err.args[0]==uerrno.EINVAL:
            show_error('Ongeldige bestand/folder naam! - %s'%err)
        else:
            show_error('Onbekende fout - %s'%err)
        return
    # update lijst
    get_files(pwd)


def view_file(nummer=0):
    ''' Toont de inhoud van het bestand uit de <lijst> met volgnummer <nummer>.
        Opgelet: alleen voor bestanden.'''
    global lijst,pwd
    # haal status op
    stats=get_file_stats(nummer)
    if stats[0]!='F':
        show_error('Enkel bestanden kunnen bekeken worden!')
        return
    # lees de inhoud van het bestand en toon het in
    try:
        bestand=open(lijst[nummer-1],'r')
        print('')
        print('<%s>'%lijst[nummer-1])
        for lijn in bestand.readlines():
            #print(lijn)
            print(lijn.replace('\n',''))
    except OSError as err:
        show_error('Probleem met lezen bestand - %s'%err)
    except Exception as err:
        show_error('Onbekende fout - %s'%err)
    finally:
        bestand.close()


def main_screen():
    ''' Toont het filemanager scherm en wacht op een commando. Vervolgens wordt
        eventueel extra input gevraagd om het commando daarna te kunnen uitvoeren '''
    global lijst,pwd,optie
    
    # lus
    while optie!='Q':
    
        # toon de header
        lijn="-"*70
        print(' ')
        print(lijn)
        print('Device Manager v1.0 - huidige folder : %s'%pwd)
        print('Nr \t Naam \t\t\t\t Grootte')
        print(lijn)
        
        # toon de lijst met bestanden
        show_files()
        
        # toon de footer
        print(lijn)    
        print('Opties : [M]kdir - [C]hdir - [D]elete - [R]ename - [V]iew - [Q]uit')
        
        # wacht op geldige optie
        optie=get_option()
        
        # optie Mkdir
        if optie=='M':
            dirname=get_name()
            make_dir(dirname)
            continue
        
        # optie Chdir
        elif optie=='C':
            nummer=get_number()
            change_dir(nummer)
            continue
        
        # optie Delete
        elif optie=='D':
            nummer=get_number()
            delete_file(nummer)
            continue
        
        # optie Rename
        elif optie=='R':
            nummer=get_number()
            filename=get_name()
            rename_file(nummer,filename)
            continue

        # optie View
        elif optie=='V':
            nummer=get_number()
            view_file(nummer)
            continue
 
        # optie Quit
        elif optie=='Q':
            break
    
    print('Bedankt om Device Manager te gebruiken!')
        
            
get_files(pwd)
main_screen()

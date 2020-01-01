import math

def loopt_fout(g):
    lijst=[]
    log=10000000
    breuk=0
    index=1000
    try:
        lijst=[]
        for i in range(0,18):
            lijst.append(i)
        
        log=math.log(g-2)
        breuk=1.0/(g-8)
        index=lijst.index(g)
    except:
        print('Foute parameter')
    
    return (log,breuk,index)


def loopt_fout_info(g):
    lijst=[]
    log=10000000
    breuk=0
    index=1000
    try:
        lijst=[]
        for i in range(0,18):
            lijst.append(i)
        log=math.log(g-2)
        breuk=1.0/(g-8)
        index=lijst.index(g)
        data=lijst[g]
    except ValueError as err:
        print('Parameter valt buiten het domein van de functie - %s'%err)
    except ZeroDivisionError as err:
        print('Er kan niet door nul gedeeld worden - %s'%err)
    except IndexError as err:
        print('De index valt buiten de lijst - %s'%err)
    except Exception as err:
        print('Er is een onbekende fout opgetreden - %s'%err)
    
    return (log,breuk,index)


print("Log van getal: %f, Uitkomst breuk : %f, index : %d"%loopt_fout(2))
print("Log van getal: %f, Uitkomst breuk : %f, index : %d"%loopt_fout(5))
print("Log van getal: %f, Uitkomst breuk : %f, index : %d"%loopt_fout(8))
print("Log van getal: %f, Uitkomst breuk : %f, index : %d"%loopt_fout(19))
print("")
print("Log van getal: %f, Uitkomst breuk : %f, index : %d"%loopt_fout_info(2))
print("Log van getal: %f, Uitkomst breuk : %f, index : %d"%loopt_fout_info(5))
print("Log van getal: %f, Uitkomst breuk : %f, index : %d"%loopt_fout_info(8))
print("Log van getal: %f, Uitkomst breuk : %f, index : %d"%loopt_fout_info(19))
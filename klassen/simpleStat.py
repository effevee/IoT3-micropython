def AvgCleanList(lijst):
    ''' Functie die het kleinste en grootste element van de lijst verwijdert
        en vervolgens het gemiddelde neem.
        Parameter: lijst
        Return: geeft een tuple weer met als eerste element de status (0=ok, -1=fout)
                (0,gemiddelde van opgeschoonde lijst)
                (-1,-1) '''
    
    # fout
    if len(lijst)<=3:
        return (-1,-1)
    
    # ok
    lijst.sort()
    lijst.pop()    # verwijder laatste element
    lijst.pop(0)   # eerste eerste element
    gem = sum(lijst)/len(lijst)
    return (0,gem)


def MedianList(lijst):
    ''' Functie die de mediaal van de lijst geeft: bij een lijst met een oneven aantal elementen
        is dit het middelste element; bij een even aantal elementen worden de 2 middelste elementen
        opgeteld en gedeeld door 2
        Parameter: lijst
        Return: geeft een tuple weer met als eerste element de status (0=ok, -1=fout)
                (0,mediaan van de lijst)
                (-1,-1) '''

    # fout
    if len(lijst)==0:
        return (-1,-1)
    
    # ok
    lijst.sort()
    #print(lijst)
    m=len(lijst)//2
    if len(lijst)%2==1:   # oneven  [1,2,3,4,5] -> 3
        med=lijst[m]
    else:                 # even [1,2,3,4,5,6] -> (3+4)/2
        med=(lijst[m-1]+lijst[m])/2
    return (0,med)
        
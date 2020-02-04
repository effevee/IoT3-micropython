def even(getal):
    if (getal%2)==0:
        return True
    else:
        return False

def veelvoud_3_4_of_beiden(getal):
    if (getal%3)==0 and (getal%4)==0:
        return 3*4
    elif (getal%3)==0:
        return 3
    elif (getal%4)==0:
        return 4
    else:
        return 1

def groter_dan_lengte_rij(lijst):
    if max(lijst)>=len(lijst):
        return True
    return False

def langste_woord(lijst):
    # lengte elementen
    l_len=[]
    pos=0
    while pos<len(lijst):
        l_len.append(len(lijst[pos]))
        pos+=1
    # print(l_len)
    # langste elementen
    max_l=max(l_len)
    l_max=[]
    pos=0
    while pos<len(lijst):
        if len(lijst[pos])>=max_l:
            max_l=l_len[pos]
            l_max.append(lijst[pos])
        pos+=1
    return tuple(l_max)

def langste_woord2(lw):
    words=[]
    max_len = len(lw[0])
    for w in lw:
        if max_len>len(w):
            continue
        if max_len < len(w):
            words=[]
        words.append(w)
        max_len=len(w)
    return tuple(words)


g=50
if even(g):
    print('%d is een even getal'%g)
else:
    print('%d is een oneven getal'%g)
        
g=12
print('%d is deelbaar door %d'%(g,veelvoud_3_4_of_beiden(g)))

l = [1, 2, 3, 4 ]
print(groter_dan_lengte_rij(l))

w=['een', 'twee', 'drie', 'vier', 'vijf', 'zes', 'zeven', 'acht', 'negen', 'tien']
print(langste_woord(w))
print(langste_woord2(w))
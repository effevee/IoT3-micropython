import random

def random_lijst(begin,einde,lengte):
    lijst=[]
    for i in range(lengte):
        g=random.randint(begin,einde)
        lijst.append(g)
    return lijst

def deelbaar_door_4(lijst):
    getallen=[]
    for e in lijst:
        if e!=0 and e%4==0:
            getallen.append(e)
    return getallen

l=random_lijst(0,250,20)
print(l)
d4=deelbaar_door_4(l)
print(d4)
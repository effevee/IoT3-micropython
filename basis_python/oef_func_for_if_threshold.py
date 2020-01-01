import func_for_if_vb as mylists

def bin_bij_threshold_interval(begin_drempel,eind_drempel,lijst):
    result=[]
    for g in lijst:
        if g in range(begin_drempel,eind_drempel):
            result.append(1)
        else:
            result.append(0)
    return result

def bin_bij_threshold_gem(lijst):
    result=[]
    som=0
    for g in lijst:
        som+=g
    gem=som//len(lijst)
    print('gemiddelde : %d'%gem)
    for g in lijst:
        if g>gem:
            result.append(1)
        else:
            result.append(0)
    return result

l=mylists.random_lijst(0,250,20)
print(l)
b=bin_bij_threshold_interval(100,150,l)
print(b)
g=bin_bij_threshold_gem(l)
print(g)
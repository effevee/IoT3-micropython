def max_van_3_kort(g1,g2,g3):
    getallen = (g1,g2,g3)
    return max(getallen)

def max_van_3_lang(g1,g2,g3):
    max=0
    if g1>=g2 and g1>=g3:
        return g1
    elif g2>=g1 and g2>=g3:
        return g2
    else:
        return g3

print('%d is het grootste getal'%max_van_3_kort(10,12,3))
print('%d is het grootste getal'%max_van_3_lang(1,2,3))
def factor(getal):
    if getal > 1:
        return getal * factor(getal - 1)
    else:
        return 1
    
resultaat = factor(4)
print(resultaat)


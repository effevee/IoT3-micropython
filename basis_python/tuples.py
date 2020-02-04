kleuren = ("rood","oranje","groen","blauw","geel","paars")
cor1 = (5,8,7)
cor2 = (9,9,11)
data_person = ("Pipi", "Langkous", 1965)
# element uit tuple halen
print(kleuren[1])
print(kleuren[2])
# reeks elementen uit tuple halen
print(kleuren[1:5])
# tuple veranderen geeft fout
#data_person[2] = 1975
# + operator voegt tuples samen
print(cor1+cor2)
# tuple met 1 element
eenzame_tuple = ("UNIEK",)
print(eenzame_tuple)
# tuple van lijsten kan je wel wijzigen
van_naar = ([0,0], [20,25])
van_naar[1][0] = 25
print(van_naar)
# aantal elementen in tuple
print(cor2.count(9))
# maximum van tuple
print(max(cor1))
# truuk om tuple toch aan te passen
print(kleuren)
kleuren_lijst = list(kleuren)
kleuren_lijst[kleuren_lijst.index("groen")] = "magenta"
kleuren = tuple(kleuren_lijst)
print(kleuren)


# 2
vakken = ["RPi1", "RPi2", "RPi3", "ESP32", "WP1", "WP2", "EHBO1", "EHBO2"]
lt = [80, 80, 80, 60, 60, 60, 80, 80]
# 3 kopie van een lijst maken
vakken2 = vakken.copy()
# kopie van de pointer ! Verwijst naar zelfde geheugenlokatie
vakken3 = vakken2
# vakken3[0] = "TEST"
# 4
print(vakken2)
# 5 uitbreiden van vakken2 met lt
vakken2.extend(lt)
# 6 
print(vakken2)
# 7 toevoegen van element aan lijst
vakken2.append("WP2")
print(vakken2)
# 8 tussenvoegen van element in een lijst op positie x
vakken2.insert(3, "C#")
print(vakken2)
# 10 verwijderen van een element uit de lijst
vakken2.remove("C#")
print(vakken2)
# 12
vakken2.remove("WP2")
print(vakken2)
# 13 lijst leegmaken
vakken2.clear()
print(vakken2)
print(vakken3)
# 14 laatste element van lijst tonen + verwijderen
print(vakken.pop())
print(vakken)
# 15 volgnummer van element in een lijst
print(vakken.index("ESP32"))
# 16
print(vakken.index("EHBO1"))
#17
print(vakken.index("WP2"))
# print(vakken.index("BlaBla"))
# geeft fout als element niet in lijst zit; opvangen met try except constructie
# 18 tellen van aantal elementen in een lijst
vakken.append("ESP32")
print(vakken)
print(vakken.count("ESP32"))
# 20 sorteren van een lijst
vakken.sort()
print(vakken)
# 21
lt.sort()
print(lt)
# 22 omgekeerd sorteren
vakken.reverse()
print(vakken)
# 23 lengte van een lijst
print(len(vakken))
# 24
print(len(lt))


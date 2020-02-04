empty={}
weekdagen={1:'maandag',
           2:'dinsdag',
           3:'woensdag',
           4:'donderdag',
           5:'vrijdag'}

# afdrukken van dictionary
print(weekdagen)
# afdrukken van waarde van een dictionary element
print(weekdagen[3])
print(weekdagen.get(4))
print(weekdagen.get(6,'niet gevonden'))

# woensdag -> woen hernoemen
weekdagen[3]='woen'
print(weekdagen)

# maak een dictionary dagen met de koppels 6:zaterdag en 7:zondag
dagen={6:'zaterdag',7:'zondag'}

# updaten van een dictionary
dagen.update(weekdagen)
print(dagen)

# opvragen van de keys
print(dagen.keys())

# opvragen van de waarden
print(dagen.values())

# koppel verwijderen uit dictionary
print(dagen.pop(6))
print(dagen)

# lengte van dictionary
print(len(dagen))
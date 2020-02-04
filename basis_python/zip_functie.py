familie =("Jan","Ann","Kamiel","Zulma")
leeftijd=[25,24,75,78]

koppels = zip(familie,leeftijd)
print(list(koppels))

x_waarden = [1,2,3,6]
y_waarden = [-3,-5,-7,0]
z_waarden = [10,11,12,9]

coordinaten = zip(x_waarden,y_waarden,z_waarden)
print(list(coordinaten))

steden = ("Brugge","Gent","Kortrijk","Brussel","Moeskroen")
neerslag = [10,5,15,8,2]
wind_richting = ["w","w","zw"]

meteo = zip(steden, neerslag, wind_richting)
print(list(meteo))

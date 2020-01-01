def inhoud_kubus(ribbe):
  """berekent de inhoud van een kubus met als ribbe de parameter:ribbe"""
  inhoud = ribbe * ribbe * ribbe
  return inhoud
  
def inhoud_balk(lengte,breedte,hoogte):
  """berekent de inhoud van een balk met als afmetingen de parameters:lengte,breedte,hoogte"""
  inhoud = lengte * breedte * hoogte
  return inhoud
  
def inhoud_opp_kubus(ribbe):
  """berekent de inhoud en de oppervlakte van een kubus met als ribbe de parameter:ribbe"""
  inhoud = ribbe * ribbe * ribbe
  oppervlakte = 6 * ribbe * ribbe
  return inhoud,oppervlakte
 
def inhoud_opp_balk(lengte,breedte,hoogte):
  """berekent de inhoud en de oppervlakte van een balk met als afmetingen de parameters:lengte,breedte,hoogte"""
  inhoud = lengte * breedte * hoogte
  oppervlakte = (2 * lengte * breedte) + (2 * lengte * hoogte) + (2 * breedte * hoogte)
  return inhoud,oppervlakte
  
# oproepen functie inhoud_kubus
print("inhoud kubus: " + str(inhoud_kubus(5)))

# oproepen functie inhoud_balk
print("inhoud balk: " + str(inhoud_balk(3,4,5)))

# oproepen functie inhoud_opp_kubus
print("inhoud kubus: " + str(inhoud_opp_kubus(5)[0]))
print("oppervlakte kubus: " + str(inhoud_opp_kubus(5)[1]))

# oproepen functie inhoud_opp_balk
print("inhoud balk: " + str(inhoud_opp_balk(3,4,5)[0]))
print("oppervlakte balk: " + str(inhoud_opp_balk(3,4,5)[1]))

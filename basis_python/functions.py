def zeg_hallo():
  """print: hallo daar!"""
  print("Hallo daar!")
  
def zeg_hallo_wie(naam):
  """print: hallo <waarde van variabele:naam>"""
  print("Hallo, " + naam + "!")

def zeg_hallo_wie_data(naam,leeftijd,lengte):
  """print: hallo <waarde van variabelen:naam, leeftijd, lengte"""
  print("Hallo, " + naam + "!")
  print("Je bent " + str(leeftijd) + " jaren oud.")
  print("Je lengte is " + str(lengte) + " m")
  
# oproepen functie zeg_hallo
zeg_hallo()

# oproepen functie zeg_hallo_wie
zeg_hallo_wie("Frank")

# oproepen functie zeg_hallo_wie_data
zeg_hallo_wie_data("Frank", 59, 1.76)

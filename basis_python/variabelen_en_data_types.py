def persoon(naam, leeftijd, is_man):
  
  if is_man :
    hij_zij = 'Hij'
    zijn_haar = 'zijn'
  else:
    hij_zij = 'Zij'
    zijn_haar = 'haar'
  
  print('Dit is %s. %s is %.1f jaar.'%(naam, hij_zij, leeftijd))
  print('%s is een man : %s.'%(naam, is_man))
  print('%s is tevreden met %s naam.'%(naam, zijn_haar))
  print('Maar %s is minder tevreden met %s %.1f jaren.'%(naam, zijn_haar, leeftijd))
  print(' ')


  
persoon('Jan', 75, True)
persoon('Piet', 50.5, True)
persoon('Ann', 55, False)
persoon('Joris', 25.5, True)  


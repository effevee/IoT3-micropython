is_een_kat = False

if is_een_kat:
  print("Dit is een kat")
else:
  print('Dit is geen kat')


is_een_hond = False
is_groot = True
if is_een_hond and is_groot:
  print('Dit is een grote hond')
elif not(is_een_hond) and is_groot:
  print('Het is geen hond maar groot')
elif is_een_hond and not(is_groot):
  print('Het is een hond maar niet groot')
else:
  print('Het is geen hond en ook niet groot')
  

is_regen = False
heb_paraplu = False
if not(is_regen) or heb_paraplu:
    print('Ik kom naar de les')
else:
    print('Ik blijf thuis')
    
is_warm = True
is_zon = False
is_wind = False
if is_warm and is_zon and not(is_wind):
    print('Ik ga op het strand liggen')
elif is_warm and is_zon and is_wind:
    print('Ik ga zeilen')
elif not(is_warm) and is_zon and not(is_wind):
    print('Ik ga wandelen')
elif not(is_warm) and is_zon and is_wind:
    print('Ik ga vliegeren')
elif not(is_warm) and not(is_zon) and not(is_wind):
    print('Ik ga naar het lunapark')
else:
    print('Ik blijf thuis')
    
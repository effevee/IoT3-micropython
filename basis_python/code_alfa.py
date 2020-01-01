def codeer(tekst):
    code=''
    for c in tekst:
        # hoofdletters
        if ord(c) in range(65,91):
            code=code+chr(91-ord(c)+64)
        # kleine letters
        elif ord(c) in range(97,123):
            code=code+chr(123-ord(c)+96)
        # ander karakter
        else:
            code=code+c
    return code
            
            
        
        
s1='Dit is 1 rare zin of 2!'
print(s1)
s2=codeer(s1)
print(s2)
s3=codeer(s2)
print(s3)
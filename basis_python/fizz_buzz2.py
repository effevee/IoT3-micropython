i=1
while i<=100:
    msg=''
    if i%3==0:
        msg='Fizz'
    if i%5==0:
        msg=msg+'Buzz'
    print('%d\t%s'%(i,msg))    
    i+=1

i=1
while i<=100:
    if i%3==0 and i%5==0:
        print('%d FizzBuzz'%i)
    elif i%3==0:
        print('%d Fizz'%i)
    elif i%5==0:
        print('%d Buzz'%i)
    else:
        print(i)
    i+=1
print('uit while lus')
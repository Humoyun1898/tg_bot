integer = int(input('Enter a number'))

prime_numbers = []

def check_prime(my_num):
    devisors = 0
    for i in range(2,int((my_num**0,5)+2)):
        if my_num%i == 0:
            devisors+=1
        
        if devisors ==0:
            prime_numbers.append(my_num)

limit = int(input('Enter a positive integer'))

for i in range(2,limit+1):
    check_prime(i)


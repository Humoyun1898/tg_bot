#1. You have to check whether a string is a palindrome or not.
string = input ('Enter any string :')
if string[::-1] == string:
    print('It is palyndrome')
else:
    print('It is not palyndrome')
    

#2.Given a non-empty array of integers nums, every element appears twice except for one. Find that single one.
nums = [2,2,5,5,8,9,9,8,10]
for x in nums:
    if nums.count(x) == 1:
        print(x)

#3.In each tuple, the first number represents the year, and the remaining numbers are values.Create a new list that contains, for each year and the highest value from that tuple.

ls = [(2001,10,101,87),
      (2002,103,19,88),
      (2003,21,23,89),
      (2004,27,28,91)]

highest_values = []
for x in ls:
    highest_values.append((x[0],max(x[1:])))

print(highest_values)

#4. It is required to print all integers powers of two that do not exceed the number N.

integer = int(input('Print any integer: '))
power = 1
while 2**power < integer:
    print(2**power)
    power += 1

#5. 
list = ["abc","bcd","aaaa","cbc"] 
indexes = []
x = 'a'
for i in list:
    if x in i:
        indexes.append(list.index(i))

print(indexes)

#6.
def is_perfect(n):
    devisors = []
    for z in range (1,n):
        if n%z == 0:
            devisors.append(z)
    if sum(devisors) == n:
        return True
    else:
        return False
    
perfect_numbers = []

integer = int(input('Give me any integer'))
for l in range(1,integer):
    if is_perfect(l):
        perfect_numbers.append(l)
print(perfect_numbers)

#my_list=['h','e','l','l','o']
#print(my_list.count('l')) #count how many l there are in the list
#print(len(my_list))
numbers_1 = [12,13,14]
numbers_2 = [15,16,17]
numbers_1.extend(numbers_2)
print(numbers_1)

new_list = numbers_1 + numbers_2
print(new_list)
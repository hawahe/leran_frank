search = '168'
num_a = '1386-168-0006'
num_b = '1681-222-0006'

print(search + ' is at ' + str(num_a.find(search)) + ' to ' + str(num_a.find(search) + len(search)) + ' of num_a')
print(search + ' is at ' + str(num_b.find(search)) + ' to ' + str(num_b.find(search) + len(search)) + ' of num_b')

import IPy

fibs = [0,1]
num = int(input('How many Fibonacci numbers do you want? '))
for i in range(num-2):
    fibs.append(fibs[-2] + fibs[-1])
print(fibs)


a = IPy.IP('10.0.0.0').make_net('255.0.0.0')
a =  str(a)
print(type(a))
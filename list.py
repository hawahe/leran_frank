#num = [1,2,3,4]
#3str = ['One','Two','Three','Four']
#for a,b in zip(num,str):
 #   print(a,'is',b)


#import time
#a = []
#t0 = time.clock()
#for i in range(1,2000):
#    a.append(i)
#print(time.clock() - t0,"seconds process time")

#t0 = time.clock()
#b = [i for i in range(1,2000)]
#print(time.clock() - t0,"seconds process time")


#a = [i**2 for i in range(1,10)]
#c = [j+1 for j in range (1,10)]
#k = [n for n in range(1,10) if n % 2 ==0]
#z = [letter.lower() for letter in 'ABCDEFGHIGKLMN']
#print(a)
#print(c)
#print(k)
#print(z)

#d = {i:i+1 for i in range(4)}
#g = {i:j for i,j in zip(range(1,6),'abcde')}
#G = {i:j.upper() for i,j in zip(range(1,6),'abcde')}
#print(d)
#print(g)
#print(G)

letters = ['a','b','c','d','e','f','g']
for num,letter in enumerate(letters):
    print(letter,'is',num + 1)


















import math
a = int(input('please input the a:'))
b = int(input('please input the b:'))

def triangle(a,b):
    c = math.sqrt(a*a + b*b)
    return c
d = triangle(a,b)
print("The right triangle third side's length is {}".format(d))




a = [x*x for x in range(10)]
print(a)

a= [x*x for x in range(10) if x % 3 ==0]
print(a)

a = [(x,y) for x in range(3) for y in range(3)]
print(a)

result = []
for x in range(3):
    for y in range(3):
        result.append((x,y))
print(result)

girls = ['alice','bernice','clarice']
boys = ['chris','arnold','bob']
a = [b+'+'+g for b in boys for g in girls if b[0] == g[0]]      #只打印首字母相同的男孩和女孩的名字
print(a)

girls = ['alice','bernice','clarice']
boys = ['chris','arnold','bob']
letterGirls = {}
for girl in girls:
    letterGirls.setdefault(girl[0],[]).append(girl)
print(letterGirls)
print([b+'+'+g for b in boys for g in letterGirls[b[0]]])



list_1 = [1,4,5,7,3,6,7,9]
list_1 = set(list_1)

print(list_1,type(list_1))


list_2 = set([2,6,0,66,22,8,4])

list_3 = set([1,3,7])
list_4 = set([5,6,7,8])
print(list_1,list_2)


#显示交集
print(list_1.intersection(list_2))

#显示并集
print(list_1.union(list_2))

#差集 集合1里有的，而集合2里没有的数据
print(list_1.difference(list_2))

#子集
print(list_1.issubset(list_2))

#父集
print(list_2.issuperset(list_1))


#对称差集，不显示两个集合中都有的数据，然后做并集
print(list_1.symmetric_difference(list_2))

#是否有交集
print(list_3.isdisjoint(list_4))


#运算符交集
print(list_1 & list_2)

#运算符并集
print(list_1 | list_2)

#运算符差集
print(list_1 - list_2)

#运算符对称差集
print(list_1 ^ list_2)

#在集合中添加数据
list_1.add(999)
print(list_1)

#在集合中添加多个数据
list_1.update([888,777,555])
print(list_1)

#在集合中随机删除一个数据并返回该值
print(list_1.pop())

#在集合中删除指定数据但不返回值
print(list_1.discard(888))



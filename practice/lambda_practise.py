'''
关于匿名函数的练习，匿名函数不需要起名字的函数。可以在单行完成的函数。

'''

f = lambda a,b,c:a+b+c
print(f(1,2,3))


d = lambda a:a[::-1]        #将匿名函数里给的实参内容顺序反转，如hello的结果就是“olleh”
print(d("hello"))


fruits = ['strawberry','fig','apple','cherry','raspberry','banana']         #使用lambda表达式反转拼写，然后依此给单词
                                                                            # 列表排序
print(sorted(fruits,key=lambda word:word[::-1]))
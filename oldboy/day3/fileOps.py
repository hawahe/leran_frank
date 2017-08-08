f = open('lyric','r',encoding='utf-8')
#print(f.read()) #一次性读出文件的所有内容
#print(f.readline()) #一次只能文件的一行内容
#for i in range(5):     #通过循环读取文件前5行
#    print(f.readline())
#print(f.readlines())   #将文件所有内容放入一个列表，每行是列表的一个元素；

'''
print(f.tell())     #返回文件指针当前的位置
print(f.readline())
print(f.tell())
f.seek(0)           #将文件指针返回文件的起始位置；
print(f.readline())


print(f.encoding)   #显示文件的编码类型
,,,




#enumerate函数的作用是在同一个循环中分别遍历list或者tuple的索引和元素
#以下的循环是循环输出每行文件内容，并将第十行的内容替换成“我是分割线”
for index,line in enumerate(f.readlines()):
    if index == 9:
        print('------------我是分割线-----------')
        continue
    else:
        print(line.strip())
'''


f_new = open('lyric_new','w',encoding='utf-8')

for line in f:  #效率最高，是一行一行的将文件读入内存；readlines函数是全部一次性读入内存，效率低
    if '肆意的快乐' in line:
        line = line.replace('肆意的快乐等我享受','肆意的快乐等Frank享受')
    f_new.write(line)
f.close()
f_new.close()

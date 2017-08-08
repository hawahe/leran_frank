f = open('password.txt' ,'r')
f1 = open('lock_user.txt','r+')

count = 3
while count > 0:        #count 是用户的试错次数，少于0将显示账户锁定
    username = input('username:')
    password = input('password:')
    for line1 in f1:    #判断用户名是否已经锁定
        if username in line1:
            print('username %s has locked by system,please contact administrator' % username)
            f1.seek(0)  #指针返回lock＿user.txt 首行,继续循环
            exit()      #退出程序
        else:
            continue    #如果lock_user.txt第一行没有该用户，继续循环到下一行；

    for line in f:
        passwd = line.split()   #将password.txt文件内的内容转成列表；
        if username == passwd[0] and password == passwd[1]: #判断用户名和密码是否匹配
            print('Welcome %s login system' %username)
            exit()              #输入用户名和密码匹配passowrd.txt将推出程序并显示登录成功；
    print('Vaild username or password,you left %s times chance to try it ' %(count - 1))    #否则显示登录失败次数
    count -= 1  #登录次数-1，
print('username %s has locked by system,please contact administrator' % username)
f1.write(username + '\n')       #登录次数减到0将该用户名追加写入到lock_user.txt
f.close()
f1.close()
exit()

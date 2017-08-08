# -*- coding: utf-8 -*-
import pexpect,time
#username = str(input('Username:'))
#password = str(input('Password:'))
#passwd1 = str(input('SSG5 administrator password:'))
#print(username, password, passwd1)
passwd1 = 'xxxxxx'
ip_list = []
log_sucess = []
log_failure = []
cmd1 = "set route 10.17.11.0/24 interface tunnel.10"
cmd2 = "set address Office 12.0.0.0/8 12.0.0.0 255.0.0.0"
cmd3 = "set address JD-to-YZ 10.0.0.0/8 10.0.0.0 255.0.0.0"
cmd4 = "set policy id 15 from Office to JD-to-YZ  12.0.0.0/8 10.0.0.0/8 ANY permit"
f1 = open('cinema_ip.txt','r')
for line in f1:
    line = line.replace('\n','')
    ip_list.append(line)
print(ip_list)
f1.close()

for i in ip_list:

    child1 = pexpect.spawn('ssh administrator@%s -p 1139' %i,timeout = 60)
    time.sleep(3)
    p2 = child1.expect(['yes','password:'])
    if p2 == 0:
        child1.sendline ('yes')
        child1.expect('password:')
        child1.sendline(passwd1)
    elif p2 == 1:
        child1.sendline(passwd1)
    p = child1.expect(['>','denied'])
    if p == 0:
        f2 = open('ip_success.txt','a+')
#        child1.logfile = f2
        time.sleep(1)
        child1.sendline(cmd1)
        child1.expect('>')
        child1.sendline(cmd2)
        child1.expect('>')
        child1.sendline(cmd3)
        child1.expect('>')
        child1.sendline(cmd4)
        child1.expect('>')
        child1.sendline('save')
        child1.expect('>')
        child1.sendline('exit')
        print('%s OKOKOK!!!!' %i)
        log_sucess.append('%s OKOKOK!!!!\n' %i)
        time.sleep(2)
        f2.close()
    elif p == 1:
        f3 = open('ip_failure.txt','a+')
 #       child1.logfile = f3
        time.sleep(1)
        print('%s failure!!!!' %i)
        log_failure.append('%s failure!!!!\n' %i)
        f3.close()





print("all has been finished")




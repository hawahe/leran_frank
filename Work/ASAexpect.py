#!/usr/bin/python
# python script to fetch the running config of a cisco asa
import pexpect

username = input('input username:')
password1 = input('input password:') # that's why you should be really carefull where to store this script!
password2 = input('input enable password:')
ip_list = { "ISG":['10.157.0.2'],
           "CiscoASA":['10.128.0.26','10.130.0.26','10.157.0.26'],
            }


def network_backup_for_ASA():
    for ip in ip_list[user_choice]:
        child = pexpect.spawn('ssh ' + username + '@' + ip)
        child.expect('.*assword:.*')
        child.sendline(password1)

        child.expect('.*> ')
        child.sendline('ena')
        child.expect('.*assword:.*')
        child.sendline(password2)

        child.sendline('terminal pager 0')

        child.sendline('more system:running-config')
        child.expect(': end.*')
        runningconfig = child.before.decode("utf-8")
        f = open('%s.txt' % ip, 'a+')
        f.write(runningconfig)
        child.sendline('exit')
        print('%s has been backup successful' % ip)
        print('--------------------------------------------------------------------------------------------'
              '--------------------------------------------------------------------------------------------')
        child.close()
        f.close()

def network_backup_for_ISG():
    for ip in ip_list[user_choice]:
        child = pexpect.spawn('ssh ' + username + '@' + ip)
        child.expect('.*assword:.*')
        child.sendline(password1)

        child.expect('.*> ')
        child.sendline('set console page 0')
        child.expect('.*> ')
        child.sendline('get tech')
        child.expect('.*> ')
        runningconfig = child.before.decode("utf-8")
        f = open('%s.txt' % ip, 'w')
        f.write(runningconfig)
        child.sendline('unset console page')
        child.expect('.*> ')
        child.sendline('exit')
        print('%s has been backup successful' % ip)
        print('--------------------------------------------------------------------------------------------'
              '--------------------------------------------------------------------------------------------')
        child.close()
        f.close()

while True:
    for k,v in ip_list.items():
        print(k,v)

    user_choice = str(input('input the type of device what you want to backup,press q quit:'))


    if user_choice.lower() == 'isg':
        #network_backup_for_ISG()
        print('This type of device is not be supported now!')
    elif user_choice.lower() == 'ciscoasa':
        network_backup_for_ASA()
    elif user_choice.lower() == 'q':
        exit()
    else:
        print('Please input  a vaild choice!!!')
        continue






# -*- coding: utf-8 -*-
import paramiko,time,os,getpass
def backup_network(username,password,cmd,ipaddress):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ipaddress, 22, username, password)
    stdin, stdout, stderr = ssh.exec_command(cmd)
    f = open('C:\\Users\\zhao\\Desktop\\运维网备份\\%s\\%s.txt' %(time1,ipaddress),'w',encoding='utf8')
    a = stdout.readlines()
    for i in a:
        f.write(i)
    print('%s has been backup successful' %ip)
    print('--------------------------------------------------------------------------------------------'
          '--------------------------------------------------------------------------------------------')
    f.close()

    ssh.close()


username = input('username:')
#password = getpass.getpass('password:')
password = input('password:')
cmd = ["show configuration | display set","show run","get config all"]
ip_list = {"Junos":['10.128.1.1','10.130.1.3'],
           "CiscoRW":['10.128.1.2','10.128.1.3','10.128.3.2','10.128.3.3',
                      '10.130.1.1','10.130.1.2','10.130.3.2','10.130.3.3',
                      '10.128.0.2','10.155.1.1','10.157.0.1',
                      '10.154.1.1','10.158.1.1','10.146.1.1','10.144.1.1',
                      '10.152.1.1','10.149.1.1','10.132.1.1','10.129.31.1'],
           "ISG":['10.157.0.2'],
           "CiscoASA":['10.128.0.26','10.130.0.26','10.157.0.26'],
}
time1 = time.strftime("%Y-%m-%d",time.localtime())

while True:
    for k,v in ip_list.items():
        print(k,v)

    user_choice = str(input('input the type of device what you want to backup,press q quit:'))

    if user_choice.lower() == 'junos':
        cmd_type = cmd[0]
    elif user_choice.lower() == 'ciscorw':
        cmd_type = cmd[1]
    elif user_choice.lower() == 'isg':
        #cmd_type = cmd[2]
        print('unsupport this type of device!!!')
    elif user_choice.lower() == 'ciscoasa':
        print('unsupport this type of device!!!')
        continue
    elif user_choice.lower() == 'q':
        exit()
    else:
        print('Please input  a vaild choice!!!')
        continue

    for ip in ip_list[user_choice]:

        if  os.path.exists('C:\\Users\\zhao\\Desktop\\运维网备份\\%s' %time1):
            backup_network(username,password,cmd_type,ip)
        else:
            os.mkdir('C:\\Users\\zhao\\Desktop\\运维网备份\\%s' %time1)
            backup_network(username,password,cmd_type,ip)





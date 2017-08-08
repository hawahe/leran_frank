
import paramiko


def junos_zone_lookup(hostname,username,password,ipaddr):
#def junos_zone_lookup(ipaddr):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #client.connect(hostname, username, password, '22')
    client.connect(hostname=hostname, username=username, password=password, port=22)
    stdin, stdout, stderr = client.exec_command('show route %s' % ipaddr)
    next_hop = stdout.readlines()
    for i in next_hop:
        if i.strip().startswith('>') or i.strip().startswith('Local'):
            res_next_hop = i.split()
            #print(res_next_hop)
            stdin, stdout, stderr = client.exec_command('show interface %s' % res_next_hop[-1])
            if_info = stdout.readlines()
            for i2 in if_info:
                    if i2.strip().startswith('Security: Zone:'):
                        zone = i2.split()
                        print(zone[-1])
                        client.close()
                        return zone[-1]


def iprange_creator(ip_begin,ip_end):
    ip1 = ip_begin.split('.')[0]
    ip2 = ip_begin.split('.')[1]
    ip3 = ip_begin.split('.')[2]
    ip4 = ip_begin.split('.')[-1]

    ipend_last = ip_end.split('.')[-1]

    for i in range(int(ip4)-1,int(ipend_last)):
        ip = str(ip1+'.'+ip2+'.'+ip3+'.'+ip4)
        int_ip4 = int(ip4)
        int_ip4 += 1
        ip4 = str(int_ip4)
        print(ip)
        ip_list.append(ip)
def junos_obj_creator(s_zone,ip_list,ip_obj_name):
    for i2 in ip_list:
        ip_obj = str(i2 + nmask)
        if ip_obj_name == '0':
            ip_obj_cmd = 'set security zones security-zone %s address-book address %s %s' %(s_zone,ip_obj,ip_obj)
        else:
            ip_obj_cmd = 'set security zones security-zone %s address-book address %s-%s %s' % (s_zone,ip_obj,ip_obj_name,ip_obj)
        ip_obj_list.append(ip_obj)
        print(ip_obj_cmd)
def junos_policy_creator(s_zone,d_zone,ip_list,policy_name):
    if len(s_zone) == 0:
        hostname = input('Please input manage ip:')
        username = input('username:')
        password = input('password:')
        s_zone = junos_zone_lookup(hostname, username, password,ip_list[0] )
    elif len(d_zone) == 0:
        hostname = input('Please input manage ip:')
        username = input('username:')
        password = input('password:')
        d_zone = junos_zone_lookup(hostname, username, password,ip_list[0] )
    for i3 in ip_list:
        ip_obj = str(i3 + nmask)
        if ip_obj_name == '0':
            ip_poc_cmd = 'set security policies from-zone %s to-zone %s policy %s match destination-address %s' %(
                s_zone,d_zone,policy_name,ip_obj)

        else:
            ip_poc_cmd = 'set security policies from-zone %s to-zone %s policy %s match destination-address %s-%s' % (
            s_zone,d_zone,policy_name,ip_obj,ip_obj_name)

        ip_obj_list.append(ip_obj)
        print(ip_poc_cmd)
def asa_obj_group_creator(ip_list):
    for i3 in ip_list:
        ip_obj_cmd = 'network-object host %s' %i3
        print(ip_obj_cmd)




ip_list = []
ip_obj_list = []
users_choice = {'ASA': ['Create object group network',],
                'Junos':['1. Create object','2. Create policy'],
                }


# menu = u
# --------- Choose a option ---------
# \033[32;1m1.    ASA
# 2.  Junos
# 3. logout
#
#
# menu_dic = {'1': asa_obj_group_creator,
#             '2': junos_obj_creator,
#             '3': logout,
#             }

while True:
    for k in users_choice:
        print(k)
    #print(menu)
    your_choice = input('Please choose which type of device you want to configure(press q to quit):')
    #your_choice = input(">>:").strip()
    #if your_choice in menu_dic:
     #   menu_dic[your_choice]()
    if your_choice == 'ASA':
        ip_begin = input('Start IP:')
        ip_end = input('End IP:')
        iprange_creator(ip_begin, ip_end)
        asa_obj_group_creator(ip_list)
    elif your_choice == 'Junos':
        while True:
            for v in users_choice['Junos']:
                print(v)
            your_choice2 = input('Please input what do you want to do:')
            if your_choice2 == '1':
                ip_begin = input('Start IP:')
                ip_end = input('End IP:')
                nmask = input('Network Subnet /xx:')
                ip_obj_name = input('object name(default none):')
                if len(ip_obj_name) == 0:
                    ip_obj_name = '0'
                s_zone = input('Source Zone:')
                iprange_creator(ip_begin, ip_end)
                junos_obj_creator(s_zone, ip_list, ip_obj_name)
            elif your_choice2 == '2':
                s_zone = input('Source Zone(Just press Enter for lookup):')
                d_zone = input('Destination Zone(Just press Enter for lookup):')
                ip_begin = input('Start IP:')
                ip_end = input('End IP:')
                nmask = input('Network Subnet /xx:')
                ip_obj_name = input('object name(default none):')
                policy_name = input('policy name:')
                if len(ip_obj_name) == 0:
                    ip_obj_name = '0'

                iprange_creator(ip_begin, ip_end)
                junos_policy_creator(s_zone,d_zone,ip_list,policy_name)
            elif your_choice2 == 'q':
                exit()
            else:
                print('please input a vaild choice!')

    elif your_choice == 'q':
        exit()
    else:
        print('please input a vaild choice!')





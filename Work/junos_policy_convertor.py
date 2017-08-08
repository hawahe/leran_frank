#用于JuniperSRX-to-SRX的策略转换
import paramiko,re

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
                        #print(zone[-1])
                        client.close()
                        return zone[-1]

def junos_all_zone_list(hostname,username,password,except_zone):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # client.connect(hostname, username, password, '22')
    client.connect(hostname=hostname, username=username, password=password, port=22)
    stdin, stdout, stderr = client.exec_command("show security zones terse")
    all_zone = stdout.readlines()
    zone_list = []
    for i in all_zone:
        if not i.strip().startswith('Zone') or i.strip().startswith(' '):
            zone_name = i.split()
            if zone_name[0] == except_zone:
                continue
            else:
                zone_list.append(zone_name[0])
        else:
            continue
    return zone_list

zone_name = "SRX-TO-BG"
# policy_name = 'anything'
f1 = open('junos_policy.txt', 'r')
# policy = []
# policy_group = []
# i = 1
# for line in f1:
#     i += 1
#     if i%4 == 0:
#         policy_group.append(policy)
#         policy = []
#     else:
#        policy.append(line)


any_policy = []
continue_flag = 4

for line in f1:

    if continue_flag > 2:
        line_list = line.split()
        if line_list[10] == "source-address":
            if line_list[-1] == 'any' or line_list[-1] == "10.0.0.0/8":
                continue_flag = 0
                any_policy.append(line)
                continue
            elif re.match(r"10\.12\.0\.[0-9]+/[0-9]+",line_list[-1]):
               zone_name = "IT-Public-Server policy"
               line_list[4] = "IT-Public-Server policy"
               network_obj = " ".join(line_list)
               print(network_obj)
            else:
                network_list = line_list[-1].split("/")
                ipaddr = network_list[0]
                zone_name = junos_zone_lookup("x.x.x.x", "username", "password", ipaddr)
                line_list[4] = str(zone_name)
                network_obj = " ".join(line_list)
                print(network_obj)
        else:
            line_list[4] = str(zone_name)
            network_obj = " ".join(line_list)
            print(network_obj)
    else:
        continue_flag += 1
        any_policy.append(line)
        continue
zone_list = junos_all_zone_list("x.x.x.x", "username", "password","Network-Team-Mangement")
for zone in zone_list:
    if zone != "trust" and zone != "untrust" and zone != "junos-host" and zone != "Manangment" \
            and zone!= "ShuJuBu" and zone != "DMZ" :
        for policy in any_policy:
            policy_list = policy.split()
            policy_list[4] = str(zone)
            network_obj = " ".join(policy_list)
            print(network_obj)
        print("set security zones security-zone %s address-book address 10.0.0.0/8 10.0.0.0/8" %zone)
    else:
        continue

f1.close()

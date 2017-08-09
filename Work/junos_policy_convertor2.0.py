#迁移ASA策略使用

import paramiko,re,IPy
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

def junos_policy_verification(hostname,username,password,szone,dzone,protocol,sipaddr,sport,dipaddr,dport):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #client.connect(hostname, username, password, '22')
    client.connect(hostname=hostname, username=username, password=password, port=22)
    stdin, stdout, stderr = client.exec_command('show security match-policies from-zone %s to-zone %s '
                                                'protocol %s source-ip %s source-port %s destination-ip '
                                                '%s destination-port %s' %(szone,dzone,protocol,sipaddr,sport,dipaddr,dport))
    result = stdout.readlines()
    policy_name_list = result[0]
    policy_name = policy_name_list.split(',')
    policy_name = policy_name[0].split()
    actiontype = policy_name_list.split(',')
    actiontype = actiontype[1].split()

    return [policy_name[-1],actiontype[-1]]



ipaddress = input("ip address for login:")
username = input("username for login:")
password = input("password for login:")

Target_ip = r"10\.255\.248\.[0-9]+"
zone_list = junos_all_zone_list(ipaddress,username,password,"IT-Public-Server")
f = open('ASApolicy.txt' , 'r')
for line in f:
    Source_zone = "IT-Public-Server"
    Destination_zone = "IT-Public-Server"
    ASApolicy_list = line.split()
    policy_count = ASApolicy_list[0]+'-1'
    if ASApolicy_list[1] == 'ip':
        application_obj_1 = 'any'
        application_obj_2 = 'any'
        application_obj_3 = 'any'
        if re.match(Target_ip,ASApolicy_list[2]):        #源是迁移地址
            if re.match(r"[0-9]+\.[0-9]+\.[0-9]+\.0$",ASApolicy_list[2]):                 #源是迁移地址并且是网段；
                source_obj = IPy.IP(ASApolicy_list[2]).make_net(ASApolicy_list[3])
                if ASApolicy_list[4] == 'any':
                    Destination_zone = 'SRX-TO-BG'
                    destination_obj = 'any'
                else:
                    Destination_zone = junos_zone_lookup(ipaddress,username,password, ASApolicy_list[4])
                    if re.match(r"[0-9]+\.[0-9]+\.[0-9]+\.0$", ASApolicy_list[4]): #源是迁移地址并且是网段，目的是网段
                        destination_obj = str(IPy.IP(ASApolicy_list[5]).make_net(ASApolicy_list[6]))
                    else :                                                           #源是迁移地址并且是网段，目的是单个地址
                        destination_obj = ASApolicy_list[4]+"/32"


            else:                                                               #源是迁移地址并且是单个地址
                source_obj = ASApolicy_list[2]+"/32"
                if ASApolicy_list[3] == 'any':
                    Destination_zone = 'SRX-TO-BG'
                    destination_obj = 'any'
                else:
                    Destination_zone = junos_zone_lookup(ipaddress,username,password, ASApolicy_list[3])
                    if re.match(r"[0-9]+\.[0-9]+\.[0-9]+\.0$", ASApolicy_list[3]):  # 源是迁移地址并且是单个地址，目的是网段
                        destination_obj = str(IPy.IP(ASApolicy_list[3]).make_net(ASApolicy_list[4]))
                    else: # 源是迁移地址并且是单个地址，目的是单个地址
                        destination_obj = ASApolicy_list[3] + "/32"
        else:
            Source_zone = junos_zone_lookup(ipaddress, username, password, ASApolicy_list[2])
            if ASApolicy_list[2] == 'any':
                Source_zone = 'SRX-TO-BG'
                source_obj = 'any'
                if re.match(r"[0-9]+\.[0-9]+\.[0-9]+\.0$", ASApolicy_list[3]):
                    destination_obj = IPy.IP(ASApolicy_list[3]).make_net(ASApolicy_list[4])
                else:
                    destination_obj = ASApolicy_list[3] + "/32"
            elif re.match(r"[0-9]+\.[0-9]+\.[0-9]+\.0$", ASApolicy_list[2]):
                Source_zone = junos_zone_lookup(ipaddress, username, password, ASApolicy_list[2])
                source_obj = str(IPy.IP(ASApolicy_list[2]).make_net(ASApolicy_list[3]))
                if re.match(r"[0-9]+\.[0-9]+\.[0-9]+\.0$", ASApolicy_list[4]):
                    destination_obj = IPy.IP(ASApolicy_list[4]).make_net(ASApolicy_list[5])
                else:
                    destination_obj = ASApolicy_list[4] + "/32"

            else:
                source_obj = ASApolicy_list[2] + "/32"
                Source_zone = junos_zone_lookup(ipaddress, username, password, ASApolicy_list[2])
                if re.match(r"[0-9]+\.[0-9]+\.[0-9]+\.0$", ASApolicy_list[3]):
                    destination_obj = IPy.IP(ASApolicy_list[3]).make_net(ASApolicy_list[4])
                else:
                    destination_obj = ASApolicy_list[3] + "/32"

    elif ASApolicy_list[1] == 'udp':
        application_obj_1 = 'UDP_'+ ASApolicy_list[-1]
        application_obj_2 = 'udp'
        application_obj_3 = ASApolicy_list[-1]
        if re.match(Target_ip, ASApolicy_list[2]):  # 源是迁移地址
            if re.match(r"[0-9]+\.[0-9]+\.[0-9]+\.0$", ASApolicy_list[2]):  # 源是迁移地址并且是网段；
                source_obj = IPy.IP(ASApolicy_list[2]).make_net(ASApolicy_list[3])
                if ASApolicy_list[4] == 'any':
                    Destination_zone = 'SRX-TO-BG'
                    destination_obj = 'any'
                else:
                    Destination_zone = junos_zone_lookup(ipaddress, username, password, ASApolicy_list[4])
                    if re.match(r"[0-9]+\.[0-9]+\.[0-9]+\.0$", ASApolicy_list[4]):  # 源是迁移地址并且是网段，目的是网段
                        destination_obj = str(IPy.IP(ASApolicy_list[5]).make_net(ASApolicy_list[6]))
                    else:  # 源是迁移地址并且是网段，目的是单个地址
                        destination_obj = ASApolicy_list[4] + "/32"


            else:  # 源是迁移地址并且是单个地址
                source_obj = ASApolicy_list[2] + "/32"
                if ASApolicy_list[3] == 'any':
                    Destination_zone = 'SRX-TO-BG'
                    destination_obj = 'any'
                else:
                    Destination_zone = junos_zone_lookup(ipaddress, username, password, ASApolicy_list[3])
                    if re.match(r"[0-9]+\.[0-9]+\.[0-9]+\.0$", ASApolicy_list[3]):  # 源是迁移地址并且是单个地址，目的是网段
                        destination_obj = str(IPy.IP(ASApolicy_list[3]).make_net(ASApolicy_list[4]))
                    else:  # 源是迁移地址并且是单个地址，目的是单个地址
                        destination_obj = ASApolicy_list[3] + "/32"
        else:
            if ASApolicy_list[2] == 'any':
                Source_zone = 'SRX-TO-BG'
                source_obj = 'any'
                if re.match(r"[0-9]+\.[0-9]+\.[0-9]+\.0$", ASApolicy_list[3]):
                    destination_obj = IPy.IP(ASApolicy_list[3]).make_net(ASApolicy_list[4])
                else:
                    destination_obj = ASApolicy_list[3] + "/32"
            elif re.match(r"[0-9]+\.[0-9]+\.[0-9]+\.0$", ASApolicy_list[2]):
                Source_zone = junos_zone_lookup(ipaddress, username, password, ASApolicy_list[2])
                source_obj = str(IPy.IP(ASApolicy_list[2]).make_net(ASApolicy_list[3]))
                if re.match(r"[0-9]+\.[0-9]+\.[0-9]+\.0$", ASApolicy_list[4]):
                    destination_obj = IPy.IP(ASApolicy_list[4]).make_net(ASApolicy_list[5])
                else:
                    destination_obj = ASApolicy_list[4] + "/32"

            else:
                source_obj = ASApolicy_list[2] + "/32"
                Source_zone = junos_zone_lookup(ipaddress, username, password, ASApolicy_list[2])
                if re.match(r"[0-9]+\.[0-9]+\.[0-9]+\.0$", ASApolicy_list[3]):
                    destination_obj = IPy.IP(ASApolicy_list[3]).make_net(ASApolicy_list[4])
                else:
                    destination_obj = ASApolicy_list[3] + "/32"
    elif ASApolicy_list[1] == 'tcp':
        application_obj_1 = 'TCP_'+ ASApolicy_list[-1]
        application_obj_2 = 'tcp'
        application_obj_3 = ASApolicy_list[-1]
        if re.match(Target_ip, ASApolicy_list[2]):  # 源是迁移地址
            if re.match(r"[0-9]+\.[0-9]+\.[0-9]+\.0$", ASApolicy_list[2]):  # 源是迁移地址并且是网段；
                source_obj = IPy.IP(ASApolicy_list[2]).make_net(ASApolicy_list[3])
                if ASApolicy_list[4] == 'any':
                    Destination_zone = 'SRX-TO-BG'
                    destination_obj = 'any'
                else:
                    Destination_zone = junos_zone_lookup(ipaddress, username, password, ASApolicy_list[4])
                    if re.match(r"[0-9]+\.[0-9]+\.[0-9]+\.0$", ASApolicy_list[4]):  # 源是迁移地址并且是网段，目的是网段
                        destination_obj = str(IPy.IP(ASApolicy_list[5]).make_net(ASApolicy_list[6]))
                    else:  # 源是迁移地址并且是网段，目的是单个地址
                        destination_obj = ASApolicy_list[4] + "/32"


            else:  # 源是迁移地址并且是单个地址
                source_obj = ASApolicy_list[2] + "/32"
                if ASApolicy_list[3] == 'any':
                    Destination_zone = 'SRX-TO-BG'
                    destination_obj = 'any'
                else:
                    Destination_zone = junos_zone_lookup(ipaddress, username, password, ASApolicy_list[3])
                    if re.match(r"[0-9]+\.[0-9]+\.[0-9]+\.0$", ASApolicy_list[3]):  # 源是迁移地址并且是单个地址，目的是网段
                        destination_obj = str(IPy.IP(ASApolicy_list[3]).make_net(ASApolicy_list[4]))
                    else:  # 源是迁移地址并且是单个地址，目的是单个地址
                        destination_obj = ASApolicy_list[3] + "/32"
        else:
            if ASApolicy_list[2] == 'any':
                Source_zone = 'SRX-TO-BG'
                source_obj = 'any'
                if re.match(r"[0-9]+\.[0-9]+\.[0-9]+\.0$", ASApolicy_list[3]):
                    destination_obj = IPy.IP(ASApolicy_list[3]).make_net(ASApolicy_list[4])
                else:
                    destination_obj = ASApolicy_list[3] + "/32"
            elif re.match(r"[0-9]+\.[0-9]+\.[0-9]+\.0$", ASApolicy_list[2]):
                Source_zone = junos_zone_lookup(ipaddress, username, password, ASApolicy_list[2])
                source_obj = str(IPy.IP(ASApolicy_list[2]).make_net(ASApolicy_list[3]))
                if re.match(r"[0-9]+\.[0-9]+\.[0-9]+\.0$", ASApolicy_list[4]):
                    destination_obj = IPy.IP(ASApolicy_list[4]).make_net(ASApolicy_list[5])
                else:
                    destination_obj = ASApolicy_list[4] + "/32"

            else:
                Source_zone = junos_zone_lookup(ipaddress, username, password, ASApolicy_list[2])
                source_obj = ASApolicy_list[2] + "/32"
                if re.match(r"[0-9]+\.[0-9]+\.[0-9]+\.0$", ASApolicy_list[3]):
                    destination_obj = IPy.IP(ASApolicy_list[3]).make_net(ASApolicy_list[4])
                else:
                    destination_obj = ASApolicy_list[3] + "/32"





    create_source_obj = "set security zones security-zone %s address-book address %s %s" \
                                        % (Source_zone, source_obj, source_obj)
    create_destination_obj = "set security zones security-zone %s address-book address %s %s" \
                                                 % (Destination_zone, destination_obj, destination_obj)
    create_application_obj = "set applications application %s protocol %s destination-port %s " \
                                                 % (application_obj_1,application_obj_2,application_obj_3)
    create_policy1 = "set security policies from-zone %s to-zone %s policy %s-policy-%s  match source-address %s " \
                     "destination-address %s application %s " % (
                         Source_zone, Destination_zone, Source_zone,
                         policy_count, source_obj, destination_obj, application_obj_1)
    create_policy2 = "set security policies from-zone %s to-zone %s policy %s-policy-%s then permit" \
                     % (Source_zone, Destination_zone, Source_zone, policy_count)
    if source_obj != 'any':
        print(create_source_obj)
    elif source_obj == 'any':
        pass
    elif source_obj == '10.0.0.0/8':
        print(create_source_obj)


    else:
        pass
    if application_obj_3 != 'any':
        print(create_application_obj)
    else:
        pass
    if destination_obj != 'any':
        print(create_destination_obj)
    else:
        pass

    print(create_policy1)
    print(create_policy2)
    if 'source-address 10.0.0.0/8'in create_policy1 or 'source-address any'in create_policy1:
        for zone in zone_list:
            if zone != "trust" and zone != "untrust" and zone != "junos-host" and zone != "Manangment" \
                    and zone != "ShuJuBu" and zone != "DMZ":
                    policy_list = create_policy1.split()
                    policy_list[4] = str(zone)
                    network_obj = " ".join(policy_list)
                    print(network_obj)
                    policy_list = create_policy2.split()
                    policy_list[4] = str(zone)
                    network_obj = " ".join(policy_list)
                    print(network_obj)
                    print("set security zones security-zone %s address-book address 10.0.0.0/8 10.0.0.0/8" % zone)
            else:
                continue
    elif 'destination-address 10.0.0.0/8' in create_policy1 or 'destination-address any' in create_policy1:
        for zone in zone_list:
            if zone != "trust" and zone != "untrust" and zone != "junos-host" and zone != "Manangment" \
                    and zone != "ShuJuBu" and zone != "DMZ":
                    policy_list = create_policy1.split()
                    policy_list[6] = str(zone)
                    network_obj = " ".join(policy_list)
                    print(network_obj)
                    policy_list = create_policy2.split()
                    policy_list[6] = str(zone)
                    network_obj = " ".join(policy_list)
                    print(network_obj)
                    print("set security zones security-zone %s address-book address 10.0.0.0/8 10.0.0.0/8" % zone)
            else:
                continue
    else:
        pass
f.close()
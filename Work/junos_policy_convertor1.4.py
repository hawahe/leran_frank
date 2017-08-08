#开通JuniperSRX新策略使用

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
                    else:
                        return 'none'
        else:
            return "none"

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


Source_zone =  "Network-Team-Mangement"
Destination_zone = "Network-Team-Mangement"
Target_ip = r"10\.12\.3\.[0-9]+"
f = open('ASApolicy.txt' , 'r')
for line in f:
    policy_count = 36
    ASApolicy_list = line.split()
    if ASApolicy_list[0] == 'ip':
        if re.match(r"10\.12\.3\.[0-9]+",ASApolicy_list[1]):        #源是迁移地址
            if re.match(r"[0-9]+\.[0-9]+\.[0-9]+\.0$",ASApolicy_list[1]):                 #源是迁移地址并且是网段；
                source_obj = IPy.IP(ASApolicy_list[1]).make_net(ASApolicy_list[2])
                create_source_obj = "set security zones security-zone %s address-book address %s %s" \
                                    % (Source_zone, source_obj, source_obj)
                Destination_zone = junos_zone_lookup("x.x.x.x", "username", "password", ASApolicy_list[3])
                if ASApolicy_list[3] == 'any':
                    Destination_zone = 'SRX-TO-BG'
                    destination_obj = 'any'
                    create_destination_obj = ' '
                    create_policy1 = "set security policies from-zone %s to-zone %s policy %s-policy-%s  match " \
                                     "source-address %s destination-address %s application any " \
                                     % (Source_zone, Destination_zone, Source_zone,policy_count, source_obj,destination_obj)
                    create_policy2 = "set security policies from-zone %s to-zone %s policy %s-policy-%s then permit" \
                                 % (Source_zone, Destination_zone, Source_zone, policy_count)
                elif re.match(r"[0-9]+\.[0-9]+\.[0-9]+\.0$", ASApolicy_list[3]): #源是迁移地址并且是网段，目的是网段
                    destination_obj = str(IPy.IP(ASApolicy_list[3]).make_net(ASApolicy_list[4]))
                    create_destination_obj = "set security zones security-zone %s address-book address %s %s" \
                                             % (Destination_zone, destination_obj,destination_obj)
                    create_policy1 = "set security policies from-zone %s to-zone %s policy %s-policy-%s  match " \
                                     "source-address %s destination-address %s application any " \
                                     % (Source_zone, Destination_zone, Source_zone,policy_count, source_obj,destination_obj)
                    create_policy2 = "set security policies from-zone %s to-zone %s policy %s-policy-%s then permit" \
                                 % (Source_zone, Destination_zone, Source_zone, policy_count)
                else:                                               #源是迁移地址并且是网段，目的是单个地址
                    create_destination_obj = "set security zones security-zone %s address-book address %s/32 %s/32" \
                                             % (Destination_zone, ASApolicy_list[3], ASApolicy_list[3])
                    create_policy1 = "set security policies from-zone %s to-zone %s policy %s-policy-%s  match " \
                                     "source-address %s destination-address %s/32 application any " \
                                     % (
                                     Source_zone, Destination_zone, Source_zone, policy_count, source_obj, ASApolicy_list[3])
                    create_policy2 = "set security policies from-zone %s to-zone %s policy %s-policy-%s then permit" \
                                     % (Source_zone, Destination_zone, Source_zone, policy_count)
            else:                                                   #源是迁移地址，并且是单个地址
                create_source_obj = "set security zones security-zone %s address-book address %s/32 %s/32" \
                                    % (Source_zone, ASApolicy_list[1], ASApolicy_list[1])
                Destination_zone = junos_zone_lookup("x.x.x.x", "username", "password", ASApolicy_list[2])
                if ASApolicy_list[2] == 'any':
                    Destination_zone = 'SRX-TO-BG'
                    destination_obj = 'any'
                    create_destination_obj = ' '
                    create_policy1 = "set security policies from-zone %s to-zone %s policy %s-policy-%s  match " \
                                     "source-address %s destination-address %s application any " \
                                     % (Source_zone, Destination_zone, Source_zone,policy_count, source_obj,destination_obj)
                    create_policy2 = "set security policies from-zone %s to-zone %s policy %s-policy-%s then permit" \
                                 % (Source_zone, Destination_zone, Source_zone, policy_count)
                elif re.match(r"[0-9]+\.[0-9]+\.[0-9]+\.0$", ASApolicy_list[2]):            #源是迁移地址且是单个地址，目的是网段
                    destination_obj = IPy.IP(ASApolicy_list[2]).make_net(ASApolicy_list[3])
                    create_destination_obj = "set security zones security-zone %s address-book address %s %s" \
                                             % (Destination_zone, destination_obj, destination_obj)
                    create_policy1 = "set security policies from-zone %s to-zone %s policy %s-policy-%s  match " \
                                     "source-address %s/32 destination-address %s application any " \
                                     % (
                                     Source_zone, Destination_zone, Source_zone, policy_count, ASApolicy_list[1], destination_obj)
                    create_policy2 = "set security policies from-zone %s to-zone %s policy %s-policy-%s then permit" \
                                     % (Source_zone, Destination_zone, Source_zone, policy_count)
                else:                                               #源是迁移地址且是单个地址，目的是单个地址
                    create_destination_obj = "set security zones security-zone %s address-book address %s/32 %s/32" \
                                             % (Destination_zone, ASApolicy_list[2], ASApolicy_list[2])

                    create_policy1 = "set security policies from-zone %s to-zone %s policy %s-policy-%s  match source-address %s/32 " \
                                     "destination-address %s/32 application any " % (
                                     Source_zone, Destination_zone, Source_zone,
                                     policy_count, ASApolicy_list[1], ASApolicy_list[2])
                    create_policy2 = "set security policies from-zone %s to-zone %s policy %s-policy-%s then permit" \
                                     % (Source_zone, Destination_zone, Source_zone, policy_count)
        else:                                                                             #目的迁移地址
            if ASApolicy_list[1] == 'any':
                Destination_zone = 'SRX-TO-BG'
                source_obj = 'any'
                if re.match(r"[0-9]+\.[0-9]+\.[0-9]+\.0$", ASApolicy_list[2]):
                    destination_obj = IPy.IP(ASApolicy_list[2]).make_net(ASApolicy_list[3])
                    create_source_obj = ' '
                    create_destination_obj = "set security zones security-zone %s address-book address %s %s" \
                                                  % (Destination_zone, destination_obj, destination_obj)
                    create_policy1 = "set security policies from-zone %s to-zone %s policy %s-policy-%s  match " \
                                     "source-address %s destination-address %s application any " \
                                     % (
                                     Source_zone, Destination_zone, Source_zone, policy_count, source_obj, destination_obj)
                    create_policy2 = "set security policies from-zone %s to-zone %s policy %s-policy-%s then permit" \
                                     % (Source_zone, Destination_zone, Source_zone, policy_count)
                else:
            elif re.match(r"[0-9]+\.[0-9]+\.[0-9]+\.0$", ASApolicy_list[1]):                #目的是迁移地址，源是网段
                source_obj = IPy.IP(ASApolicy_list[1]).make_net(ASApolicy_list[2])
                Source_zone = junos_zone_lookup("x.x.x.x", "username", "password", ASApolicy_list[1])
                create_source_obj = "set security zones security-zone %s address-book address %s %s" \
                                    % (Source_zone, source_obj, source_obj)
                if re.match(r"[0-9]+\.[0-9]+\.[0-9]+\.0$", ASApolicy_list[3]):            #目的是迁移地址，并且是网段；源也是网段
                     destination_obj = IPy.IP(ASApolicy_list[3]).make_net(ASApolicy_list[4])
                     create_destination_obj = "set security zones security-zone %s address-book address %s %s" \
                                              % (Destination_zone, destination_obj, destination_obj)
                     create_policy1 = "set security policies from-zone %s to-zone %s policy %s-policy-%s  match " \
                                      "source-address %s destination-address %s application any " \
                                      % (
                                      Source_zone, Destination_zone, Source_zone, policy_count, source_obj, destination_obj)
                     create_policy2 = "set security policies from-zone %s to-zone %s policy %s-policy-%s then permit" \
                                      % (Source_zone, Destination_zone, Source_zone, policy_count)
                else:                                                #目的是迁移地址，并且是单个地址，源是网段
                    create_destination_obj = "set security zones security-zone %s address-book address %s/32 %s/32" \
                                             % (Destination_zone, ASApolicy_list[3], ASApolicy_list[3])
                    create_policy1 = "set security policies from-zone %s to-zone %s policy %s-policy-%s  match source-address %s " \
                                     "destination-address %s/32 application any " % (
                                         Source_zone, Destination_zone, Source_zone,
                                         policy_count, source_obj, ASApolicy_list[3])
                    create_policy2 = "set security policies from-zone %s to-zone %s policy %s-policy-%s then permit" \
                                     % (Source_zone, Destination_zone, Source_zone, policy_count)
            else:                                                    #目的是迁移地址，源是单个地址
                Source_zone = junos_zone_lookup("x.x.x.x", "username", "password", ASApolicy_list[1])
                create_source_obj = "set security zones security-zone %s address-book address %s/32 %s/32" \
                                    % (Source_zone, ASApolicy_list[1],ASApolicy_list[1])
                if re.match(r"[0-9]+\.[0-9]+\.[0-9]+\.0$", ASApolicy_list[2]):            #目的是迁移地址，源是单个地址
                    destination_obj = IPy.IP(ASApolicy_list[2]).make_net(ASApolicy_list[3])
                    create_destination_obj = "set security zones security-zone %s address-book address %s %s" \
                                             % (Destination_zone, destination_obj, destination_obj)
                    create_policy1 = "set security policies from-zone %s to-zone %s policy %s-policy-%s  match " \
                                     "source-address %s/32 destination-address %s application any " \
                                     % (
                                         Source_zone, Destination_zone, Source_zone, policy_count, ASApolicy_list[1],
                                         destination_obj)
                    create_policy2 = "set security policies from-zone %s to-zone %s policy %s-policy-%s then permit" \
                                     % (Source_zone, Destination_zone, Source_zone, policy_count)
                else:                                               #目的是迁移地址且是单个地址，源是单个地址
                    create_destination_obj = "set security zones security-zone %s address-book address %s/32 %s/32" \
                                             % (Destination_zone, ASApolicy_list[2], ASApolicy_list[2])
                    create_policy1 = "set security policies from-zone %s to-zone %s policy %s-policy-%s  match source-address %s/32 " \
                                     "destination-address %s/32 application any " % (
                                         Source_zone, Destination_zone, Source_zone,
                                         policy_count, ASApolicy_list[1], ASApolicy_list[2])
                    create_policy2 = "set security policies from-zone %s to-zone %s policy %s-policy-%s then permit" \
                                     % (Source_zone, Destination_zone, Source_zone, policy_count)
        print(create_source_obj)
        print(create_destination_obj)
        print(create_policy1)
        print(create_policy2)

    elif ASApolicy_list[0] == 'udp':
        if re.match(r"10\.12\.3\.[0-9]+", ASApolicy_list[1]):      # 源是迁移地址
            if re.match(r"[0-9]+\.[0-9]+\.[0-9]+\.0$", ASApolicy_list[1]):  # 源是迁移地址并且是网段；
                source_obj = IPy.IP(ASApolicy_list[1]).make_net(ASApolicy_list[2])
                create_source_obj = "set security zones security-zone %s address-book address %s %s" \
                                    % (Source_zone, source_obj, source_obj)
                Destination_zone = junos_zone_lookup("x.x.x.x", "username", "password", ASApolicy_list[3])
                if re.match(r"[0-9]+\.[0-9]+\.[0-9]+\.0$", ASApolicy_list[3]):  # 源是迁移地址并且是网段，目的是网段
                    destination_obj = IPy.IP(ASApolicy_list[3]).make_net(ASApolicy_list[4])
                    create_destination_obj = "set security zones security-zone %s address-book address %s %s" \
                                             % (Destination_zone, destination_obj, destination_obj)
                    create_application_obj = "set applications application UDP_%s protocol udp destination-port %s " \
                                             % (ASApolicy_list[5], ASApolicy_list[5])
                    create_policy1 = "set security policies from-zone %s to-zone %s policy %s-policy-%s  match " \
                                     "source-address %s destination-address %s application UDP_%s " \
                                     % (
                                     Source_zone, Destination_zone, Source_zone, policy_count, source_obj, destination_obj,
                                     ASApolicy_list[5])
                    create_policy2 = "set security policies from-zone %s to-zone %s policy %s-policy-%s then permit" \
                                     % (Source_zone, Destination_zone, Source_zone, policy_count)
                else:  # 源是迁移地址并且是网段，目的是单个地址
                    create_destination_obj = "set security zones security-zone %s address-book address %s/32 %s/32" \
                                             % (Destination_zone, ASApolicy_list[3], ASApolicy_list[3])
                    create_application_obj = "set applications application UDP_%s protocol udp destination-port %s " \
                                             % (ASApolicy_list[4], ASApolicy_list[4])
                    create_policy1 = "set security policies from-zone %s to-zone %s policy %s-policy-%s  match " \
                                     "source-address %s destination-address %s/32 application UDP_%s " \
                                     % (
                                         Source_zone, Destination_zone, Source_zone, policy_count, source_obj,
                                         ASApolicy_list[3],
                                         ASApolicy_list[4])
                    create_policy2 = "set security policies from-zone %s to-zone %s policy %s-policy-%s then permit" \
                                     % (Source_zone, Destination_zone, Source_zone, policy_count)
            else:  # 源是迁移地址，并且是单个地址
                create_source_obj = "set security zones security-zone %s address-book address %s/32 %s/32" \
                                    % (Source_zone, ASApolicy_list[1], ASApolicy_list[1])
                Destination_zone = junos_zone_lookup("x.x.x.x", "username", "password", ASApolicy_list[2])
                if re.match(r"[0-9]+\.[0-9]+\.[0-9]+\.0$", ASApolicy_list[2]):  # 源是迁移地址且是单个地址，目的是网段
                    destination_obj = IPy.IP(ASApolicy_list[2]).make_net(ASApolicy_list[3])
                    create_destination_obj = "set security zones security-zone %s address-book address %s %s" \
                                             % (Destination_zone, destination_obj, destination_obj)
                    create_application_obj = "set applications application UDP_%s protocol udp destination-port %s " \
                                             % (ASApolicy_list[4], ASApolicy_list[4])
                    create_policy1 = "set security policies from-zone %s to-zone %s policy %s-policy-%s  match " \
                                     "source-address %s/32 destination-address %s application UDP_%s " \
                                     % (
                                         Source_zone, Destination_zone, Source_zone, policy_count, ASApolicy_list[1],
                                         destination_obj,
                                         ASApolicy_list[4])
                    create_policy2 = "set security policies from-zone %s to-zone %s policy %s-policy-%s then permit" \
                                     % (Source_zone, Destination_zone, Source_zone, policy_count)
                else:  # 源是迁移地址且是单个地址，目的是单个地址
                    create_destination_obj = "set security zones security-zone %s address-book address %s/32 %s/32" \
                                             % (Destination_zone, ASApolicy_list[2], ASApolicy_list[2])
                    create_application_obj = "set applications application UDP_%s protocol udp destination-port %s " \
                                             % (ASApolicy_list[3], ASApolicy_list[3])
                    create_policy1 = "set security policies from-zone %s to-zone %s policy %s-policy-%s  match source-address %s/32 " \
                                     "destination-address %s/32 application UDP_%s " % (
                                         Source_zone, Destination_zone, Source_zone,
                                         policy_count, ASApolicy_list[1], ASApolicy_list[2], ASApolicy_list[3])
                    create_policy2 = "set security policies from-zone %s to-zone %s policy %s-policy-%s then permit" \
                                     % (Source_zone, Destination_zone, Source_zone, policy_count)
        else:  # 目的迁移地址
            if re.match(r"[0-9]+\.[0-9]+\.[0-9]+\.0$", ASApolicy_list[1]):  # 目的是迁移地址，源是网段
                source_obj = IPy.IP(ASApolicy_list[1]).make_net(ASApolicy_list[2])
                Source_zone = junos_zone_lookup("x.x.x.x", "username", "password", ASApolicy_list[1])
                create_source_obj = "set security zones security-zone %s address-book address %s %s" \
                                    % (Source_zone, source_obj, source_obj)
                if re.match(r"[0-9]+\.[0-9]+\.[0-9]+\.0$", ASApolicy_list[3]):  # 目的是迁移地址，并且是网段；源也是网段
                    destination_obj = IPy.IP(ASApolicy_list[3]).make_net(ASApolicy_list[4])
                    create_destination_obj = "set security zones security-zone %s address-book address %s %s" \
                                             % (Destination_zone, destination_obj, destination_obj)
                    create_application_obj = "set applications application UDP_%s protocol udp destination-port %s " \
                                             % (ASApolicy_list[5], ASApolicy_list[5])
                    create_policy1 = "set security policies from-zone %s to-zone %s policy %s-policy-%s  match " \
                                     "source-address %s destination-address %s application UDP_%s " \
                                     % (
                                         Source_zone, Destination_zone, Source_zone, policy_count, source_obj,
                                         destination_obj,
                                         ASApolicy_list[5])
                    create_policy2 = "set security policies from-zone %s to-zone %s policy %s-policy-%s then permit" \
                                     % (Source_zone, Destination_zone, Source_zone, policy_count)
                else:  # 目的是迁移地址，并且是单个地址，源是网段
                    create_destination_obj = "set security zones security-zone %s address-book address %s/32 %s/32" \
                                             % (Destination_zone, ASApolicy_list[3], ASApolicy_list[3])
                    create_application_obj = "set applications application UDP_%s protocol udp destination-port %s " \
                                             % (ASApolicy_list[4], ASApolicy_list[4])
                    create_policy1 = "set security policies from-zone %s to-zone %s policy %s-policy-%s  match source-address %s " \
                                     "destination-address %s/32 application UDP_%s " % (
                                         Source_zone, Destination_zone, Source_zone,
                                         policy_count, source_obj, ASApolicy_list[3], ASApolicy_list[4])
                    create_policy2 = "set security policies from-zone %s to-zone %s policy %s-policy-%s then permit" \
                                     % (Source_zone, Destination_zone, Source_zone, policy_count)
            else:  # 目的是迁移地址，源是单个地址
                Source_zone = junos_zone_lookup("x.x.x.x", "username", "password", ASApolicy_list[1])
                create_source_obj = "set security zones security-zone %s address-book address %s/32 %s/32" \
                                    % (Source_zone, ASApolicy_list[1], ASApolicy_list[1])
                if re.match(r"[0-9]+\.[0-9]+\.[0-9]+\.0$", ASApolicy_list[2]):  # 目的是迁移地址，源是单个地址
                    destination_obj = IPy.IP(ASApolicy_list[2]).make_net(ASApolicy_list[3])
                    create_destination_obj = "set security zones security-zone %s address-book address %s %s" \
                                             % (Destination_zone, destination_obj, destination_obj)
                    create_application_obj = "set applications application UDP_%s protocol udp destination-port %s " \
                                             % (ASApolicy_list[4], ASApolicy_list[4])
                    create_policy1 = "set security policies from-zone %s to-zone %s policy %s-policy-%s  match " \
                                     "source-address %s/32 destination-address %s application UDP_%s " \
                                     % (
                                         Source_zone, Destination_zone, Source_zone, policy_count, ASApolicy_list[1],
                                         destination_obj,
                                         ASApolicy_list[4])
                    create_policy2 = "set security policies from-zone %s to-zone %s policy %s-policy-%s then permit" \
                                     % (Source_zone, Destination_zone, Source_zone, policy_count)
                else:  # 目的是迁移地址且是单个地址，源是单个地址
                    create_destination_obj = "set security zones security-zone %s address-book address %s/32 %s/32" \
                                             % (Destination_zone, ASApolicy_list[2], ASApolicy_list[2])
                    create_application_obj = "set applications application UDP_%s protocol udp destination-port %s " \
                                             % (ASApolicy_list[3], ASApolicy_list[3])
                    create_policy1 = "set security policies from-zone %s to-zone %s policy %s-policy-%s  match source-address %s/32 " \
                                     "destination-address %s/32 application UDP_%s " % (
                                         Source_zone, Destination_zone, Source_zone,
                                         policy_count, ASApolicy_list[1], ASApolicy_list[2], ASApolicy_list[3])
                    create_policy2 = "set security policies from-zone %s to-zone %s policy %s-policy-%s then permit" \
                                     % (Source_zone, Destination_zone, Source_zone, policy_count)
        print(create_source_obj)
        print(create_destination_obj)
        print(create_application_obj)
        print(create_policy1)
        print(create_policy2)

    elif re.match(r"10\.12\.3\.[0-9]+",ASApolicy_list[0]):        #源是迁移地址
        if re.match(r"[0-9]+\.[0-9]+\.[0-9]+\.0$",ASApolicy_list[0]):                 #源是迁移地址并且是网段；
            source_obj = IPy.IP(ASApolicy_list[0]).make_net(ASApolicy_list[1])
            create_source_obj = "set security zones security-zone %s address-book address %s %s" \
                                % (Source_zone, source_obj, source_obj)
            Destination_zone = junos_zone_lookup("x.x.x.x", "username", "password", ASApolicy_list[2])
            if re.match(r"[0-9]+\.[0-9]+\.[0-9]+\.0$", ASApolicy_list[2]):            #源是迁移地址并且是网段，目的是网段
                destination_obj = IPy.IP(ASApolicy_list[2]).make_net(ASApolicy_list[3])
                create_destination_obj = "set security zones security-zone %s address-book address %s %s" \
                                         % (Destination_zone, destination_obj,destination_obj)
                create_application_obj = "set applications application TCP_%s protocol tcp destination-port %s " \
                                         % (ASApolicy_list[4], ASApolicy_list[4])
                create_policy1 = "set security policies from-zone %s to-zone %s policy %s-policy-%s  match " \
                                 "source-address %s destination-address %s application TCP_%s " \
                                 % (Source_zone, Destination_zone, Source_zone,policy_count, source_obj,destination_obj,
                                    ASApolicy_list[4])
                create_policy2 = "set security policies from-zone %s to-zone %s policy %s-policy-%s then permit" \
                             % (Source_zone, Destination_zone, Source_zone, policy_count)
            else:                                               #源是迁移地址并且是网段，目的是单个地址
                create_destination_obj = "set security zones security-zone %s address-book address %s/32 %s/32" \
                                         % (Destination_zone, ASApolicy_list[2], ASApolicy_list[2])
                create_application_obj = "set applications application TCP_%s protocol tcp destination-port %s " \
                                         % (ASApolicy_list[3], ASApolicy_list[3])
                create_policy1 = "set security policies from-zone %s to-zone %s policy %s-policy-%s  match " \
                                 "source-address %s destination-address %s/32 application TCP_%s " \
                                 % (
                                 Source_zone, Destination_zone, Source_zone, policy_count, source_obj, ASApolicy_list[2],
                                 ASApolicy_list[3])
                create_policy2 = "set security policies from-zone %s to-zone %s policy %s-policy-%s then permit" \
                                 % (Source_zone, Destination_zone, Source_zone, policy_count)
        else:                                                   #源是迁移地址，并且是单个地址
            create_source_obj = "set security zones security-zone %s address-book address %s/32 %s/32" \
                                % (Source_zone, ASApolicy_list[0], ASApolicy_list[0])
            Destination_zone = junos_zone_lookup("x.x.x.x", "username", "password", ASApolicy_list[1])
            if re.match(r"[0-9]+\.[0-9]+\.[0-9]+\.0$", ASApolicy_list[1]):            #源是迁移地址且是单个地址，目的是网段
                destination_obj = IPy.IP(ASApolicy_list[1]).make_net(ASApolicy_list[2])
                create_destination_obj = "set security zones security-zone %s address-book address %s %s" \
                                         % (Destination_zone, destination_obj, destination_obj)
                create_application_obj = "set applications application TCP_%s protocol tcp destination-port %s " \
                                         % (ASApolicy_list[3], ASApolicy_list[3])
                create_policy1 = "set security policies from-zone %s to-zone %s policy %s-policy-%s  match " \
                                 "source-address %s/32 destination-address %s application TCP_%s " \
                                 % (
                                 Source_zone, Destination_zone, Source_zone, policy_count, ASApolicy_list[0], destination_obj,
                                 ASApolicy_list[3])
                create_policy2 = "set security policies from-zone %s to-zone %s policy %s-policy-%s then permit" \
                                 % (Source_zone, Destination_zone, Source_zone, policy_count)
            else:                                               #源是迁移地址且是单个地址，目的是单个地址
                create_destination_obj = "set security zones security-zone %s address-book address %s/32 %s/32" \
                                         % (Destination_zone, ASApolicy_list[1], ASApolicy_list[1])
                create_application_obj = "set applications application TCP_%s protocol tcp destination-port %s " \
                                         % (ASApolicy_list[2], ASApolicy_list[2])
                create_policy1 = "set security policies from-zone %s to-zone %s policy %s-policy-%s  match source-address %s/32 " \
                                 "destination-address %s/32 application TCP_%s " % (
                                 Source_zone, Destination_zone, Source_zone,
                                 policy_count, ASApolicy_list[0], ASApolicy_list[1], ASApolicy_list[2])
                create_policy2 = "set security policies from-zone %s to-zone %s policy %s-policy-%s then permit" \
                                 % (Source_zone, Destination_zone, Source_zone, policy_count)
    else:                                                       #目的迁移地址
        if re.match(r"[0-9]+\.[0-9]+\.[0-9]+\.0$", ASApolicy_list[0]):                #目的是迁移地址，源是网段
            source_obj = IPy.IP(ASApolicy_list[0]).make_net(ASApolicy_list[1])
            Source_zone = junos_zone_lookup("x.x.x.x", "username", "password", ASApolicy_list[0])
            create_source_obj = "set security zones security-zone %s address-book address %s %s" \
                                % (Source_zone, source_obj, source_obj)
            if re.match(r"[0-9]+\.[0-9]+\.[0-9]+\.0$", ASApolicy_list[2]):            #目的是迁移地址，并且是网段；源也是网段
                 destination_obj = IPy.IP(ASApolicy_list[2]).make_net(ASApolicy_list[3])
                 create_destination_obj = "set security zones security-zone %s address-book address %s %s" \
                                          % (Destination_zone, destination_obj, destination_obj)
                 create_application_obj = "set applications application TCP_%s protocol tcp destination-port %s " \
                                          % (ASApolicy_list[4], ASApolicy_list[4])
                 create_policy1 = "set security policies from-zone %s to-zone %s policy %s-policy-%s  match " \
                                  "source-address %s destination-address %s application TCP_%s " \
                                  % (
                                  Source_zone, Destination_zone, Source_zone, policy_count, source_obj, destination_obj,
                                  ASApolicy_list[4])
                 create_policy2 = "set security policies from-zone %s to-zone %s policy %s-policy-%s then permit" \
                                  % (Source_zone, Destination_zone, Source_zone, policy_count)
            else:                                                #目的是迁移地址，并且是单个地址，源是网段
                create_destination_obj = "set security zones security-zone %s address-book address %s/32 %s/32" \
                                         % (Destination_zone, ASApolicy_list[2], ASApolicy_list[2])
                create_application_obj = "set applications application TCP_%s protocol tcp destination-port %s " \
                                         % (ASApolicy_list[3], ASApolicy_list[3])
                create_policy1 = "set security policies from-zone %s to-zone %s policy %s-policy-%s  match source-address %s " \
                                 "destination-address %s/32 application TCP_%s " % (
                                     Source_zone, Destination_zone, Source_zone,
                                     policy_count, source_obj, ASApolicy_list[2], ASApolicy_list[3])
                create_policy2 = "set security policies from-zone %s to-zone %s policy %s-policy-%s then permit" \
                                 % (Source_zone, Destination_zone, Source_zone, policy_count)
        else:                                                    #目的是迁移地址，源是单个地址
            Source_zone = junos_zone_lookup("x.x.x.x", "username", "password", ASApolicy_list[0])
            create_source_obj = "set security zones security-zone %s address-book address %s/32 %s/32" \
                                % (Source_zone, ASApolicy_list[0],ASApolicy_list[0])
            if re.match(r"[0-9]+\.[0-9]+\.[0-9]+\.0$", ASApolicy_list[1]):            #目的是迁移地址，源是单个地址
                destination_obj = IPy.IP(ASApolicy_list[1]).make_net(ASApolicy_list[2])
                create_destination_obj = "set security zones security-zone %s address-book address %s %s" \
                                         % (Destination_zone, destination_obj, destination_obj)
                create_application_obj = "set applications application TCP_%s protocol tcp destination-port %s " \
                                         % (ASApolicy_list[3], ASApolicy_list[3])
                create_policy1 = "set security policies from-zone %s to-zone %s policy %s-policy-%s  match " \
                                 "source-address %s/32 destination-address %s application TCP_%s " \
                                 % (
                                     Source_zone, Destination_zone, Source_zone, policy_count, ASApolicy_list[0],
                                     destination_obj,
                                     ASApolicy_list[3])
                create_policy2 = "set security policies from-zone %s to-zone %s policy %s-policy-%s then permit" \
                                 % (Source_zone, Destination_zone, Source_zone, policy_count)
            else:                                               #目的是迁移地址且是单个地址，源是单个地址
                create_destination_obj = "set security zones security-zone %s address-book address %s/32 %s/32" \
                                         % (Destination_zone, ASApolicy_list[1], ASApolicy_list[1])
                create_application_obj = "set applications application TCP_%s protocol tcp destination-port %s " \
                                         % (ASApolicy_list[2], ASApolicy_list[2])
                create_policy1 = "set security policies from-zone %s to-zone %s policy %s-policy-%s  match source-address %s/32 " \
                                 "destination-address %s/32 application TCP_%s " % (
                                     Source_zone, Destination_zone, Source_zone,
                                     policy_count, ASApolicy_list[0], ASApolicy_list[1], ASApolicy_list[2])
                create_policy2 = "set security policies from-zone %s to-zone %s policy %s-policy-%s then permit" \
                                 % (Source_zone, Destination_zone, Source_zone, policy_count)



    print(create_source_obj)
    print(create_destination_obj)
    print(create_application_obj)
    print(create_policy1)
    print(create_policy2)
f.close()

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
                        #print(zone[-1])
                        client.close()
                        return zone[-1]
f1 = open('networkOBJ.txt', 'r')
for line in f1:
    line_list = line.split()
    if line_list[4] == "IT-Public-Server":
        continue
    else:
        network_list = line_list[-1].split("/")
        ipaddr = network_list[0]
        zone_name = junos_zone_lookup("x.x.x.x","username","password",ipaddr)
        line_list[4] = zone_name
        network_obj = " ".join(line_list)
        print(network_obj)
    #
    # f1 = open('cinema_ip.txt', 'r')
    # for line in f1:
    #     line = line.replace('\n', '')
    #     ip_list.append(line)
    # print(ip_list)
    # f1.close()


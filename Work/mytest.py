import paramiko
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


zone_list = junos_all_zone_list("x.x.x.x", "username", "password","IT-Public-Server policy")
for zone in zone_list:
    if zone != "trust" and zone !="untrust":
        print(zone)
    else:
        continue
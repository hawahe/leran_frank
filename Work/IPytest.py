import paramiko
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





print(junos_policy_verification('10.0.3.201','zhaobohua','Bibolang1','SRX-TO-BG','Old-ShuJuBu','tcp','10.12.60.60','11111','10.14.250.151','22'))

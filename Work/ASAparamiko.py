import paramiko


'''
ip = '10.0.0.70'
username = 'username'
password = 'password'
remote_conn_pre=paramiko.SSHClient()
remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
remote_conn_pre.connect(ip, username=username, password=password,
                        look_for_keys=False, allow_agent=False)
remote_conn = remote_conn_pre.invoke_shell()
output = remote_conn.recv(65535)
print(output)
remote_conn.send('enable\n')
remote_conn.send('ecc0m@Test\n')
remote_conn.send('show run\n')
output = remote_conn.recv(65535)
print (output)
'''


secret = 'ecc0m@Test'
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname='10.0.0.70', username='username', password='password', port=22)
stdin, stdout, stderr = client.exec_command('enable')
stdin, stdout, stderr = client.exec_command(secret)
stdin, stdout, stderr = client.exec_command('terminal pager 0')
stdin, stdout, stderr = client.exec_command('more system:running-config')
f = open('asa-showrun.txt' 'a+',encoding='utf8')
a = stdout.readlines()
for i in a:
    f.write(i)
f.close()

ssh.close()
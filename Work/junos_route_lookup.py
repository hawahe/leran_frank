import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname='x.x.x.x', username='username', password='password', port=22)
stdin, stdout, stderr = client.exec_command('show route 10.14.250.1')
a = stdout.readlines()
for i in a:
    #i.strip().startswith('>'):
    p = i.split()
    print(p)
stdin, stdout, stderr = client.exec_command('show interface %s' %p[-1])
b = stdout.readlines()
for i2 in b:
    if i2.strip().startswith('Security: Zone:'):
        p2 = i2.split()
        print(p2[-1])


#f = open('asa-showrun.txt' 'a+',encoding='utf8')
#a = stdout.read()
#print(a.decode())
#for i in a:
#    f.write(i)
#f.close()

client.close()
import pexpect


def network_backup_for_ASA():
    child = pexpect.spawn('ssh %s@10.0.0.70' %username)
    child.expect('.*assword:.*')
    child.sendline(password1)

    child.expect('.*> ')
    child.sendline('ena')
    child.expect('.*assword:.*')
    child.sendline(password2)

    child.sendline('terminal pager 0')

    child.sendline('more system:running-config')
    child.expect(': end.*')
    runningconfig = child.before.decode("utf-8")
    print(runningconfig)
    child.close()

username = input('input username:')
password1 = input('input password:') # that's why you should be really carefull where to store this script!
password2 = input('input enable password:')

network_backup_for_ASA()
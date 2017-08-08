import getpass


_username = "zhaobohua"
_password = "abc123"

username = input("username:")
password = getpass.getpass("password:")

if _username == username and _password == password:
    print ("Welcome user {name} login ....".format(name=username))
else:
    print("Invalid username or password!")


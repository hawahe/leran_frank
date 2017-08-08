password_list = ['*#*#','12345']
def account_login():
    tries = 3
    while tries > 0:
        password = input('Password:')
        password_correct = password == password_list[-1]
        password_rest = password == password_list[0]
        if password_correct:
            print ('Login success!')
        elif password_rest:
            new_password = input('Enter a new password:')
            password_list.append(new_password)
            print('Your password has changed successfully!')
            account_login()
        else:
            print('Wrong password or invalid input!')
            tries = tries - 1
            print(tries, 'times left')
    else:
        print('Your account has been suspended')
account_login()
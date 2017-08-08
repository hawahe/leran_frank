import os,time,json
from core import db_handler
from conf import setting



def acc_auth(account,password):
    '''
    account auth func
    :param account: credit account number
    :param password: credit card password
    :return: if passed the authentication , return the account object, otherwise, return None
    '''
    db_path = db_handler.db_handler(setting.DATABASE)
    account_file = "%s/%s.jason" %(db_path,account)
    print(account_file)
    if os.path.isfile(account_file):
        with open(account_file,'r') as f:
            account_data = json.load(f)
            if account_data['password'] == password:
                exp_time_stamp = time.mktime(time.strptime(account_data['expire_data'],"%Y-%m-%d"))
                if time.time() > exp_time_stamp:
                    print("Account [%s] has expired, please contact the back to get a new account" %account)
                else:
                    return account_data
            else:
                print("Account ID or password is incorrect!")
    else:
        print("Account [%s] does not exist!" % account)


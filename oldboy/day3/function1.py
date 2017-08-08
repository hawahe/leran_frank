


# def change_name():
#     global name
#     name = 'alex'
#
# change_name()
# print(name)

def calc(n):
    print(n)
    if int(n/2) > 0:
        return calc(int(n/2))
    print('->',n)
calc(10)
def mobile(number):
    CN_mobile = [134, 135, 136, 137, 138, 139, 150, 151, 152, 157, 158, 159, 182, 183, 184, 187, 188, 147, 178, 1705]
    CN_union = [130, 131, 132, 155, 156, 185, 186, 145, 176, 1709]
    CN_telecom = [133, 153, 180, 181, 189, 177, 1700]

    if ''.join(list_number[:4]) in str(CN_mobile):
        print('Operator : China Mobile')
        print("We're sending verification code via text to your phone: ", number)

    elif ''.join(list_number[:4]) in str(CN_union):
        print('Operator : China Union')
        print("We're sending verification code via text to your phone: ", number)

    elif ''.join(list_number[:4]) in str(CN_telecom):
        print('Operator : China Telecom')
        print("We're sending verification code via text to your phone: ", number)
    else:
        if ''.join(list_number[:3]) in str(CN_mobile):
            print('Operator : China Mobile')
            print("We're sending verification code via text to your phone: ",number)
        elif ''.join(list_number[:3]) in str(CN_union):
            print('Operator : China Union')
            print("We're sending verification code via text to your phone: ",number)

        elif ''.join(list_number[:3]) in str(CN_telecom):
            print('Operator : China Telecom')
            print("We're sending verification code via text to your phone: ",number)
        else:
            print('No such a operator')
            register()
def register():
    your_phone = input('Enter Your number:')
    if len(your_phone) == 11:

        mobile(your_phone)
    else:
        print("Invalid length, your number should be in 11 digits")
        register()
register()






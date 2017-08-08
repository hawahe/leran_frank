user_interface = ["I'm a Customer",
                  "I'm a StoreKeeper",
]


while True:
    for index,interface in enumerate(user_interface):   #打印user_interface选项等待用户选择；
        print(index,interface)
    First_Choice = input('Please choose a entrance>>>:')
    if First_Choice.isdigit() and int(First_Choice) <= len(user_interface) and int(First_Choice) >= 0:  #判断用户的选项是数字、并且该数字小于选项的长度并且大于0
        if First_Choice == str(user_interface.index("I'm a Customer")): #判断用户的选项是否选择顾客入口；
            f = open('production_list2.txt','r')    #将产品列表从文件中读出放入列表
            product_list = []
            for line in f:
                product_list.append(line.split())
            print('')
            f.close()
            f1 = open('shopping_list.txt','r+') #将用户已购物信息从文件中打开放入列表
            shopping_cart = []
            for line1 in f1:
                shopping_cart.append(line1.split())
            f1.close()
            with open('salary.txt','r') as f3:  #判断用户是否第一次输入薪水数目
                salary = f3.read()
            while salary == 'none':
                salary = input('Please input your salary:') #如果是第一次输入薪水，那么输入；否则跳过输入薪水的循环
                if salary.isdigit():
                    salary = int(salary)
                    break
                else:
                    print('Please input digtal number')
                    continue
            while True:
                for index, item in enumerate(product_list): #循环打印商品列表；
                    print(index + 1, item[0], item[1])
                choice = input('>>>:')
                if choice.isdigit() and int(choice) <= len(product_list) and int(choice) > 0: #判断用户的选项是数字、并且该数字小于选项的长度并且大于0
                    choice = int(choice)
                    if int(product_list[choice - 1][1]) <= int(salary): #判断用户的薪水是否足够购买该商品，是的话用薪水余额减去商品价格
                        print('added [%s] to your shopping cart.' % product_list[choice - 1][0])
                        shopping_cart.append(product_list[choice - 1])
                        salary = int(salary)
                        salary -= int(product_list[choice - 1][1])
                        print('Your banlance is \033[31;1m%s\033[0m' % (salary))
                    else:   #否则打印余额不足
                        print('\033[41;1mYour balance is not enough to buy it.\033[0m')
                elif choice == 'q': #输入q退出购买循环
                    break
                else:
                    print('Please input vaild option.')
            print('You have bought below:')     #循环打印已购买的商品
            f2 = open('shopping_list.txt','a+')
            for item in shopping_cart:
                print(item)
                f2.write(str(item))
            f2.close()
            print('Your banlance is \033[31;1m%s\033[0m' % (salary))    #显示薪水余额
            with open('salary.txt','w') as f3:
                f3.write(str(salary))
            exit()
        if First_Choice == str(user_interface.index("I'm a StoreKeeper")):  #进入商家窗口
            f = open('production_list2.txt', 'r')   #读取商品列表并放入一个列表
            product_list = []
            for line in f:
                product_list.append(line.split())
            f.close()
            while True:
                for index, item in enumerate(product_list): #循环打印现有的商品列表
                    print(index + 1, item[0], item[1])
                choice = input('input 0 to add new item or input other number to modify price,press q to quit>>>:')
                if choice.isdigit() and int(choice) <= len(product_list) and int(choice) > 0:   #用户选择修改商品价格
                    choice = int(choice)
                    modify_price = int(input('Please input a new price>>>:'))
                    product_list[choice - 1][1] = modify_price  #修改商品价格列表后打印，并写入文件
                    with open('production_list2.txt','w') as f5:
                        for line2 in product_list:
                            f5.writelines(str(line2).replace(',',' ').replace('[','').replace(']','\n').replace("'",'').replace('  ',' '))

                elif choice == 'q': #退出程序
                    exit()
                elif choice == '0': #用户选择‘0’，进入添加商品的窗口；
                    while True:
                        new_product = input('Please input new product name>>>:')
                        new_price = input('Please input new price>>>:')
                        if new_product != 'q' or new_price != 'q':
                            with open('production_list2.txt','a+') as f5:
                                f5.write('\n'+new_product)
                                f5.write(' ')
                                f5.write(new_price)
                                print('The new production list as below:')
                                print(new_product,' ',new_price)
                                continue
                        else:
                            exit()
                elif choice == 'q':
                    break
                else:
                    print('Please input vaild option.')
            print('You have bought below:')     #打印已经购买的商品并写入文件；
            f2 = open('shopping_list.txt','a+')
            for item in shopping_cart:
                print(item)
                f2.write(str(item).replace(',',' ').replace('[','').replace(']','\n').replace("'",'').replace('  ',' '))
            f2.close()
            print('Your banlance is \033[31;1m%s\033[0m' % (salary))
            with open('salary.txt','w') as f3:
                f3.write(str(salary))
            exit()
    elif First_Choice == 'q':
        exit()
    else:
        print('Please input  a vaild option.')




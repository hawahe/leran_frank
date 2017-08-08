import random


def roll_dice(numbers=3, points=None):
    print('<<<<< ROLL THE DICE! >>>>>')
    if points is None:
        points = []
    while numbers > 0:
        point = random.randrange(1,7)
        points.append(point)
        numbers = numbers - 1
    return points
def roll_result(total):
    isBig = 11 <= total <= 18
    isSmall = 3 <= total <=10
    if isBig:
        return 'Big'
    elif isSmall:
        return 'Small'
def start_game():
    print('<<<<< GAME STARTS! >>>>>')
    first_money = 1000
    choices = ['Big','Small']
    while first_money > 0:
        your_choice = input('Big or Small :')
        your_bet = int(input('How much you wanna bet ?'))
        if your_bet > first_money:
            print("You don't have enough money, please bet again ! ")

        else:
            if your_choice in choices:
                points = roll_dice()
                total = sum(points)
                youWin = your_choice == roll_result(total)
                if youWin:
                    print('The points are',points, 'You win !')
                    first_money = first_money + your_bet
                    print("You gained",your_bet,"you have",first_money,'now')
                else:
                    print('The points are',points,'You lose !')
                    first_money = first_money - your_bet
                    print("You love",your_bet,"you have",first_money,'now')
            else:
                print('Invalid Words')
                start_game()
    else:
        print('GAME OVER !')





start_game()
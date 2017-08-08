

age_of_oldboy = 56
count = 3
while count > 0:
    guess_age = int(input("guess age:"))

    if guess_age == age_of_oldboy:
        print("yes, you got it.")
        break
    elif guess_age > age_of_oldboy:
        print("Think smaller...")
    else:
        print("Think bigger!")
    count -= 1
    if count == 0:
        countine_confirm = input("do you want to keep guessing..?")
        if countine_confirm != "n":
            count = 3
if count == 0:
    print ("Good bye!")

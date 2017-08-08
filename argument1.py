def trapezoid_area(base_up, base_down, height = 3):
    return 1 / 2 * (base_up + base_down) * height


print(trapezoid_area(1,2,height=15))

print('   *', '  * *', '* * *', '   |  ', sep='\n')

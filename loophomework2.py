amount_v = int(input('principal amount:'))
rate_v = float(input('expected rate:'))
time_v = int(input('principal time:'))
def invest(amount,rate,time):
    total = 1
    for i in range(1,time+1):
        total = total * (1 + rate)
        total_final = total * amount
        print('year {}: ${}'.format(i,total_final))
invest(amount_v,rate_v,time_v)


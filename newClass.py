class CocaCola:
    formula = ['caffeine','sugar','water','soda']
    def __init__(self,logo_name):
       self.local_logo = logo_name
    def drink(self):
        print('Energy!')
coke = CocaCola('可口可乐')
print (coke.local_logo)









class Dog(object):
    n = 'Alex'
    def __init__ (self,name):
        self.name = name
    @classmethod
    def eat(self):
        print("%s is eating %s" % (self.n,'包子'))

    def talk(self):
        print('%s is talking' % self.name)



d = Dog('ChenRonghua')
d.eat()
d.talk()


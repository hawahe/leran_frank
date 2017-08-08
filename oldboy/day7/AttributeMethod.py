



class Dog(object):
    n = 'Alex'
    def __init__ (self,name):
        self.name = name
    @property
    def eat(self,food):
        print("%s is eating %s" % (self.name,food))

    def talk(self):
        print('%s is talking' % self.name)



d = Dog('ChenRonghua')
d.eat('baozi')
d.talk()




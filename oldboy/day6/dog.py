


class Dog:
    def __init__(self,name):
        self.name = name

    def bulk(self):
        print("%s: woof! woof!" % self.name)

d1 = Dog('dog1')
d2 = Dog('dog2')

d1.bulk()
d2.bulk()
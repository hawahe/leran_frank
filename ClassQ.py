class TestA:
    attr = 1
    def _init_(self):
        self.attr = 42
obj_a = TestA()
print (obj_a.attr)

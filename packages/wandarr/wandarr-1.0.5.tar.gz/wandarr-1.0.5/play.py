

class A:
    def __init__(self, d):
        self.data = d

    @property
    def num(self):
        return self.data["n"]

class B(A):
    def __init__(self):
        super().__init__({"n": 6})

    def p(self):
        print(self.num)


z = B()
z.p()



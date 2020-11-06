class Cat:
    species = "cat"
    @classmethod
    def cry(cls):
        print("发春")

    @staticmethod
    def eat(cls):
        cls.cry()

    def catch_mice(self):
        print("catch mouse")

class Babby(Cat):
    def catch_mice(self):
        print("don't like catch mouse")



tom = Cat()
tony = Babby()

def animal(cat):
    cat.catch_mice()



tom.cry()
tom.eat(Cat)

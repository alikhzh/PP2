class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    def __init__(self, name):
        super().__init__(name)

dog = Dog("Buddy")
print(dog.name)


class Vehicle:
    def start(self):
        print("Vehicle started")

class Car(Vehicle):
    def start(self):
        super().start()
        print("Car is ready")

car = Car()
car.start()


class Shape:
    def area(self):
        print("Calculating area")

class Square(Shape):
    def area(self):
        super().area()
        print("Square area")

sq = Square()
sq.area()
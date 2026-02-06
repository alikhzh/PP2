class Animal:
    def speak(self):
        print("Animal sound")

class Dog(Animal):
    def speak(self):
        print("Bark")

Dog().speak()


class Vehicle:
    def move(self):
        print("Vehicle moves")

class Bike(Vehicle):
    def move(self):
        print("Bike rides")

Bike().move()


class Person:
    def work(self):
        print("Working")

class Programmer(Person):
    def work(self):
        print("Coding")

Programmer().work()
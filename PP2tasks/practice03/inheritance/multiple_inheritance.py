class Flyer:
    def fly(self):
        print("Flying")

class Swimmer:
    def swim(self):
        print("Swimming")

class Duck(Flyer, Swimmer):
    pass

duck = Duck()
duck.fly()
duck.swim()


class Writer:
    def write(self):
        print("Writing")

class Speaker:
    def speak(self):
        print("Speaking")

class Blogger(Writer, Speaker):
    pass

blogger = Blogger()
blogger.write()
blogger.speak()
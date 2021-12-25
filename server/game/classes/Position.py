import math


class Position:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def update(self, x=0, y=0):
        self.x = x
        self.y = y

    def distance(self, pos):
        return math.sqrt(pow(self.x - pos.x, 2) + pow(self.y - pos.y, 2))

    def __add__(self, position):
        return Position(self.x + position.x, self.y + position.y)

    def __sub__(self, position):
        return Position(self.x - position.x, self.y - position.y)

    # def __setattr__(self, name, value):
    #     print(str(type(self))+' Set: '+name+'='+str(value))
    #     self.__dict__[name] = value

    # def __getattr__(self, name):
    #     print(str(type(self))+' Get: '+name)
    #     return exit()

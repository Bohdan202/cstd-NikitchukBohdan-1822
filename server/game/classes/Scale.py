class Scale:

    def __init__(self, value=1, max=1):
        self.value = value
        self.max = max

    # def __setattr__(self, name, value):
    #     print(str(type(self))+' Set: '+name+'='+str(value))
    #     self.__dict__[name] = value

    def __getattr__(self, name):
        print(str(type(self))+' Get: '+name)
        return exit()

    def getPercent(self):
        if self.max == 0:
            return 0
        return self.value / self.max

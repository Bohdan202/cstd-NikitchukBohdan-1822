from game.classes import Position

class Character:
    def __init__(self, uid, name=None, img=None, x=0, y=0):
        self.uid = uid
        self.name = name
        self.img = img
        self.pos = Position.Position()

    def distance(self, pos):
        return self.pos.distance(pos)

    def toJson(self):
        return {
            'name': self.name,
            'img': self.img,
            'pos': {
                'x': self.pos.x,
                'y': self.pos.y
            }
        }
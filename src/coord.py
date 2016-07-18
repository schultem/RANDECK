
class Coord(object):

    def __init__(self,x,y):
        self.x=x
        self.y=y

    def __iter__(self):
        return iter([self.x,self.y])

    def __add__(self, other):
        return Coord(self.x+other.x, self.y+other.y)

    def __str__(self):
        return 'Coord(%d,%d)'%(self.x,self.y)
 
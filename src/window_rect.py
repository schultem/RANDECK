from coord import Coord

class WindowRect(object):
    """WindowRect constructor requires a 4-tuple representing: (upper_left_x,upper_left_y,lower_right_x,lower_right_y)
    and results in corresponding members (origin_x,origin_y,x,y)+(width,height)"""
 
    def __init__(self, iterable):
        if len(iterable) != 4:
            raise Exception(self.__doc__)
        else:
            (self.origin_x, self.origin_y, self.x, self.y) = tuple(iterable)
            self.origin=Coord(self.origin_x, self.origin_y)

            self.width  = self.x - self.origin.x
            self.height = self.y - self.origin.y

            if self.width < 0 or self.height < 0:
                raise Exception(self.__doc__)

    def __iter__(self):
        return iter([self.origin_x,self.origin_y,self.x,self.y])
        
    def __str__(self):
        return 'WindowRect(width:%d, height:%d, (%d,%d,%d,%d))'%(self.width,self.height,self.origin.x,self.origin.y,self.x,self.y)
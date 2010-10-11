

class Position(object):
    def __init__(self, x=0, y=0):
        
        #this can probably be commented out in production
        if isinstance(x, Position) or isinstance(y, Position):
            raise ValueError('Position recursion detected!')
        
        self.x = int(x)
        self.y = int(y)

    def __repr__(self):
        return str((self.x,self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def moveUp(self):
        self.y += 1
        return self

    def moveDown(self):
        self.y -= 1
        return self
        
    def moveLeft(self):
        self.x -= 1
        return self
        
    def moveRight(self):
        self.x += 1
        return self

    def moveUpLeft(self):
        self.y += 1
        self.x -= 1
        return self

    def moveUpRight(self):
        self.y += 1
        self.x += 1
        return self

    def moveDownLeft(self):
        self.y -= 1
        self.x -= 1
        return self

    def moveDownRight(self):
        self.y -= 1
        self.x += 1
        return self


if __name__ == "__main__":
    p1 = Position(1,2)
    p2 = Position(2,3)
    print p1 == p1
    print p1 != p2


    
    

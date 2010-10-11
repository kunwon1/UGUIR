

class Position(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def moveUp(self):
        self.y -= 1

    def moveDown(self):
        self.y += 1
        
    def moveLeft(self):
        self.x -= 1
        
    def moveRight(self):
        self.x += 1



if __name__ == "__main__":
    p1 = Position(1,2)
    p2 = Position(2,3)
    print p1 == p1
    print p1 != p2


    
    

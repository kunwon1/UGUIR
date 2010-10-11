import random
from position import Position

class Rect(object):
    def __init__(self, pos, w, h):
        self.pos = pos
        self.w = w
        self.h = h

    def getPoint(self):
        randX = random.randint(self.pos.x+1, self.pos.x+self.w-1)
        randY = random.randint(self.pos.y+1, self.pos.y+self.h-1)
        return Position(randX,randY)

    def checkIntersect(self, other):
        for x in xrange(other.pos.x, other.pos.x + other.w + 1):
            for y in xrange(other.pos.y, other.pos.y + other.h + 1):
                if self.checkPointIntersect(Position(x, y)):
                    return True
        return False

    def checkPointIntersect(self, otherPos):
        if self.pos.x <= otherPos.x <= self.pos.x + self.w:
            if self.pos.y <= otherPos.y <= self.pos.y + self.h:
                return True
        return False

    def splitRect(self, splitPos):
        if not splitPos.x == 0 and not splitPos.y == 0:
            raise ValueError('splitRect must be called with either x or y set to 0')
            return
        if not splitPos.x == 0:
            leftSize = splitPos.x - self.pos.x
            rightSize = self.w - leftSize - 1
            leftRect = Rect(self.pos, leftSize, self.h)
            rightRect = Rect(Position(splitPos.x+1, self.pos.y), rightSize, self.h)
            return (leftRect, rightRect)
        else:
            bottomSize = splitPos.y - self.pos.y 
            topSize = self.h - bottomSize - 1
            bottomRect = Rect(self.pos, self.w, bottomSize)
            topRect = Rect(Position(self.pos.x, splitPos.y+1), self.w, topSize)
            return (bottomRect, topRect)
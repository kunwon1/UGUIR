from constants import *
import random

class BSP(object):
    def __init__(self, firstRect):
        self.firstRect = firstRect
        self.rects = []
        self.rects.append(self.firstRect)
        self.doBSP()

    def splitRand(self, rect):
        if random.randint(0,1) == 0:  # split on x
            min = rect.pos.x + MINIMUM_ROOM_SIZE + 1
            max = rect.pos.x + rect.w - MINIMUM_ROOM_SIZE - 1
            if not max > min:
                return [rect]
            randx = random.randint(min,max)
            return rect.splitRect(Position(randx,0))
        else:                           #split on y
            min = rect.pos.y + MINIMUM_ROOM_SIZE + 1
            max = rect.pos.y + rect.h - MINIMUM_ROOM_SIZE - 1
            if not max > min:
                return [rect]
            randy = random.randint(min,max)
            return rect.splitRect(Position(0,randy))

    def doBSP(self):
        iter = 0
        while iter <= BSP_RECURSION_DEPTH:
            newRects = []
            for rect in self.rects:
                rectsTuple = self.splitRand(rect)
                for item in rectsTuple:
                    newRects.append(item)
            self.rects = newRects
            iter += 1
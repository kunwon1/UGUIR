from pyglet.sprite import Sprite
import pyglet.graphics

pyglet.resource.path = ['res', 'res/images',]
pyglet.resource.reindex()

import random

from constants import *
from spritesheet import sheet
from player import Player
from monsters import *
from fov import fieldOfView

class Map:
    def __init__(self, width=DEFAULT_MAP_CELLS_X, height=DEFAULT_MAP_CELLS_Y):
        random.seed()
        self.map = []
        self.viewport = []
        (self.playerX, self.playerY) = (0,0)
        self.width, self.height = width, height
        self.playableArea = Rect(1,1,width-2,height-2)
        self.batch = pyglet.graphics.Batch()
        self.mapGroup = pyglet.graphics.OrderedGroup(0)
        self.monsterGroup = pyglet.graphics.OrderedGroup(1)
        self.playerGroup = pyglet.graphics.OrderedGroup(2)
        self.player = Player(x=0, y=0, batch=self.batch, group=self.playerGroup)
        
        for i in range(VIEWPORT_W):
            self.viewport.append([0]*VIEWPORT_H)
        self.initViewport()

        for x in range(width):
            list = []
            for y in range(height):
                list.append(MapCell(x*SPRITE_SIZE, y*SPRITE_SIZE, self.batch, self.mapGroup))
            self.map.append(list)
        
        bsp = BSP(self.playableArea)
        rooms = []
        for r in  bsp.rects:
            if random.randint(0,10) > 3:
                roomrect = self.makeRandRoom(r)
                rooms.append(roomrect)

        lastroom = None
        for i in rooms:
            if not lastroom is None:
                x1,y1 = lastroom.getPoint()
                x2,y2 = i.getPoint()
                self.randTunnel(x1,y1,x2,y2)
                lastroom = i
            else:
                px,py = i.getPoint()
                self.movePlayer(px,py)
                self.map[px+1][py+1].objects.append(Kobold(batch=self.batch, group=self.monsterGroup))
                lastroom = i

    def debugPrint(self):
        import sys
        
        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                if self.map[x][y].type == DUNGEON_WALL:
                    sys.stdout.write('#')
                elif self.map[x][y].visible == True:
                    sys.stdout.write(' ')
                elif self.map[x][y].type == DUNGEON_FLOOR:
                    sys.stdout.write('~')
            print '\n',

    def movePlayer(self, x, y):
        (xPx, yPx) = (self.player.x, self.player.y)
        (newX, newY) = (self.playerX + x, self.playerY + y)
        if self.map[newX][newY].blocked == True:
            return
        else:
            self.player.set_position(xPx + x*SPRITE_SIZE, yPx + y*SPRITE_SIZE)
            self.playerX = newX
            self.playerY = newY

    def initViewport(self):
        for x in range(len(self.viewport)):
            for y in range(len(self.viewport[x])):
                self.viewport[x][y] = Sprite(sheet['dungeon'][81], x=x * SPRITE_SIZE, y=y * SPRITE_SIZE, batch = self.batch, group = self.mapGroup)

    def updateViewport(self, width, height):
        startX = self.playerX - width / 2
        startY = self.playerY - height / 2
        endX = startX + width
        endY = startY + height
        mapLenX = len(self.map)
        mapLenY = len(self.map[0])
        
        if endX > mapLenX - 1:
            endX = mapLenX - 1
        if endY > mapLenY:
            endY = mapLenY - 1
        if startX < 0:
            startX = 0
        if startY < 0:
            startY = 0
        if endX - startX < VIEWPORT_W - 1:
            if startX < VIEWPORT_W:
                startX,endX = 0,VIEWPORT_W
            else:
                startX,endX = mapLenX - VIEWPORT_W, mapLenX 
        if endY - startY < VIEWPORT_H - 1:
            if startY < VIEWPORT_H:
                startY,endY = 0,VIEWPORT_H
            else:
                startY,endY = mapLenY - VIEWPORT_H, mapLenY

        for x in xrange(startX, endX):
            yIter = 0
            for y in xrange(startY, endY):
                self.map[x][y].visible = False

        self.doFOV()

        xIter = 0

        for x in xrange(startX, endX):
            yIter = 0
            for y in xrange(startY, endY):
                if x == self.playerX and y == self.playerY:
                    playerXPx = self.viewport[xIter][yIter].x
                    playerYPx = self.viewport[xIter][yIter].y 
                    self.player.set_position(playerXPx,playerYPx)
                if self.map[x][y].type == DUNGEON_WALL:
                    self.viewport[xIter][yIter].image = sheet['dungeon'][81]
                elif self.map[x][y].type == DUNGEON_FLOOR:
                    self.viewport[xIter][yIter].image = sheet['ground'][170]
                if self.map[x][y].discovered == False:
                    self.viewport[xIter][yIter].opacity = 0
                elif self.map[x][y].visible == False:
                    self.viewport[xIter][yIter].opacity = 128
                else:
                    self.viewport[xIter][yIter].opacity = 255
                for obj in self.map[x][y].objects:
                    obj.set_position(xIter*32,yIter*32)
                    if obj.blocked is True:
                        self.map[x][y].blocked = True
                yIter += 1
            xIter += 1

    def doFOV(self):
        fieldOfView(self.playerX,self.playerY,
                    self.width,self.height,15,
                    self.funcVisit,self.funcBlocked)

    def funcVisit(self,x,y):
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        self.map[x][y].visible = True
        self.map[x][y].discovered = True

    def funcBlocked(self,x,y):
        return self.map[x][y].blocked

    def makeRectRoom(self, rect):
        for r in xrange(rect.x, rect.x+rect.w):
            for n in xrange(rect.y, rect.y+rect.h):
                self.map[r][n].blocked = False
                self.map[r][n].type = DUNGEON_FLOOR
        return rect

    def makeHorizTunnel(self, y, x1, x2):
        if x1 > x2:
            (x1,x2) = (x2,x1)
        for x in xrange(x1, x2 + 1):
            self.map[x][y].blocked = False
            self.map[x][y].type = DUNGEON_FLOOR

    def makeVertTunnel(self, x, y1, y2):
        if y1 > y2:
            (y1,y2) = (y2,y1)
        for y in xrange(y1, y2 + 1):
            self.map[x][y].blocked = False
            self.map[x][y].type = DUNGEON_FLOOR

    def makeTwoLeggedTunnel(self, x1, y1, x2, y2):
        if random.randint(0,1) == 0:
            self.makeHorizTunnel(y1, x1, x2)
            self.makeVertTunnel(x2, y1, y2)
        else:
            self.makeVertTunnel(x1, y1, y2)
            self.makeHorizTunnel(y2, x1, x2)

    def makeDiagTunnel(self, x1, y1, x2, y2):
        '''see bresenham_line.py for license'''

        steep = abs(y2 - y1) > abs(x2 - x1)
        if steep:
            x1, y1 = y1, x1  
            x2, y2 = y2, x2

        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        if y1 < y2: 
            ystep = 1
        else:
            ystep = -1

        deltax = x2 - x1
        deltay = abs(y2 - y1)
        error = -deltax / 2
        y = y1

        for x in range(x1, x2 + 1):
            if steep:
                self.map[y][x].blocked = False
                self.map[y][x].type = DUNGEON_FLOOR
            else:
                self.map[x][y].blocked = False
                self.map[x][y].type = DUNGEON_FLOOR                
            error = error + deltay
            if error > 0:
                y = y + ystep
                error = error - deltax

    def randTunnel(self, x1, y1, x2, y2):
        if random.randint(0,10) > 3:
            self.makeTwoLeggedTunnel(x1,y1,x2,y2)
        else:
            self.makeDiagTunnel(x1,y1,x2,y2)

    def makeRandRoom(self, rect):
        subFromW = random.randint(1,5)
        subFromH = random.randint(1,5)
        addToX = subFromW / 2
        subFromW = subFromW - addToX
        addToY = subFromH / 2
        subFromH = subFromH - addToY
        
        x = rect.x + addToX
        y = rect.y + addToY
        w = rect.w - subFromW
        h = rect.h - subFromH
        
        if  w > 3 and h > 3:
            return self.makeRectRoom(Rect(x,y,w,h))
        else:
            return self.makeRectRoom(rect)

class Rect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def getPoint(self):
        randX = random.randint(self.x+1, self.x+self.w-1)
        randY = random.randint(self.y+1, self.y+self.h-1)
        return (randX,randY)

    def checkIntersect(self, other):
        for x in xrange(other.x, other.x + other.w + 1):
            for y in xrange(other.y, other.y + other.h + 1):
                if self.checkPointIntersect(x, y):
                    return True
        return False

    def checkPointIntersect(self, x, y):
        if self.x <= x <= self.x + self.w:
            if self.y <= y <= self.y + self.h:
                return True
        return False

    def splitRect(self, x=None, y=None):
        if x is not None and y is not None:
            raise ValueError('splitRect must be called with only one arg')
            return
        if x is not None:
            leftSize = x - self.x
            rightSize = self.w - leftSize - 1
            leftRect = Rect(self.x, self.y, leftSize, self.h)
            rightRect = Rect(x+1, self.y, rightSize, self.h)
            return (leftRect, rightRect)
        else:
            bottomSize = y - self.y 
            topSize = self.h - bottomSize - 1
            bottomRect = Rect(self.x, self.y, self.w, bottomSize)
            topRect = Rect(self.x, y+1, self.w, topSize)
            return (bottomRect, topRect)

class MapCell:
    def __init__(self, xCells, yCells, batch,
                 group, blocked=True, visible=True,
                 discovered=False):
        self.blocked = blocked
        self.visible = visible
        self.discovered = discovered
        self.batch = batch
        self.group = group
        self.xCells = xCells
        self.yCells = yCells
        self.xPx = self.xCells * SPRITE_SIZE
        self.yPx = self.yCells * SPRITE_SIZE
        self.type = DUNGEON_WALL
        self.objects = []

class BSP:
    def __init__(self, firstRect):
        self.firstRect = firstRect
        self.rects = []
        self.rects.append(self.firstRect)
        self.doBSP()

    def splitRand(self, rect):
        if random.randint(0,1) == 0:  # split on x
            min = rect.x + MINIMUM_ROOM_SIZE + 1
            max = rect.x + rect.w - MINIMUM_ROOM_SIZE - 1
            if not max > min:
                return [rect]
            randx = random.randint(min,max)
            return rect.splitRect(x=randx)
        else:                           #split on y
            min = rect.y + MINIMUM_ROOM_SIZE + 1
            max = rect.y + rect.h - MINIMUM_ROOM_SIZE - 1
            if not max > min:
                return [rect]
            randy = random.randint(min,max)
            return rect.splitRect(y=randy)

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
                
def isNearEdge(x,y):
    lowPass = CLOSE_TO_EDGE
    highPassX = VIEWPORT_W * SPRITE_SIZE - CLOSE_TO_EDGE
    highPassY = VIEWPORT_H * SPRITE_SIZE - CLOSE_TO_EDGE
    if lowPass <= x <= highPassX:
        if lowPass <= y <= highPassY:
            return False
    return True

if __name__ == '__main__':
    import sys
    
    map = Map(width=60,height=79)
    for x in range(len(map.map)):
        for y in range(len(map.map[x])):
            if map.map[x][y].type == DUNGEON_WALL:
                sys.stdout.write('#')
            elif map.map[x][y].type == DUNGEON_FLOOR:
                sys.stdout.write(' ')
        print '\n',
        
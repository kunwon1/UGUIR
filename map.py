from pyglet.sprite import Sprite
import pyglet.graphics

pyglet.resource.path = ['res', 'res/images',]
pyglet.resource.reindex()

import random
random.seed()

from constants import *
from spritesheet import sheet
from player import Player
from monsters import *
from fov import fieldOfView
from position import Position

class Map(object):
    def __init__(self, width=DEFAULT_MAP_CELLS_X, height=DEFAULT_MAP_CELLS_Y):
        self.map = []
        self.viewport = []
        self.width, self.height = width, height
        self.playableArea = Rect(Position(1,1),width-2,height-2)
        self.playerPos = Position()
        self.batch = pyglet.graphics.Batch()
        self.mapGroup = pyglet.graphics.OrderedGroup(0)
        self.monsterGroup = pyglet.graphics.OrderedGroup(1)
        self.playerGroup = pyglet.graphics.OrderedGroup(2)
        self.player = Player(pos=self.playerPos, batch=self.batch, group=self.playerGroup)
        
        for i in range(VIEWPORT_W):
            self.viewport.append([0]*VIEWPORT_H)
        self.initViewport()

        for x in range(width):
            lst = []
            for y in range(height):
                lst.append(MapCell(Position(x, y), self.batch, self.mapGroup))
            self.map.append(lst)

        bsp = BSP(self.playableArea)
        self.rooms = []
        for r in  bsp.rects:
            if random.randint(0,10) > 3:
                roomrect = self.makeRandRoom(r)
                self.rooms.append(roomrect)

        lastroom = None
        for i in self.rooms:
            if not lastroom is None:
                pos1 = lastroom.getPoint()
                pos2 = i.getPoint()
                self.randTunnel(pos1,pos2)
                lastroom = i
            else:
                pos = i.getPoint()
                self.movePlayer(pos)
                self.map[pos.x+1][pos.y+1].objects.append(Kobold(batch=self.batch, group=self.monsterGroup))
                lastroom = i

    def getCellAtPos(self, pos):
        return self.map[pos.x][pos.y]

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

    def movePlayer(self, pos):
        xPx, yPx = self.player.x, self.player.y
        newPos = Position(self.playerPos.x + pos.x, self.playerPos.y + pos.y)
        if self.map[newPos.x][newPos.y].blocked:
            if self.map[newPos.x][newPos.y].type == DUNGEON_DOOR:
                self.map[newPos.x][newPos.y].type = OPEN_DOOR
                self.map[newPos.x][newPos.y].blocked = False
            return
        else:
            self.player.set_position(xPx + pos.x * SPRITE_SIZE, yPx + pos.y * SPRITE_SIZE)
            self.playerPos = newPos
    
    def initViewport(self):
        for x in range(len(self.viewport)):
            for y in range(len(self.viewport[x])):
                self.viewport[x][y] = Sprite(sheet['dungeon'][81], 
                                             x=x * SPRITE_SIZE, 
                                             y=y * SPRITE_SIZE, 
                                             batch = self.batch, 
                                             group = self.mapGroup)

    def updateViewport(self, width, height):
        startX = self.playerPos.x - width / 2
        startY = self.playerPos.y - height / 2
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
            for y in xrange(startY, endY):
                self.map[x][y].visible = False

        self.doFOV()

        xIter = 0

        for x in xrange(startX, endX):
            yIter = 0
            for y in xrange(startY, endY):
                if x == self.playerPos.x and y == self.playerPos.y:
                    playerXPx = self.viewport[xIter][yIter].x
                    playerYPx = self.viewport[xIter][yIter].y
                    self.player.set_position(playerXPx,playerYPx)
                if self.map[x][y].type == DUNGEON_WALL:
                    self.viewport[xIter][yIter].image = sheet['dungeon'][81]
                elif self.map[x][y].type == DUNGEON_FLOOR:
                    self.viewport[xIter][yIter].image = sheet['ground'][170]
                elif self.map[x][y].type == DUNGEON_DOOR:
                    self.viewport[xIter][yIter].image = sheet['dungeon'][84]
                elif self.map[x][y].type == OPEN_DOOR:
                    self.viewport[xIter][yIter].image = sheet['dungeon'][85]
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
        fieldOfView(self.playerPos.x,self.playerPos.y,
                    self.width,self.height,15,
                    self.funcVisit,self.funcBlocked)

    def funcVisit(self,x,y):
        pos = Position(x,y)
        if pos.x < 0:
            pos.x = 0
        if pos.y < 0:
            pos.y = 0
        self.map[pos.x][pos.y].visible = True
        self.map[pos.x][pos.y].discovered = True

    def funcBlocked(self,x,y):
        return self.map[x][y].blocked

    def makeRectRoom(self, rect):
        for r in xrange(rect.pos.x, rect.pos.x+rect.w):
            for n in xrange(rect.pos.y, rect.pos.y+rect.h):
                self.map[r][n].blocked = False
                self.map[r][n].type = DUNGEON_FLOOR
        return rect

    def makeHorizTunnel(self, pos, x2):
        if pos.x > x2:
            (pos.x,x2) = (x2,pos.x)
        flag = 0
        for x in xrange(pos.x, x2 + 1):
            if self.map[x][pos.y].type == DUNGEON_DOOR:
                    continue
            doorPlacement = self.map[x][pos.y].checkDoorPlacement(self)
            self.map[x][pos.y].blocked = False
            self.map[x][pos.y].type = DUNGEON_FLOOR
            if flag < MAX_DOORS_PER_TUNNEL:
                if doorPlacement == True:
                    self.map[x][pos.y].type = DUNGEON_DOOR
                    self.map[x][pos.y].blocked = True
                    flag += 1

    def makeVertTunnel(self, pos, y2):
        if pos.y > y2:
            (pos.y,y2) = (y2,pos.y)
        flag = 0
        for y in xrange(pos.y, y2 + 1):
            if self.map[pos.x][y].type == DUNGEON_DOOR:
                    continue
            doorPlacement = self.map[pos.x][y].checkDoorPlacement(self)
            self.map[pos.x][y].blocked = False
            self.map[pos.x][y].type = DUNGEON_FLOOR
            if flag < MAX_DOORS_PER_TUNNEL:
                if doorPlacement == True:
                    self.map[pos.x][y].type = DUNGEON_DOOR
                    self.map[pos.x][y].blocked = True
                    flag += 1

    def makeTwoLeggedTunnel(self, pos1, pos2):
        if random.randint(0,1) == 0:
            self.makeHorizTunnel(pos1, pos2.x)
            self.makeVertTunnel(pos2, pos1.y)
        else:
            self.makeVertTunnel(pos1, pos2.y)
            self.makeHorizTunnel(pos2, pos1.x)

    def makeDiagTunnel(self, pos1, pos2):
        '''see bresenham_line.py for license'''
        self.firstDoor, self.secondDoor = False, False 
        steep = abs(pos2.y - pos1.y) > abs(pos2.x - pos1.x)
        if steep:
            pos1.x, pos1.y = pos1.y, pos1.x  
            pos2.x, pos2.y = pos2.y, pos2.x

        if pos1.x > pos2.x:
            pos1.x, pos2.x = pos2.x, pos1.x
            pos1.y, pos2.y = pos2.y, pos1.y

        if pos1.y < pos2.y: 
            ystep = 1
        else:
            ystep = -1

        deltax = pos2.x - pos1.x
        deltay = abs(pos2.y - pos1.y)
        error = -deltax / 2
        y = pos1.y
        
        flag = 0
        
        for x in range(pos1.x, pos2.x + 1):
            if steep:
                if self.map[y][x].type == DUNGEON_DOOR:
                    continue
                doorPlacement = self.map[y][x].checkDoorPlacement(self)
                self.map[y][x].blocked = False
                self.map[y][x].type = DUNGEON_FLOOR
                if flag < MAX_DOORS_PER_TUNNEL:
                    if doorPlacement == True:
                        self.map[y][x].type = DUNGEON_DOOR
                        self.map[y][x].blocked = True
                        flag += 1
            else:
                if self.map[x][y].type == DUNGEON_DOOR:
                    continue
                doorPlacement = self.map[x][y].checkDoorPlacement(self)
                self.map[x][y].blocked = False
                self.map[x][y].type = DUNGEON_FLOOR
                if flag < MAX_DOORS_PER_TUNNEL:
                    if doorPlacement == True:
                        self.map[x][y].type = DUNGEON_DOOR
                        self.map[x][y].blocked = True
                        flag += 1
            error = error + deltay
            if error > 0:
                y = y + ystep
                error = error - deltax

    def randTunnel(self, pos1, pos2):
        if random.randint(0,10) > 3:
            self.makeTwoLeggedTunnel(pos1,pos2)
        else:
            self.makeDiagTunnel(pos1,pos2)

    def makeRandRoom(self, rect):
        subFromW = random.randint(1,5)
        subFromH = random.randint(1,5)
        addToX = subFromW / 2
        subFromW = subFromW - addToX
        addToY = subFromH / 2
        subFromH = subFromH - addToY
        
        w = rect.w - subFromW
        h = rect.h - subFromH
        
        if  w > 3 and h > 3:
            newPos = Position(rect.pos.x+addToX, rect.pos.y+addToY)
            return self.makeRectRoom(Rect(newPos,w,h))
        else:
            return self.makeRectRoom(rect)

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

class MapCell:
    def __init__(self, pos, batch,
                 group, blocked=True, visible=True,
                 discovered=False):
        self.blocked = blocked
        self.visible = visible
        self.discovered = discovered
        self.batch = batch
        self.group = group
        self.pos = pos
        self.xPx = self.pos.x * SPRITE_SIZE
        self.yPx = self.pos.y * SPRITE_SIZE
        self.type = DUNGEON_WALL
        self.objects = []

    def checkDoorPlacement(self, gameMap):
        for r in gameMap.rooms:
            if r.checkPointIntersect(self.pos):
                return False

        iterPos = Position(self.pos.x,self.pos.y)
        results = []
        topResult = self.checkCell(gameMap, iterPos.moveUp())
        results.append(self.checkCell(gameMap, iterPos.moveRight()))
        rightResult = self.checkCell(gameMap, iterPos.moveDown())
        results.append(self.checkCell(gameMap, iterPos.moveDown()))
        bottomResult = self.checkCell(gameMap, iterPos.moveLeft())
        results.append(self.checkCell(gameMap, iterPos.moveLeft()))
        leftResult = self.checkCell(gameMap, iterPos.moveUp())
        results.append(self.checkCell(gameMap, iterPos.moveUp()))

        if topResult == DUNGEON_DOOR and bottomResult == DUNGEON_WALL:
            return True
        if bottomResult == DUNGEON_DOOR and topResult == DUNGEON_WALL:
            return True
        if leftResult == DUNGEON_DOOR and rightResult == DUNGEON_WALL:
            return True
        if rightResult == DUNGEON_DOOR and leftResult == DUNGEON_WALL:
            return True 

        if not topResult == DUNGEON_WALL and not bottomResult == DUNGEON_WALL:
            if not leftResult == DUNGEON_WALL and not rightResult == DUNGEON_WALL:
                return False
        
        results.append(topResult)
        results.append(bottomResult)
        results.append(leftResult)
        results.append(rightResult)
        
        found = [0,0,0,0] 
        for i in results:
            found[i] += 1

        if found[DUNGEON_FLOOR] > 1:
            if found[DUNGEON_WALL] > 2:
                return True
        return False

    def checkCell(self, gameMap, pos):
        try:
            cell = gameMap.getCellAtPos(pos)
        except IndexError:
            return OUT_OF_BOUNDS
        return cell.type

class BSP:
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
                

if __name__ == '__main__':
    import sys
    
    map = Map(width=60,height=79)
    for x in range(len(map.map)):
        for y in range(len(map.map[x])):
            if map.map[x][y].type == DUNGEON_WALL:
                sys.stdout.write('#')
            elif map.map[x][y].type == DUNGEON_FLOOR:
                sys.stdout.write(' ')
            elif map.map[x][y].type == DUNGEON_DOOR:
                sys.stdout.write('A')
        print '\n',

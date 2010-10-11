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
from BSP import BSP
from mapcell import MapCell
from rect import Rect
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
        
        self.initGameMap()        

        self.initBSP()

        self.drawTunnels()

    def initGameMap(self):
        for x in range(self.width):
            lst = []
            for y in range(self.height):
                lst.append(MapCell(Position(x, y), self.batch, self.mapGroup))
            self.map.append(lst)

    def initBSP(self):
        bsp = BSP(self.playableArea)
        self.rooms = []
        for r in bsp.rects:
            if random.randint(0,10) > 3:
                roomrect = self.makeRandRoom(r)
                self.rooms.append(roomrect)
                
    def drawTunnels(self):
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

    def getViewportPos(self,width,height):
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
        startPos = Position(startX,startY)
        endPos = Position(endX,endY)
        return (startPos,endPos)
        

    def updateViewport(self, width, height):
        startPos,endPos = self.getViewportPos(width,height)

        for x in xrange(startPos.x, endPos.x):
            for y in xrange(startPos.y, endPos.y):
                self.map[x][y].visible = False

        self.doFOV()

        xIter = 0

        for x in xrange(startPos.x, endPos.x):
            yIter = 0
            for y in xrange(startPos.y, endPos.y):
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

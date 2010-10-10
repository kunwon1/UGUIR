from pyglet.sprite import Sprite
import pyglet.graphics

import random
random.seed()

from constants import *
from spritesheet import sheet
from player import Player
from position import Position

class Map(object):
    def __init__(self, width=DEFAULT_MAP_CELLS_X, height=DEFAULT_MAP_CELLS_Y):
        self.map = []
        self.viewport = []
        self.playerX, self.playerY = 0, 0
        self.playerPos = Position()
        self.batch = pyglet.graphics.Batch()
        self.mapGroup = pyglet.graphics.OrderedGroup(0)
        self.playerGroup = pyglet.graphics.OrderedGroup(1)
        self.player = Player(x=0, y=0, batch=self.batch, group=self.playerGroup)
        
        for i in range(VIEWPORT_W):
            self.viewport.append([0]*VIEWPORT_H)
        self.initViewport()

        for x in range(width):
            lst = []
            for y in range(height):
                lst.append(MapCell(x*SPRITE_SIZE, y*SPRITE_SIZE, self.batch, self.mapGroup))
            self.map.append(lst)
        
        self.makeRectRoom(Rect(12, 12, 12, 12))
        self.makeRectRoom(Rect(50, 50, 16, 16))
        self.makeTwoLeggedTunnel(16, 16, 55, 55)
        self.movePlayer(15, 15)
        self.playerX, self.playerY = 60, 60
        
    def movePlayer(self, x, y):
        xPx, yPx = self.player.x, self.player.y
        newX, newY = self.playerX + x, self.playerY + y

        if self.map[newX][newY].blocked:
            return
        else:
            self.player.set_position(xPx + x*SPRITE_SIZE, yPx + y*SPRITE_SIZE)
            self.playerX = newX
            self.playerY = newY
    
    def initViewport(self):
        for x in range(len(self.viewport)):
            for y in range(len(self.viewport[x])):
                self.viewport[x][y] = Sprite(sheet['dungeon'][81], 
                                             x=x * SPRITE_SIZE, 
                                             y=y * SPRITE_SIZE, 
                                             batch = self.batch, 
                                             group = self.mapGroup)

    def updateViewport(self, width, height):
        startX = self.playerX - width / 2
        startY = self.playerY - height / 2
        endX = startX + width
        endY = startY + height
        
        if endX > (len(self.map) - 1):
            endX = len(self.map) - 1
        if endY > (len(self.map[endX])):
            endY = len(self.map[endX]) - 1
        if startX < 0:
            startX = 0
        if startY < 0:
            startY = 0

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
                yIter += 1
            xIter += 1

    def makeRectRoom(self, rect):
        for r in xrange(rect.x, rect.x+rect.w):
            for n in xrange(rect.y, rect.y+rect.h):
                self.map[r][n].blocked = False
                self.map[r][n].type = DUNGEON_FLOOR

    def makeHorizTunnel(self, y, x1, x2):
        for x in xrange(x1, x2 + 1):
            self.map[x][y].blocked = False
            self.map[x][y].type = DUNGEON_FLOOR

    def makeVertTunnel(self, x, y1, y2):
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

class Rect(object):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

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

class MapCell(object):
    def __init__(self, xCells, yCells, batch, group, blocked=True):
        self.blocked = blocked
        self.batch = batch
        self.group = group
        self.xCells = xCells
        self.yCells = yCells
        self.xPx = self.xCells * SPRITE_SIZE
        self.yPx = self.yCells * SPRITE_SIZE
        self.type = DUNGEON_WALL
        
def isNearEdge(x,y):
    lowPass = CLOSE_TO_EDGE
    highPassX = VIEWPORT_W * SPRITE_SIZE - CLOSE_TO_EDGE
    highPassY = VIEWPORT_H * SPRITE_SIZE - CLOSE_TO_EDGE
    if lowPass <= x <= highPassX:
        if lowPass <= y <= highPassY:
            return False
    return True

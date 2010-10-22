from pyglet.sprite import Sprite
import pyglet.graphics

from dice import Dice
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
    def __init__(self,
                 width=DEFAULT_MAP_CELLS_X,
                 height=DEFAULT_MAP_CELLS_Y ):
        self.map = []
        self.viewport = []
        self.width, self.height = width, height
        self.playableArea = Rect(Position(1,1),width-2,height-2)
        self.batch = pyglet.graphics.Batch()
        self.mapGroup = pyglet.graphics.OrderedGroup(0)
        self.monsterGroup = pyglet.graphics.OrderedGroup(1)
        self.playerGroup = pyglet.graphics.OrderedGroup(2)
        self.player = Player(map=self, pos=Position(),
                             batch=self.batch,
                             group=self.playerGroup)
        
        self.dice = Dice()
                
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
            if self.dice.roll('1d10') > 3:
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
                self.player.moveOrAttack(self,pos)
                self.map[pos.x+1][pos.y+1].objects.append(
                    Kobold(Position(pos.x+1,pos.y+1), self,
                           self.batch, self.monsterGroup)
                    )
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
    
    def initViewport(self):
        for i in range(VIEWPORT_W):
            self.viewport.append([0]*VIEWPORT_H)
        for x in range(len(self.viewport)):
            for y in range(len(self.viewport[x])):
                self.viewport[x][y] = Sprite(sheet['dungeon'][81], 
                                             x=x * SPRITE_SIZE, 
                                             y=y * SPRITE_SIZE, 
                                             batch = self.batch, 
                                             group = self.mapGroup)

    def getViewportPos(self,width,height):
        startX = self.player.pos.x - width / 2
        startY = self.player.pos.y - height / 2
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

        if self.objectUpdateRequired == 1:
            try:
                self.minimap.updatePointList()
            except AttributeError:
                pass
            self.doObjectUpdate(width,height)

        xIter = 0
        for x in xrange(startPos.x, endPos.x):
            yIter = 0
            for y in xrange(startPos.y, endPos.y):
                cell = self.map[x][y]
                vpSprite = self.viewport[xIter][yIter]
                
                self.setSpriteImg(cell,vpSprite)
                self.setSpriteOpacity(cell,vpSprite)

                objPixels = (xIter*32,yIter*32)
                self.displayVisibleObjects(cell,objPixels)

                if self.player.pos == Position(x,y):
                    playerXPx = vpSprite.x
                    playerYPx = vpSprite.y
                    self.player.set_position(playerXPx,playerYPx)

                yIter += 1
            xIter += 1

    def doFOV(self):
        fieldOfView(self.player.pos.x,self.player.pos.y,
                    self.width,self.height,15,
                    self.funcVisit,self.funcBlocked)

    def doObjectUpdate(self, width, height):
        self.objectUpdateRequired = 0
        startObjectProc,endObjectProc = \
            self.getViewportPos(width + width/2, height + height/2)

        self.getCellAtPos(self.player.pos).blockedByObject = True
        for x in xrange(startObjectProc.x, endObjectProc.x):
            for y in xrange(startObjectProc.y, endObjectProc.y):
                self.map[x][y].blockedByObject = False
                for o in self.map[x][y].objects:
                    o.updateState(self)

    def setSpriteImg(self,cell,vpSprite):
        if cell.type == DUNGEON_WALL:
            vpSprite.image = sheet['dungeon'][81]
        elif cell.type == DUNGEON_FLOOR:
            vpSprite.image = sheet['ground'][170]
        elif cell.type == DUNGEON_DOOR:
            vpSprite.image = sheet['dungeon'][84]
        elif cell.type == OPEN_DOOR:
            vpSprite.image = sheet['dungeon'][85]

    def setSpriteOpacity(self,cell,vpSprite):
        if cell.discovered == False:
            vpSprite.opacity = 0
        elif cell.visible == False:
            vpSprite.opacity = 128
        else:
            vpSprite.opacity = 255

    def displayVisibleObjects(self,cell,pixels):
        for obj in cell.objects:
            if cell.discovered == True and cell.visible == True:
                obj.set_position(pixels[0],pixels[1])
                obj.visible = True
            else:
                obj.visible = False
            if obj.blocked == True:
                cell.blockedByObject = True

    ##### These are used only by the FOV system ###############################

    def funcVisit(self,x,y):
        pos = Position(x,y)
        if pos.x < 0:
            pos.x = 0
        if pos.y < 0:
            pos.y = 0
        self.map[pos.x][pos.y].visible = True
        self.map[pos.x][pos.y].discovered = True

    def funcBlocked(self,x,y):
        return self.map[x][y].blockedByTerrain

    ###########################################################################

    def makeRectRoom(self, rect):
        for r in xrange(rect.pos.x, rect.pos.x+rect.w):
            for n in xrange(rect.pos.y, rect.pos.y+rect.h):
                self.map[r][n].blockedByTerrain = False
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
            self.map[x][pos.y].blockedByTerrain = False
            self.map[x][pos.y].type = DUNGEON_FLOOR
            if flag < MAX_DOORS_PER_TUNNEL:
                if doorPlacement == True:
                    self.map[x][pos.y].type = DUNGEON_DOOR
                    self.map[x][pos.y].blockedByTerrain = True
                    flag += 1

    def makeVertTunnel(self, pos, y2):
        if pos.y > y2:
            (pos.y,y2) = (y2,pos.y)
        flag = 0
        for y in xrange(pos.y, y2 + 1):
            if self.map[pos.x][y].type == DUNGEON_DOOR:
                    continue
            doorPlacement = self.map[pos.x][y].checkDoorPlacement(self)
            self.map[pos.x][y].blockedByTerrain = False
            self.map[pos.x][y].type = DUNGEON_FLOOR
            if flag < MAX_DOORS_PER_TUNNEL:
                if doorPlacement == True:
                    self.map[pos.x][y].type = DUNGEON_DOOR
                    self.map[pos.x][y].blockedByTerrain = True
                    flag += 1

    def makeTwoLeggedTunnel(self, pos1, pos2):
        if self.dice.roll('1d2') == 1:
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
                self.map[y][x].blockedByTerrain = False
                self.map[y][x].type = DUNGEON_FLOOR
                if flag < MAX_DOORS_PER_TUNNEL:
                    if doorPlacement == True:
                        self.map[y][x].type = DUNGEON_DOOR
                        self.map[y][x].blockedByTerrain = True
                        flag += 1
            else:
                if self.map[x][y].type == DUNGEON_DOOR:
                    continue
                doorPlacement = self.map[x][y].checkDoorPlacement(self)
                self.map[x][y].blockedByTerrain = False
                self.map[x][y].type = DUNGEON_FLOOR
                if flag < MAX_DOORS_PER_TUNNEL:
                    if doorPlacement == True:
                        self.map[x][y].type = DUNGEON_DOOR
                        self.map[x][y].blockedByTerrain = True
                        flag += 1
            error = error + deltay
            if error > 0:
                y = y + ystep
                error = error - deltax

    def randTunnel(self, pos1, pos2):
        if self.dice.roll('1d10') > 3:
            self.makeTwoLeggedTunnel(pos1,pos2)
        else:
            self.makeDiagTunnel(pos1,pos2)

    def makeRandRoom(self, rect):
        subFromW = self.dice.roll('1d5')
        subFromH = self.dice.roll('1d5')
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

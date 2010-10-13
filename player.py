from pyglet.sprite import Sprite
import pyglet.gl

from spritesheet import sheet
from position import Position
from constants import *
from fighterstats import Stats
from msgbox import msgBox

class Player(Sprite):
    def __init__(self,
                 x=0, y=0, map=None,
                 blend_src=pyglet.gl.GL_SRC_ALPHA,
                 blend_dest=pyglet.gl.GL_ONE_MINUS_SRC_ALPHA,
                 pos=None,
                 batch=None,
                 group=None,
                 usage='dynamic',
                 ):
        self.dead = False
        self.name = 'Player'
        self.map = map
        self.mbox = msgBox()
        img = sheet['class'][79]
        self.stats = Stats(self, Con=18, hpRoll=20)
        if pos is None:
            self.pos = Position()
        else:
            self.pos = pos
        Sprite.__init__(self, img,
                        x, y, blend_src,
                        blend_dest, batch,
                        group, usage)

    def moveOrAttack(self, map, incPos):
        xPx, yPx = self.x, self.y
        newPos = Position(self.pos.x + incPos.x, self.pos.y + incPos.y)
        newCell = map.getCellAtPos(newPos)
        if newCell.blockedByTerrain:
            if newCell.type == DUNGEON_DOOR:
                newCell.type = OPEN_DOOR
                newCell.blockedByTerrain = False
                self.map.objectUpdateRequired = 1
        elif newCell.blockedByObject:
            if len(newCell.objects) == 1:
                self.stats.attackOther(newCell.objects[0])
            else:
                raise ValueError('cell should not have two objects!')
        else:
            map.getCellAtPos(self.pos).blockedByObject = False
            self.set_position(xPx + incPos.x * SPRITE_SIZE,
                              yPx + incPos.y * SPRITE_SIZE)
            self.pos = newPos
            map.objectUpdateRequired = 1
        
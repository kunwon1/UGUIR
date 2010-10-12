from pyglet.sprite import Sprite
import pyglet.gl

from spritesheet import sheet
from position import Position
from constants import *

class Player(Sprite):
    def __init__(self,
                 x=0, y=0,
                 blend_src=pyglet.gl.GL_SRC_ALPHA,
                 blend_dest=pyglet.gl.GL_ONE_MINUS_SRC_ALPHA,
                 pos=None,
                 batch=None,
                 group=None,
                 usage='dynamic',
                 ):
        img = sheet['class'][79]
        if pos is None:
            self.pos = Position()
        else:
            self.pos = pos
        Sprite.__init__(self, img, x, y, blend_src, blend_dest, batch, group, usage)

    def moveOrAttack(self, map, incPos):
        xPx, yPx = self.x, self.y
        newPos = Position(self.pos.x + incPos.x, self.pos.y + incPos.y)
        newCell = map.getCellAtPos(newPos)
        if newCell.blockedByTerrain or newCell.blockedByObject:
            if newCell.type == DUNGEON_DOOR:
                newCell.type = OPEN_DOOR
                newCell.blockedByTerrain = False
            return
        else:
            map.getCellAtPos(self.pos).blockedByObject = False
            self.set_position(xPx + incPos.x * SPRITE_SIZE, yPx + incPos.y * SPRITE_SIZE)
            self.pos = newPos
            map.objectUpdateRequired = 1
        
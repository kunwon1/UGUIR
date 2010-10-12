from pyglet.sprite import Sprite
import pyglet.gl
from random import randint

from spritesheet import sheet
from fighterstats import Stats
from position import Position
from pathfinder import findPath

class Monster(Sprite):
    def __init__(self, img,
             pos=None,
             stats=Stats(),
             x=0, y=0,
             blend_src=pyglet.gl.GL_SRC_ALPHA,
             blend_dest=pyglet.gl.GL_ONE_MINUS_SRC_ALPHA,
             batch=None,
             group=None,
             usage='dynamic'):
        self.pos = pos
        self.stats = stats
        self.blocked = True
        self.oldPos = pos
        self.playerOldPos = None
        self.currentPath = []
        Sprite.__init__(self, img, x, y, blend_src, blend_dest, batch, group, usage)

    def updateState(self, map):
        mapPos = map.getCellAtPos(self.pos)
        if mapPos.visible:
            self.currentPath = []
            pFinder = findPath(map,self.pos,map.player.pos)
            pIter = pFinder.iter
            pIter.next()
            for p in pIter:
                self.currentPath.append(p)
            self.playerOldPos = map.player.pos
        try:
            next = self.currentPath.pop(0)
        except IndexError:
            return
        self.moveOrAttack(map, mapPos, next)

    def moveOrAttack(self, map, curPos, nextPos):
        if nextPos == map.player.pos:
            return
        else:               
            curPos.objects.remove(self)
            map.getCellAtPos(nextPos).objects.append(self)
            lastMapPos = map.getCellAtPos(self.oldPos)
            self.oldPos = self.pos
            self.pos = nextPos

class Kobold(Monster):
    def __init__(self, pos, batch, group,
                 x=0, y=0):

        Str = randint(7,10)
        Dex = randint(12,16)
        Con = randint(8,10)
        Int = randint(7,13)
        Wis = randint(6,10)
        Cha = randint(4,8)
        hpr = randint(1,10)

        stats = Stats(hpRoll=hpr,
                      Str=Str,Dex=Dex,
                      Con=Con,Int=Int,
                      Wis=Wis,Cha=Cha)
        img = sheet['monster1'][90]
        Monster.__init__(self, img, pos=pos,
                         stats=stats, x=x, y=y,
                         batch=batch, group=group)

from pyglet.sprite import Sprite
import pyglet.gl
from random import randint

from spritesheet import sheet
from fighterstats import Stats

class Monster(Sprite):
    def __init__(self, img,
             stats=Stats(),
             x=0, y=0,
             blend_src=pyglet.gl.GL_SRC_ALPHA,
             blend_dest=pyglet.gl.GL_ONE_MINUS_SRC_ALPHA,
             batch=None,
             group=None,
             usage='dynamic'):
        self.stats = stats
        self.blocked = True
        Sprite.__init__(self, img, x, y, blend_src, blend_dest, batch, group, usage)

class Kobold(Monster):
    def __init__(self, x=0, y=0,
                 batch=None,
                 group=None):
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
        Monster.__init__(self, img, stats,
                         x=x, y=y, batch=batch,
                         group=group)

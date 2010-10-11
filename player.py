from pyglet.sprite import Sprite
import pyglet.gl

from spritesheet import sheet
from position import Position

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

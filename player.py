from pyglet.sprite import Sprite
import pyglet.gl

from spritesheet import sheet

class Player(Sprite):
    def __init__(self,
             x=0, y=0,
             blend_src=pyglet.gl.GL_SRC_ALPHA,
             blend_dest=pyglet.gl.GL_ONE_MINUS_SRC_ALPHA,
             batch=None,
             group=None,
             usage='dynamic'):
        img = sheet['class'][79]
        Sprite.__init__(self, img, x, y, blend_src, blend_dest, batch, group, usage)
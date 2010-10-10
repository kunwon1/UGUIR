import pyglet
from pyglet.window.key import MOTION_UP, MOTION_DOWN, MOTION_LEFT, MOTION_RIGHT
from pyglet.sprite import Sprite

pyglet.resource.path = ['res', 'res/images',]
pyglet.resource.reindex()

from spritesheet import *

# map is a built-in function map(func, sequence) -> [func(seq0), func(seq1) ..]
from map import *
from constants import *
from msgbox import msgBox

mbox = msgBox()
map = Map(width=500, height=500)
map.updateViewport(VIEWPORT_W,VIEWPORT_H)
window = pyglet.window.Window(width=WINDOW_W, height=WINDOW_H)

outline = pyglet.resource.image('outline.png')
outline = pyglet.sprite.Sprite(outline)
outline.set_position(OUTLINE_X, OUTLINE_Y)

@window.event
def on_text_motion(motion):
    if motion == MOTION_UP:
        map.movePlayer(0,1)
    elif motion == MOTION_RIGHT:
        map.movePlayer(1,0)
    elif motion == MOTION_DOWN:
        map.movePlayer(0,-1)
    elif motion == MOTION_LEFT:
        map.movePlayer(-1,0)
    else:
        pass

@window.event
def on_draw():
    window.clear()
    outline.draw()
    if isNearEdge(map.player.x, map.player.y):
        map.updateViewport(VIEWPORT_W,VIEWPORT_H)
    mbox.draw()
    map.batch.draw()
    map.player.draw()

pyglet.app.run()

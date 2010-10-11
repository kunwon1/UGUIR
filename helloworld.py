import pyglet
from pyglet.window.key import *

pyglet.resource.path = ['res', 'res/images',]
pyglet.resource.reindex()

from spritesheet import *

# map is a built-in function map(func, sequence) -> [func(seq0), func(seq1) ..]
from map import *
from constants import *
from msgbox import msgBox

mbox = msgBox()
map = Map(width=60, height=70)
map.updateViewport(VIEWPORT_W,VIEWPORT_H)
window = pyglet.window.Window(width=WINDOW_W, height=WINDOW_H)

outline = pyglet.resource.image('outline.png')
outline = pyglet.sprite.Sprite(outline)
outline.set_position(OUTLINE_X, OUTLINE_Y)

@window.event
def on_text_motion(motion):
    if motion == MOTION_UP:
        map.movePlayer(UP)
    elif motion == MOTION_RIGHT:
        map.movePlayer(RIGHT)
    elif motion == MOTION_DOWN:
        map.movePlayer(DOWN)
    elif motion == MOTION_LEFT:
        map.movePlayer(LEFT)
    else:
        pass

@window.event
def on_key_press(symbol, modifiers):
    if symbol == NUM_1:
        map.movePlayer(DOWN_LEFT)
    elif symbol == NUM_7:
        map.movePlayer(UP_LEFT)
    elif symbol == NUM_9:
        map.movePlayer(UP_RIGHT)
    elif symbol == NUM_3:
        map.movePlayer(DOWN_RIGHT)

    elif symbol == NUM_8:
        map.movePlayer(UP)
    elif symbol == NUM_6:
        map.movePlayer(RIGHT)
    elif symbol == NUM_2:
        map.movePlayer(DOWN)
    elif symbol == NUM_4:
        map.movePlayer(LEFT)
    else:
        pass

@window.event
def on_draw():
    window.clear()
    outline.draw()
    map.updateViewport(VIEWPORT_W,VIEWPORT_H)
    mbox.draw()
    map.batch.draw()
    map.player.draw()

pyglet.app.run()

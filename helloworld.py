import pyglet
from pyglet.window.key import *

from spritesheet import *
from gamemap import *
from constants import *
from msgbox import msgBox
from minimap import miniMap

mbox = msgBox()
map = Map(width=60, height=70)
map.updateViewport(VIEWPORT_W,VIEWPORT_H)
    
minimap = miniMap(map=map, pos=MINIMAP_POS)
window = pyglet.window.Window(width=WINDOW_W, height=WINDOW_H)

outline = pyglet.resource.image('outline.png')
outline = pyglet.sprite.Sprite(outline)
outline.set_position(OUTLINE_X, OUTLINE_Y)

@window.event
def on_text_motion(motion):
    if map.player.dead:
        return
    if motion == MOTION_UP:
        map.player.moveOrAttack(map, UP)
    elif motion == MOTION_RIGHT:
        map.player.moveOrAttack(map, RIGHT)
    elif motion == MOTION_DOWN:
        map.player.moveOrAttack(map, DOWN)
    elif motion == MOTION_LEFT:
        map.player.moveOrAttack(map, LEFT)
    else:
        return

@window.event
def on_key_press(symbol, modifiers):
    if map.player.dead:
        return
    if symbol == NUM_1:
        map.player.moveOrAttack(map, DOWN_LEFT)
    elif symbol == NUM_7:
        map.player.moveOrAttack(map, UP_LEFT)
    elif symbol == NUM_9:
        map.player.moveOrAttack(map, UP_RIGHT)
    elif symbol == NUM_3:
        map.player.moveOrAttack(map, DOWN_RIGHT)
    elif symbol == NUM_8:
        map.player.moveOrAttack(map, UP)
    elif symbol == NUM_6:
        map.player.moveOrAttack(map, RIGHT)
    elif symbol == NUM_2:
        map.player.moveOrAttack(map, DOWN)
    elif symbol == NUM_4:
        map.player.moveOrAttack(map, LEFT)
    else:
        return

@window.event
def on_draw():
    window.clear()
    outline.draw()
    map.updateViewport(VIEWPORT_W,VIEWPORT_H)
    mbox.draw()
    map.batch.draw()
    map.player.draw()
    map.player.statuswindow.draw()
    minimap.draw()
pyglet.app.run()

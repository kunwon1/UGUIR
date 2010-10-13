import pyglet
from map import Map
from constants import *
from position import Position

class miniMap:
    def __init__(self, map, pos, w, h):
        self.map = map
        self.xOff = pos.x + 10
        self.yOff = pos.y + 10
        
    def draw(self):
        xIter = 0
        for x in range(len(self.map.map)):
            yIter = 0
            for y in range(len(self.map.map[x])):
                startX = self.xOff + xIter * 2
                startY = self.yOff + yIter * 2
                if self.map.map[x][y].type == DUNGEON_FLOOR:
                    if self.map.map[x][y].discovered == True:
                        pyglet.graphics.draw(2, pyglet.gl.GL_POINTS,
                            ('v2i', (startX, startY, startX + 1, startY + 1))
                        )
                yIter += 1
            xIter += 1

if __name__ == '__main__':

    window = pyglet.window.Window(width=WINDOW_W, height=WINDOW_H)

    map = Map(width=60,height=79)
    miniMapPos = Position(MINIMAP_X,MINIMAP_Y)
    
    mm = miniMap(map=map, pos=miniMapPos, w=MINIMAP_W, h=MINIMAP_H)
    
    @window.event
    def on_draw():
        window.clear()
        mm.draw()
    pyglet.app.run()
    
import pyglet
from constants import *

class miniMap:
    def __init__(self, map, pos):
        self.map = map
        self.map.minimap = self
        self.xOff = pos.x + ( (MINIMAP_W - len(self.map.map) * 2) / 2 )
        self.yOff = pos.y + 10
        self.pointList = []
        
    def draw(self):
        
        if len(self.pointList) < 1:
            self.updatePointList()
            
        pyglet.graphics.draw(self.pointListLength, pyglet.gl.GL_POINTS,
                            ('v2i', self.pointList)
                        )
        
    def updatePointList(self):
        self.pointList = []
        
        xIter = 0
        for x in range(len(self.map.map)):
            yIter = 0
            for y in range(len(self.map.map[x])):
                X = self.xOff + xIter * 2
                Y = self.yOff + yIter * 2
                cell = self.map.map[x][y]
                if cell.type == DUNGEON_FLOOR \
                or cell.type == DUNGEON_DOOR \
                or cell.type == OPEN_DOOR:
                    if cell.discovered == True:
                        self.pointList.extend([X,Y,X+1,Y,X,Y+1,X+1,Y+1])
                yIter += 1
            xIter += 1
        
        self.pointListLength = len(self.pointList) / 2
        
if __name__ == '__main__':

    #doesn't work, because no map tiles are discovered by default
    
    #code above can be changed for this to work

    from map import Map
    from position import Position

    window = pyglet.window.Window(width=WINDOW_W, height=WINDOW_H)

    map = Map(width=60,height=79)
    miniMapPos = Position(MINIMAP_X,MINIMAP_Y)
    
    mm = miniMap(map=map, pos=miniMapPos)
    
    @window.event
    def on_draw():
        window.clear()
        mm.draw()
    pyglet.app.run()
    
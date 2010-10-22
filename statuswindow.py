import pyglet
from constants import *
from position import Position

class statusWindow(object):
    def __init__(self, playerObj, batch, group):
        self.parent = playerObj
        self.batch = batch
        self.group = group
        
        self.xpPercentage = 0
        self.hpPercentage = 1
        self.mpPercentage = 1
        
        posInc = STATUSWINDOW_POS.copy()
        yInc = Position(0,STATUSWIN_MODULE_H + 1)
        
        posInc += yInc

        self.xpEntry = statusWindowProgressBarEntry(
                        self.xpPercentage,
                        posInc.copy(),
                        (255,255,0))
        posInc += yInc
        self.mpEntry = statusWindowProgressBarEntry(
                        self.mpPercentage,
                        posInc.copy(),
                        (0,0,255))
        
        posInc += yInc
        
        self.hpEntry = statusWindowProgressBarEntry(
                        self.hpPercentage,
                        posInc.copy(),
                        (255,0,0))
        
        posInc += yInc
        
        self.nameEntry = statusWindowTextEntry(
                        self.parent.charName + ' the ' + self.parent.charClass,
                        posInc.copy(),
                        self.batch, self.group)

        self.draw()
        
    def updateStats(self):
        self.hpPercentage = \
        float(self.parent.stats.hp) / float(self.parent.stats.maxHP)
        self.hpEntry.updateValue(self.hpPercentage)

        self.mpPercentage = \
        float(self.parent.stats.mp) / float(self.parent.stats.maxMP)
        self.mpEntry.updateValue(self.mpPercentage)
        
        self.xpPercentage = \
        float(self.parent.stats.xp) / float(self.parent.stats.xpForNextLevel)
        self.xpEntry.updateValue(self.xpPercentage)
        
    def draw(self):
        self.updateStats()
        self.hpEntry.draw()
        self.mpEntry.draw()
        self.xpEntry.draw()

class statusWindowProgressBarEntry(object):
    def __init__(self, value, pos, color):
        self.value = value
        self.pos = pos
        self.color = color
        self.updateValue(value)
        
    def updateValue(self, value):
        startX,endX = self.pos.x + 10, \
                        self.pos.x + STATUSWINDOW_W - 10
        startY,endY = self.pos.y + 4, \
                        self.pos.y + STATUSWIN_MODULE_H - 4
        barTotal = endX - startX
        endX = int(value * barTotal) + startX
        self.lineLoopList = [
            self.pos.x + 1,
            self.pos.y + 1,
            self.pos.x + STATUSWINDOW_W - 1,
            self.pos.y + 1,
            self.pos.x + STATUSWINDOW_W - 1,
            self.pos.y + STATUSWIN_MODULE_H - 1,
            self.pos.x + 1,
            self.pos.y + STATUSWIN_MODULE_H - 1,
            self.pos.x + 1,
            self.pos.y + 1
            ]
        self.lineLoopListLength = len(self.lineLoopList) / 2
        self.pointList = [startX,startY,startX,endY,endX,endY,endX,startY]
        self.pointListLength = len(self.pointList) / 2

    def draw(self):
        pyglet.gl.glColor3f(*self.color)
        pyglet.graphics.draw(self.pointListLength, pyglet.gl.GL_QUADS,
                    ('v2i', self.pointList)
                )
        pyglet.graphics.draw(self.lineLoopListLength, pyglet.gl.GL_LINE_LOOP,
                    ('v2i', self.lineLoopList)
                )
        pyglet.gl.glColor3f(*WHITE)

class statusWindowTextEntry(object):
    def __init__(self, text, pos, batch, group):
        self.doc = pyglet.text.decode_text(text)
        
        self.style = dict(font_name='NotCourierSans',
                          font_size=10, bold=True,
                          color=(255,255,255,255))
        
        l = len(self.doc.text)
        self.doc.set_style(0, l, self.style)
        
        self.layout = pyglet.text.layout.TextLayout(self.doc,
                                                    MSGBOX_W,
                                                    STATUSWIN_MODULE_H,
                                                    batch=batch)
        self.layout.x,self.layout.y = pos.x + 10,pos.y + 2

    def updateText(self, text):
        self.layout.begin_update()
        self.doc = pyglet.text.decode_text(text)
        l = len(self.doc.text)
        self.doc.set_style(0, l, self.style)
        self.layout.end_update()

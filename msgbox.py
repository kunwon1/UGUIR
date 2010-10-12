import pyglet.text
from constants import *

class msgBox(object):
    def __init__(self):
        self.doc = pyglet.text.decode_text('Hello, World. Welcome to my game.')
        l = len(self.doc.text)
        self.doc.set_style(0, l, DEFAULT_MSGSTYLE)
        self.layout = pyglet.text.layout.TextLayout(self.doc, MSGBOX_W, MSGBOX_H, multiline=True)
        self.layout.x = MSGBOX_X
        self.layout.y = MSGBOX_Y

    def addMsg(self, s):
        s = s + '\n'
        self.layout.begin_update()
        if self.doc.text.count('\n') > MSGBOX_LINES:
            count = self.doc.text.index('\n')
            self.doc.delete_text(0, count + 1)
        l = len(self.doc.text)
        ls = len(s)
        self.doc.insert_text(l,s)
        self.doc.set_style(0, l+ls, DEFAULT_MSGSTYLE)
        self.layout.end_update()

    def draw(self):
        self.layout.draw()
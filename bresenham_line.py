# Copyright (c) 2010 the authors listed at the following URL, and/or
# the authors of referenced articles or incorporated external code:
# http://en.literateprograms.org/Bresenham's_line_algorithm_(Python)?action=history&offset=20090320052336
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# 
# Retrieved from: http://en.literateprograms.org/Bresenham's_line_algorithm_(Python)?oldid=16281

from Tkinter import *

class BresenhamCanvas(Canvas):

    def draw_point(self, x, y, color="red"):
        self.create_line(x, y, x, y, fill=color)


    def draw_line(self, x0, y0, x1, y1, color="red"):
        steep = abs(y1 - y0) > abs(x1 - x0)
        if steep:
            x0, y0 = y0, x0  
            x1, y1 = y1, x1


        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        
        if y0 < y1: 
            ystep = 1
        else:
            ystep = -1

            
        deltax = x1 - x0
        deltay = abs(y1 - y0)
        error = -deltax / 2
        y = y0

            
        for x in range(x0, x1 + 1): # We add 1 to x1 so that the range includes x1
	    if steep:
	        self.draw_point(y, x, color)
	    else:
	        self.draw_point(x, y, color)
	            
	    error = error + deltay
	    if error > 0:
	        y = y + ystep
	        error = error - deltax


                
if __name__ == "__main__":

    import math
    CANVAS_SIZE = 600

    root = Tk()
    canvas = BresenhamCanvas(root, width=CANVAS_SIZE, height=CANVAS_SIZE)
    canvas.pack()
    
    margin = CANVAS_SIZE / 10
    
    xcenter = int(CANVAS_SIZE / 2)
    ycenter = int(CANVAS_SIZE / 2)
    line_length = ((CANVAS_SIZE / 2) - margin)
    
    n_lines = 100
    angle_step = (2 * math.pi) / n_lines
    
    for i in range(n_lines):
        theta = angle_step * i
        xstart = int(margin * math.cos(theta)) + xcenter
        ystart = int(margin * math.sin(theta)) + ycenter
        xend = int(line_length * math.cos(theta)) + xcenter
        yend = int(line_length * math.sin(theta)) + ycenter
        canvas.draw_line(xstart, ystart, xend, yend, color="blue")
        
    root.mainloop()



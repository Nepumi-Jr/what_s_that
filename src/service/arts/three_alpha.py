from src.service.art_canvas import Canvas, extractType3
from math import sqrt, sin, cos, pi

n_type = 26 * 26 * 26

#* keep in mind that top left is (0, 0) and bottom right is (63, 47)
def get(type : int) -> Canvas:
    alpha1, alpha2, alpha3 = extractType3(type, 26, 26, 26)

    c = Canvas()

    def drawAlphabet(x, y, alpha):
        #* 20 x 40
        left, right, top, bottom = x, x + 19, y, y + 39
        cx, cy = (left + right) // 2, (top + bottom) // 2
        if alpha == 0: # A
            c.line(left,bottom,cx,top)
            c.line(right,bottom,cx,top)
            c.line(left+5,cy,right-5,cy)
        elif alpha == 1: # B
            c.line(left,top,left,bottom)
            c.line(left,top,right,int(bottom * 0.25))
            c.line(left,cy,right,int(bottom *  0.25))
            c.line(left,cy,right,int(bottom * 0.75))
            c.line(left,bottom,right,int(bottom *  0.75))
        elif alpha == 2: # C
            c.line(right,top,left,cy)
            c.line(right,bottom,left,cy)
        elif alpha == 3: # D
            c.line(left,top,left,bottom)
            c.line(left,top,right,cy)
            c.line(left,bottom,right,cy)
        elif alpha == 4: # E
            c.line(left,top,right,top)
            c.line(left,cy,cx,cy)
            c.line(left,bottom,right,bottom)
            c.line(left,top,left,bottom)
        elif alpha == 5: # F
            c.line(left,top,right,top)
            c.line(left,cy,cx,cy)
            c.line(left,top,left,bottom)
        elif alpha == 6: # G
            c.line(right,top,left,top)
            c.line(left,top,left,bottom)
            c.line(left,bottom,right,bottom)
            c.line(right,bottom,cx,cy)
        elif alpha == 7: #H
            c.line(left,top,left,bottom)
            c.line(right,top,right,bottom)
            c.line(left,cy,right,cy)
        elif alpha == 8: # I
            c.line(cx,top,cx,bottom)
        elif alpha == 9: # J
            c.line(cx,top,cx,bottom)
            c.line(cx,bottom,left,cy)
        elif alpha == 10: # K
            c.line(left,top,left,bottom)
            c.line(left,cy,right,top)
            c.line(left,cy,right,bottom)
        elif alpha == 11: # L
            c.line(left,top,left,bottom)
            c.line(left,bottom,right,bottom)
        elif alpha == 12: # M
            c.line(left,bottom,right//4,top)
            c.line(cx,cy,right//4, top)
            c.line(cx,cy, right//4 * 3, top)
            c.line(right,bottom,right//4 * 3,top)
        elif alpha == 13: # N
            c.line(left,top,left,bottom)
            c.line(left,top,right,bottom)
            c.line(right,top,right,bottom)
        elif alpha == 14: # O
            c.line(cx, top, left, cy)
            c.line(left, cy, cx, bottom)
            c.line(cx, bottom, right, cy)
            c.line(right, cy, cx, top)
        elif alpha == 15: # P
            c.line(left,top,left,bottom)
            c.line(left,top,right,cy//2)
            c.line(left,cy,right,cy//2)
        elif alpha == 16: # Q
            c.line(cx, top, left, cy)
            c.line(left, cy, cx, bottom)
            c.line(cx, bottom, right, cy)
            c.line(right, cy, cx, top)
            c.line(cx, cy, right, bottom)
        elif alpha == 17: # R
            c.line(left,top,left,bottom)
            c.line(left,top,right,cy//2)
            c.line(left,cy,right,cy//2)
            c.line(left,cy,right,bottom)
        elif alpha == 18: # S
            c.line(right,top,left,cy)
            c.line(left,cy,right,cy)
            c.line(right,cy,left,bottom)
        elif alpha == 19: # T
            c.line(cx,top,cx,bottom)
            c.line(left,top,right,top)
        elif alpha == 20: # U
            c.line(left,top,left,bottom)
            c.line(left,bottom,right,bottom)
            c.line(right,bottom,right,top)
        elif alpha == 21: # V
            c.line(left,top,cx,bottom)
            c.line(right,top,cx,bottom)
        elif alpha == 22: # W
            c.line(left,top,right//4,bottom)
            c.line(cx,cy,right//4, bottom)
            c.line(cx,cy, right//4 * 3, bottom)
            c.line(right,top,right//4 * 3,bottom)
        elif alpha == 23: # X
            c.line(left,top,right,bottom)
            c.line(left,bottom,right,top)
        elif alpha == 24: # Y
            c.line(left,top,cx,cy)
            c.line(right,top,cx,cy)
            c.line(cx,cy,cx,bottom)
        elif alpha == 25: # Z
            c.line(left,top,right,top)
            c.line(right,top,left,bottom)
            c.line(left,bottom,right,bottom)
    
    drawAlphabet(0, 0, alpha1)
    drawAlphabet(21, 0, alpha2)
    drawAlphabet(42, 0, alpha3)

    
    return c


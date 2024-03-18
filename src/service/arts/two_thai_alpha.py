from src.service.art_canvas import Canvas, extractType2
from math import sqrt, sin, cos, pi

n_type = 44 * 44

#* keep in mind that top left is (0, 0) and bottom right is (63, 47)
def get(type : int) -> Canvas:
    alpha1, alpha2 = extractType2(type, 44, 44)

    c = Canvas()

    def drawAlphabet(x, y, alpha):
        #* 20 x 40
        left, right, top, bottom = x, x + 19, y, y + 39
        cx, cy = (left + right) // 2, (top + bottom) // 2
        x14 = left + (right - left) // 4
        x34 = left + 3 * (right - left) // 4
        x18 = left + (right - left) // 8
        x38 = left + 3 * (right - left) // 8
        x58 = left + 5 * (right - left) // 8
        if alpha == 0: # ก
            c.line(left, bottom, left, cy)
            c.line(left, cy, x14, cy//2)
            c.line(x14, cy//2, left, cy//2)
            c.line(left, cy//2, cx, top)
            c.line(cx, top, right, cy//2)
            c.line(right, cy//2, right, bottom)
        elif alpha == 1: # ข
            c.line(left, cy//2, x14, cy//2)
            c.line(x14, cy//2, x14, bottom)
            c.line(x14, bottom, x34, bottom)
            c.line(x34, bottom, x34, cy//2)
        elif alpha == 2: # ค
            c.line(x34, cy, cx, cy)
            c.line(cx, cy, left, bottom)
            c.line(left, bottom, left, top)
            c.line(left, top, right, top)
            c.line(right, top, right, bottom)
        elif alpha == 3: # ง
            c.line(cx, top, x34, top)
            c.line(x34, top, x34, bottom)
            c.line(x34, bottom, left, cy)
        elif alpha == 4: # จ
            c.line(x14, cy, cx, cy)
            c.line(cx, cy, right, bottom)
            c.line(right, bottom, right, top)
            c.line(right, top, left, top)
        elif alpha == 5: # ช
            c.line(left, cy//2, x14, cy//2)
            c.line(x14, cy//2, x14, bottom)
            c.line(x14, bottom, x34, bottom)
            c.line(x34, bottom, x34, cy)
            c.line(x34, cy, cx, cy//4 * 3)
            c.line(cx, cy//4 * 3, right, cy//2)
        elif alpha == 6: # ญ
            c.line(left, cy//2 *3, left, top)
            c.line(left, top, x34, top)
            c.line(x34, top, x34, cy//2 * 3)
            c.line(x34, cy//2 * 3, right, cy // 2*3)
            c.line(right, cy//2 * 3, right, top)

            
    drawAlphabet(5, 0, alpha1)
    drawAlphabet(35, 0, alpha2)

    
    return c


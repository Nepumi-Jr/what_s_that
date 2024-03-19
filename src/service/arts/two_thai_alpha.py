from src.service.art_canvas import Canvas, extractType2
from math import sqrt, sin, cos, pi

n_type = 17 * 17

#* keep in mind that top left is (0, 0) and bottom right is (63, 47)
def get(type : int) -> Canvas:
    alpha1, alpha2 = extractType2(type, 17, 17)

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
            c.line(left, cy//2, x38, cy//2)
            c.line(x38, cy//2, x38, bottom)
            c.line(x38, bottom, x58, bottom)
            c.line(x58, bottom, x58, cy//2)
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
            c.line(x34, bottom, right, bottom)
        elif alpha == 7: # ด
            c.line(x14, cy, cx, cy)
            c.line(cx, cy, left, bottom)
            c.line(left, bottom, left, top)
            c.line(left, top, right, top)
            c.line(right, top, right, bottom)
        elif alpha == 8: # ฅ
            c.line(x34, cy, cx, cy)
            c.line(cx, cy, left, bottom)
            c.line(left, bottom, left, top)
            c.line(left, top, cx, cy//2)
            c.line(right, top, cx, cy//2)
            c.line(right, top, right, bottom)
        elif alpha == 9: # ต
            c.line(x14, cy, cx, cy)
            c.line(cx, cy, left, bottom)
            c.line(left, bottom, left, top)
            c.line(left, top, cx, cy//2)
            c.line(right, top, cx, cy//2)
            c.line(right, top, right, bottom)
        elif alpha == 10: # ถ
            c.line(left, bottom, x14, bottom)
            c.line(left, bottom, left, cy)
            c.line(left, cy, x14, cy//2)
            c.line(x14, cy//2, left, cy//2)
            c.line(left, cy//2, cx, top)
            c.line(cx, top, right, cy//2)
            c.line(right, cy//2, right, bottom)
        elif alpha == 11: # ท
            c.line(left, cy//2, x14, cy//2)
            c.line(x14, cy//2, x14, bottom)
            c.line(x14, cy, cx, cy//2)
            c.line(cx, cy//2, x34, cy)
            c.line(x34, cy, x34, bottom)
        elif alpha == 12: # ธ
            c.line(left, cy//2, left, bottom)
            c.line(left, bottom, right, bottom)
            c.line(right, bottom, right, cy)
            c.line(right, cy, left, top)
            c.line(left, top, right, top)
        elif alpha == 13: # บ
            c.line(left, cy//2, x14, cy//2)
            c.line(x14, cy//2, x14, bottom)
            c.line(x14, bottom, x34, bottom)
            c.line(x34, bottom, x34, cy//2)
        elif alpha == 14: # พ
            c.line(left, cy//2, x14, cy//2)
            c.line(x14, cy//2, x14, bottom)
            c.line(x14, bottom, cx, cy//2)
            c.line(cx, cy//2, x34, bottom)
            c.line(x34, bottom, x34, cy//2)
        elif alpha == 15: # ผ
            c.line(cx, cy//2, x14, cy//2)
            c.line(x14, cy//2, x14, bottom)
            c.line(x14, bottom, cx, cy)
            c.line(cx, cy, x34, bottom)
            c.line(x34, bottom, x34, cy//2)
        elif alpha == 16: # อ
            c.line(cx, cy, x14, cy)
            c.line(x14, cy, x14, bottom)
            c.line(x14, bottom, x34, bottom)
            c.line(x34, bottom, x34, top)
            c.line(x34, top, x14, top)

            
    drawAlphabet(5, 0, alpha1)
    drawAlphabet(35, 0, alpha2)

    
    return c


from src.service.art_canvas import Canvas, extractType4
from math import sqrt, sin, cos, pi

n_type = 3 * 3 * 4 * 2

#* keep in mind that top left is (0, 0) and bottom right is (63, 47)
def get(type : int) -> Canvas:
    middleShape, outerShape, n_flower, isRotate = extractType4(type, 3, 3, 4, 2)

    c = Canvas()

    # body of flower
    c.rect(c.centerX-1, c.centerY, c.centerX, c.bottom, 1)

    # middle shape of flower
    if middleShape == 0:
        c.circle(c.centerX-1, c.centerY, 3)
    elif middleShape == 1:
        c.rect(c.centerX-3, c.centerY-3, c.centerX+2, c.centerY+2)
    else:
        c.triangle(c.centerX-3, c.centerY+2, c.centerX+2, c.centerY+2, c.centerX, c.centerY-2)
    
    n_flower += 3
    offset_a = -90
    if isRotate == 1:
        if n_flower % 2 == 1:
            offset_a += 180
        elif n_flower == 6:
            offset_a += 90
        else:
            offset_a += 45
    for a in range(0 + offset_a, 360 + offset_a, 360 // n_flower):
        posx = c.centerX + int(cos(a / 180 * pi) * 12)
        posy = c.centerY + int(sin(a / 180 * pi) * 12)
        if outerShape == 0:
            c.circle(posx, posy, 5)
        elif outerShape == 1:
            c.rect(posx-2, posy-2, posx+2, posy+2)
        else:
            c.triangle(posx-2, posy+2, posx+2, posy+2, posx, posy-2)

    
    return c


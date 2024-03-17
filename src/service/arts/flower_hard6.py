from src.service.art_canvas import Canvas, extractType2, extractType6
from math import sqrt, sin, cos, pi

n_type = 3 * 3 * 3 * 3 * 3 * 2

#* keep in mind that top left is (0, 0) and bottom right is (63, 47)
def get(type : int) -> Canvas:
    n_flower = 5
    oShapeType, isRotate = extractType2(type, 3**6, 2)
    oShape1, oShape2, oShape3, oShape4, oShape5, oShape6 = extractType6(oShapeType, 3, 3, 3, 3, 3, 3)
    oShape = [oShape1, oShape2, oShape3, oShape4, oShape5, oShape6]

    c = Canvas()

    # body of flower
    c.rect(c.centerX-1, c.centerY, c.centerX, c.bottom, 1)

    # middle shape of flower
    c.circle(c.centerX-1, c.centerY, 3)
    
    offset_a = -90
    if isRotate == 1:
        offset_a += 90
    for i in range(n_flower):
        a = offset_a + 360 // n_flower * i
        posx = c.centerX + int(cos(a / 180 * pi) * 12)
        posy = c.centerY + int(sin(a / 180 * pi) * 12)
        if oShape[i] == 0:
            c.circle(posx, posy, 5)
        elif oShape[i] == 1:
            c.rect(posx-2, posy-2, posx+2, posy+2)
        else:
            c.triangle(posx-2, posy+2, posx+2, posy+2, posx, posy-2)

    
    return c


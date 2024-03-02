from src.service.art_to import canvas, extractType3
from math import sqrt

n_type = 3 * 2 * 2

#* keep in mind that top left is (0, 0) and bottom right is (63, 47)
def get(type : int) -> canvas:
    posStone, isSun, isFlip = extractType3(type, 3, 2, 2)

    c = canvas()
    # left-Down triangle
    
    c.triangle(0, c.bottom, c.right, c.top, c.right, c.bottom)

    # roundStone
    r = 8
    dm = int(sqrt(2) * r / 2)
    cx = c.centerX
    cy = c.centerY
    if posStone == 1:
        cx = c.right - 7
        cy = c.top + 7
    elif posStone == 2:
        cx = c.left + 7
        cy = c.bottom - 7
    
    cx -= dm
    cy -= dm
    c.circle(cx, cy, r)

    # sun
    if isSun == 1:
        c.circle(c.left, c.top, 10)

    # flip?
    if isFlip == 1:
        c.flip(horizontal = True)
    
    return c
from src.service.art_canvas import Canvas, extractType3

n_type = 5 * 4 * 3

#* keep in mind that top left is (0, 0) and bottom right is (63, 47)
def get(type : int) -> Canvas:
    eye, mouth, whisker = extractType3(type, 5, 4, 3)

    c = Canvas()

    # nose
    c.triangle(c.centerX, c.centerY, c.centerX+3, c.centerY-3, c.centerX-3, c.centerY-3)
    if mouth & 1 == 1:
        c.pixel(c.centerX-1, c.centerY-3, 0)
        c.pixel(c.centerX+1, c.centerY-3, 0)
    
    # mouth
    c.line(c.centerX, c.centerY, c.centerX-3, c.centerY+3)
    c.line(c.centerX, c.centerY, c.centerX+3, c.centerY+3)
    if mouth & 2 == 2:
        c.line(c.centerX-3, c.centerY+3, c.centerX-6, c.centerY)
        c.line(c.centerX+3, c.centerY+3, c.centerX+6, c.centerY)
    # eyes
    if eye == 0:
        c.circle(c.width//4, c.height//3, 3)
        c.circle(c.width//4*3, c.height//3, 3)
    elif eye == 1:
        c.rect(c.width//4-2, c.height//3-2, c.width//4+2, c.height//3+2)
        c.rect(c.width//4*3-2, c.height//3-2, c.width//4*3+2, c.height//3+2)
    elif eye == 2:
        c.triangle(c.width//4, c.height//3, c.width//4+2, c.height//3-2, c.width//4-2, c.height//3-2)
        c.triangle(c.width//4*3, c.height//3, c.width//4*3+2, c.height//3-2, c.width//4*3-2, c.height//3-2)
    elif eye == 3:
        c.triangle(c.width//4, c.height//3-2, c.width//4+2, c.height//3, c.width//4-2, c.height//3)
        c.triangle(c.width//4*3, c.height//3-2, c.width//4*3+2, c.height//3, c.width//4*3-2, c.height//3)
    elif eye == 4:
        c.line(c.width//4-2, c.height//3-2, c.width//4+2, c.height//3+2)
        c.line(c.width//4-2, c.height//3+2, c.width//4+2, c.height//3-2)
        c.line(c.width//4*3-2, c.height//3-2, c.width//4*3+2, c.height//3+2)
        c.line(c.width//4*3-2, c.height//3+2, c.width//4*3+2, c.height//3-2)
    
    # whisker
    if whisker == 1:
        c.triangle(0, c.centerY, 1, c.centerY-1, 0, c.centerY-2)
        c.triangle(0, c.centerY, 1, c.centerY+1, 0, c.centerY+2)
        c.triangle(c.right, c.centerY, c.right-1, c.centerY-1, c.right, c.centerY-2)
        c.triangle(c.right, c.centerY, c.right-1, c.centerY+1, c.right, c.centerY+2)
    elif whisker == 2:
        c.line(0, c.centerY-1, 2, c.centerY-1)
        c.line(0, c.centerY+1, 2, c.centerY+1)
        c.line(c.right, c.centerY-1, c.right-2, c.centerY-1)
        c.line(c.right, c.centerY+1, c.right-2, c.centerY+1)

    return c

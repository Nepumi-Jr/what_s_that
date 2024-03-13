from src.service.art_canvas import Canvas

n_type = 4

#* keep in mind that top left is (0, 0) and bottom right is (63, 47)
def get(type : int) -> Canvas:
    eye_type = type

    c = Canvas()

    # nose
    c.triangle(c.centerX, c.centerY, c.centerX+2, c.centerY-2, c.centerX-2, c.centerY-2)
    
    # mouth
    c.line(c.centerX, c.centerY, c.centerX-3, c.centerY+3)
    c.line(c.centerX, c.centerY, c.centerX+3, c.centerY+3)

    # eyes
    if eye_type == 0:
        c.circle(c.width//4, c.height//3, 3)
        c.circle(c.width//4*3, c.height//3, 3)
    elif eye_type == 1:
        c.rect(c.width//4-2, c.height//3-2, c.width//4+2, c.height//3+2)
        c.rect(c.width//4*3-2, c.height//3-2, c.width//4*3+2, c.height//3+2)
    elif eye_type == 2:
        #c.triangle(c.width//4, c.height//3, c.width//4+2, c.height//3-2, c.width//4-2, c.height//3-2)
        #c.triangle(c.width//4*3, c.height//3, c.width//4*3+2, c.height//3-2, c.width//4*3-2, c.height//3-2)
        c.triangle(c.width//4, c.height//3-2, c.width//4+2, c.height//3, c.width//4-2, c.height//3)
        c.triangle(c.width//4*3, c.height//3-2, c.width//4*3+2, c.height//3, c.width//4*3-2, c.height//3)
    elif eye_type == 3:
        c.line(c.width//4-2, c.height//3-2, c.width//4+2, c.height//3+2)
        c.line(c.width//4-2, c.height//3+2, c.width//4+2, c.height//3-2)
        c.line(c.width//4*3-2, c.height//3-2, c.width//4*3+2, c.height//3+2)
        c.line(c.width//4*3-2, c.height//3+2, c.width//4*3+2, c.height//3-2)

    return c

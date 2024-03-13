from src.service.art_canvas import Canvas, extractType2

n_type = (1 << 4) * 2

#* keep in mind that top left is (0, 0) and bottom right is (63, 47)
def get(type : int) -> Canvas:
    arrow_segment, center_shape = extractType2(type, 1<<4, 2)

    c = Canvas()

    if center_shape == 0:
        c.rect(c.centerX-3, c.centerY-3, c.centerX+3, c.centerY+3)
    elif center_shape == 1:
        c.circle(c.centerX, c.centerY, 5)
    
    if arrow_segment & 1 == 1:
        c.rect(c.centerX-1, c.centerY-5, c.centerX+1, c.centerY-3)
        c.triangle(c.centerX-4, c.centerY-6, c.centerX+4, c.centerY-6, c.centerX, c.centerY-10)
    
    if arrow_segment & 2 == 2:
        c.rect(c.centerX-1, c.centerY+3, c.centerX+1, c.centerY+5)
        c.triangle(c.centerX-4, c.centerY+6, c.centerX+4, c.centerY+6, c.centerX, c.centerY+10)
    
    if arrow_segment & 4 == 4:
        c.rect(c.centerX-5, c.centerY-1, c.centerX-3, c.centerY+1)
        c.triangle(c.centerX-6, c.centerY-4, c.centerX-6, c.centerY+4, c.centerX-10, c.centerY)

    if arrow_segment & 8 == 8:
        c.rect(c.centerX+3, c.centerY-1, c.centerX+5, c.centerY+1)
        c.triangle(c.centerX+6, c.centerY-4, c.centerX+6, c.centerY+4, c.centerX+10, c.centerY)

    return c

from src.service.art_canvas import Canvas, extractType3
from math import sqrt, sin, cos, pi

n_type = 1 << 8

#* keep in mind that top left is (0, 0) and bottom right is (63, 47)
def get(type : int) -> Canvas:

    c = Canvas()

    if (type & 1):
        c.rect(c.centerX - 12, 3, c.centerX + 12, 3+3) # top segment
    
    if (type & (1 << 1)):
        c.rect(c.centerX + 12 - 4, 3 + 4, c.centerX + 12, 3 + 4 + 14)
    
    if (type & (1 << 2)):
        c.rect(c.centerX + 12 - 4, 26, c.centerX + 12, 26 + 14)
    
    if (type & (1 << 3)):
        c.rect(c.centerX - 12, 41, c.centerX + 12, 41+3)
    
    if (type & (1 << 4)):
        c.rect(c.centerX - 8 - 4, 26, c.centerX - 8, 26 + 14)
    
    if (type & (1 << 5)):
        c.rect(c.centerX - 8 - 4, 3 + 4, c.centerX - 8, 3 + 4 + 14)
    
    if (type & (1 << 6)):
        c.rect(c.centerX - 12, 22, c.centerX, 22+3)
    
    if (type & (1 << 7)):
        c.rect(c.centerX + 1, 22, c.centerX + 12, 22+3)

    return c

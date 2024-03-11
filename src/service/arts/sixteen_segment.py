from src.service.art_canvas import Canvas, extractType2
from src.util import permutation

n_type = 5 * 4000

#* keep in mind that top left is (0, 0) and bottom right is (63, 47)
def get(type : int) -> Canvas:

    n_seg, next_p = extractType2(type, 5, 4000)
    n_seg += 4
    bitList = [0 for _ in range(16)]
    for i in range(n_seg):
        bitList[i] = 1
    
    for i in range(next_p):
        permutation.nextPermutation(bitList)


    c = Canvas()
    x_left = c.centerX - 46 // 2
    x_center = c.centerX
    x_right = c.centerX + 46 // 2

    y_top = 0
    y_center = 46 // 2
    y_bottom = 46

    if (bitList[0]):
        c.line(x_left, y_top, x_center, y_top)
    
    if (bitList[1]):
        c.line(x_center, y_top, x_right, y_top)
    
    if (bitList[2]):
        c.line(x_right, y_top, x_right, y_center)
    
    if (bitList[3]):
        c.line(x_right, y_center, x_right, y_bottom)
    
    if (bitList[4]):
        c.line(x_center, y_bottom, x_right, y_bottom)
    
    if (bitList[5]):
        c.line(x_left, y_bottom, x_center, y_bottom)
    
    if (bitList[6]):
        c.line(x_left, y_center, x_left, y_bottom)
    
    if (bitList[7]):
        c.line(x_left, y_center, x_left, y_top)
    
    if (bitList[8]):
        c.line(x_center, y_center, x_left, y_top)
    
    if (bitList[9]):
        c.line(x_center, y_center, x_center, y_top)
    
    if (bitList[10]):
        c.line(x_center, y_center, x_right, y_top)
    
    if (bitList[11]):
        c.line(x_center, y_center, x_right, y_center)
    
    if (bitList[12]):
        c.line(x_center, y_center, x_right, y_bottom)
    
    if (bitList[13]):
        c.line(x_center, y_center, x_center, y_bottom)
    
    if (bitList[14]):
        c.line(x_center, y_center, x_left, y_bottom)
    
    if (bitList[15]):
        c.line(x_center, y_center, x_left, y_center)

    return c

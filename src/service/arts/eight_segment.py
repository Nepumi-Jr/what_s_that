from src.service.art_canvas import Canvas, extractType2
from src.util import permutation

n_type = 3 * 55

#* keep in mind that top left is (0, 0) and bottom right is (63, 47)
def get(type : int) -> Canvas:

    n_seg, next_p = extractType2(type, 3, 55)
    n_seg += 3
    bitList = [0 for _ in range(8)]
    for i in range(n_seg):
        bitList[i] = 1
    
    for i in range(next_p):
        permutation.nextPermutation(bitList)

    c = Canvas()

    if (bitList[0]):
        c.rect(c.centerX - 12, 3, c.centerX + 12, 3+3) # top segment
    
    if (bitList[1]):
        c.rect(c.centerX + 12 - 4, 3 + 4, c.centerX + 12, 3 + 4 + 14)
    
    if (bitList[2]):
        c.rect(c.centerX + 12 - 4, 26, c.centerX + 12, 26 + 14)
    
    if (bitList[3]):
        c.rect(c.centerX - 12, 41, c.centerX + 12, 41+3)
    
    if (bitList[4]):
        c.rect(c.centerX - 8 - 4, 26, c.centerX - 8, 26 + 14)
    
    if (bitList[5]):
        c.rect(c.centerX - 8 - 4, 3 + 4, c.centerX - 8, 3 + 4 + 14)
    
    if (bitList[6]):
        c.rect(c.centerX - 12, 22, c.centerX, 22+3)
    
    if (bitList[7]):
        c.rect(c.centerX + 1, 22, c.centerX + 12, 22+3)

    return c

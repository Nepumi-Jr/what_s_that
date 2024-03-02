from src.service import oled_lcd as oled
from time import sleep

from src.service.arts import flower_hard as art # < --- Change this line

cur_type = 0
c = art.get(cur_type)
oled.text("Test_art", 0, 0)
oled.rect(58, 3, 62 + c.width , 7 + c.height)
oled.delRect(59, 4, 61 + c.width, 6 + c.height)

while True:
    oled.delRect(0, 10, 57, 10 + 10)
    oled.delRect(60, 5, 60 + c.width - 1, 5 + c.height - 1)
    oled.text(f"{cur_type} / {art.n_type - 1}", 0, 10)
    oled.insertPixelImage(c.convert_to_int32_array(), 60, 5, c.width, c.height, True)

    cur_type = (cur_type + 1) % art.n_type
    c = art.get(cur_type)
    sleep(1)

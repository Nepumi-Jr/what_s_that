from machine import Pin, SoftI2C
from src.service.config import get_config, LCDDeviceType
from random import randint
import sh1106, ssd1306

config = get_config()

i2c = SoftI2C(scl = Pin(get_config().lcd.clock), sda = Pin(get_config().lcd.data))

if config.lcd.device == LCDDeviceType.SH1106:
    oled = sh1106.SH1106_I2C(128, 64, i2c, rotate=180) # 128 x 64
else:
    oled = ssd1306.SSD1306_I2C(128, 64, i2c, rotate=180)

# just test

for i in range(4):
    x1, x2 = randint(0, 127), randint(0, 127)
    if x2 < x1: x1, x2 = x2, x1
    y1, y2 = randint(0, 64), randint(0, 64)
    if y2 < y1: y1, y2 = y2, y1
    oled.fill_rect(x1, x2-x1, y1, y2-y1, 1)
    print(x1, x2-x1, y1, y2-y1)

oled.show()

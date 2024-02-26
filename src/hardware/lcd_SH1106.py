from machine import Pin, SoftI2C
from src.service.config import get_config
import sh1106

config = get_config()

i2c = SoftI2C(scl = Pin(get_config().lcd.clock), sda = Pin(get_config().lcd.data))
oled = sh1106.SH1106_I2C(128, 64, i2c, rotate=180) #? remove rotate=180?

def show():
    oled.show()

def text(text, x, y):
    oled.text(text, x, y)

def pixel(x, y):
    oled.pixel(x, y, 1)

def rect(x1, y1, x2, y2):
    if x1 > x2:
        x1, x2 = x2, x1
    if y1 > y2:
        y1, y2 = y2, y1
    
    oled.fill_rect(x1, y1, x2 - x1, y2 - y1, 1)

def delPixel(x, y):
    oled.pixel(x, y, 0)

def delRect(x1, y1, x2, y2):
    if x1 > x2:
        x1, x2 = x2, x1
    if y1 > y2:
        y1, y2 = y2, y1
    
    oled.fill_rect(x1, y1, x2 - x1, y2 - y1, 0)

def clear():
    oled.fill(0)

def width():
    return 128

def height():
    return 64

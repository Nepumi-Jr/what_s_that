from math import ceil
from src.hardware import lcd_SH1106 as sh1106
from src.hardware import lcd_SSD1306 as ssd1306
from src.service.config import get_config, LCDDeviceType

config = get_config()
if config.lcd.device == LCDDeviceType.SH1106:
    oled = sh1106
else:
    oled = ssd1306

class TextAlign:
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"

def width():
    return oled.width()

def height():
    return oled.height()

def CenterX():
    return (oled.width()) // 2

def CenterY(includingNav = True):
    return (oled.height() - (10 if includingNav else 0)) // 2

def show():
    oled.show()

def text(textStr, x, y, reload = True):
    oled.text(textStr, x, y)
    if reload:
        show()

def textAlign(textStr, x, y, align : TextAlign, reload = True): #! Warning : about text overflow
    if align == TextAlign.CENTER:
        x -= (len(textStr) * 6 + (len(textStr) - 1) * 2) // 2
    elif align == TextAlign.RIGHT:
        x -= (len(textStr) * 6 + (len(textStr) - 1) * 2)
    text(textStr, x, y, reload)

def clear(reload = True):
    oled.delRect(0, 0, oled.width() - 1, oled.height() - 11)
    if reload:
        show()

def pixel(x, y, reload = False):
    oled.pixel(x, y)
    if reload:
        show()

def delPixel(x, y, reload = False):
    oled.delPixel(x, y)
    if reload:
        show()

def rect(x1, y1, x2, y2, reload = False):
    oled.rect(x1, y1, x2, y2)
    if reload:
        show()

def delRect(x1, y1, x2, y2, reload = False):
    oled.delRect(x1, y1, x2, y2)
    if reload:
        show()

def insertPixelImage(int32Array, x, y, width, height, reload = False):
    startX = x
    startY = y

    for y in range(height):
        for x in range(width):
            posXCal = width - x - 1
            arrayInd = y * ceil(width / 32) + ceil(width / 32) - posXCal // 32 - 1
            bitPos = posXCal % 32

            if (int32Array[arrayInd] >> bitPos) & 1:
                pixel(startX + x, startY + y)
            else:
                delPixel(startX + x, startY + y)
            
    if reload:
        show()


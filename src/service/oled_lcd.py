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

def _checkTextOverflow(textStr, x = 0):
    if x < 0 or x > oled.width():
        Exception("Text overflow")
    if len(textStr) * 6 + (len(textStr) - 1) * 2 + x > oled.width():
        Exception("Text overflow")

def text(textStr, x, y, align : TextAlign = TextAlign.LEFT, reload = False): 
    '''เขียนข้อความ ที่ xy และจัดตำแหน่งตาม align'''
    if align == TextAlign.CENTER:
        x -= (len(textStr) * 6 + (len(textStr) - 1) * 2) // 2
    elif align == TextAlign.RIGHT:
        x -= (len(textStr) * 6 + (len(textStr) - 1) * 2)

    _checkTextOverflow(textStr, x)
    oled.text(textStr, x, y)
    if reload:
        show()

def textInLine(textStr, x, lineNumber, align : TextAlign = TextAlign.LEFT, reload = False):
    '''เขียนข้อความในบรรทัด (linenumber 0-4)'''
    assert lineNumber >= 0 and lineNumber < 5
    delRect(0, lineNumber * 10, oled.width(), lineNumber * 10 + 9, False)
    text(textStr, x, lineNumber * 10, align, reload)

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
    '''วาดสี่เหลี่ยม ที่มีมุมบนซ้ายที่ xy1 และมุมล่างขวาที่ xy2'''
    oled.rect(x1, y1, x2, y2)
    if reload:
        show()

def delRect(x1, y1, x2, y2, reload = False):
    '''ลบ(เคลียร์พื้นที่)สี่เหลี่ยม ที่มีมุมบนซ้ายที่ xy1 และมุมล่างขวาที่ xy2'''
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


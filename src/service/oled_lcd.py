from src.hardware import lcd_SH1106 as sh1106
from src.hardware import lcd_SSD1306 as ssd1306
from src.service.config import get_config, LCDDeviceType

config = get_config()
if config.lcd.device == LCDDeviceType.SH1106:
    oled = sh1106
else:
    oled = ssd1306


def text(text, x, y, reload = True):
    oled.text(text, x, y)
    if reload:
        oled.show()

def clear(reload = True):
    oled.delRect(0, 0, oled.width() - 1, oled.height() - 11)
    if reload:
        oled.show()

def pixel(x, y, reload = False):
    oled.pixel(x, y)
    if reload:
        oled.show()

def delPixel(x, y, reload = False):
    oled.delPixel(x, y)
    if reload:
        oled.show()

def rect(x1, y1, x2, y2, reload = False):
    oled.rect(x1, y1, x2, y2)
    if reload:
        oled.show()

def delRect(x1, y1, x2, y2, reload = False):
    oled.delRect(x1, y1, x2, y2)
    if reload:
        oled.show()
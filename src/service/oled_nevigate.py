from src.hardware import lcd_SH1106 as sh1106
from src.hardware import lcd_SSD1306 as ssd1306
from src.service.config import get_config, LCDDeviceType

config = get_config()
if config.lcd.device == LCDDeviceType.SH1106:
    oled = sh1106
else:
    oled = ssd1306

isFourButton = config.button.button4 != None
useGraphic = [None, None, None, None]

# the Art (icon) start here

class Icon: # 16x8 pixel
    width = 16
    height = 8

    UP = [0xC003, 0x8001, 0x0180, 0x03C0, 0x07E0, 0x0FF0, 0x8001, 0xC003]
    DOWN = [0xC003, 0x8001, 0x0FF0, 0x07E0, 0x03C0, 0x0180, 0x8001, 0xC003]
    RIGHT = [0xC003, 0x8041, 0x0060, 0x0FF0, 0x0FF0, 0x0060, 0x8041, 0xC003] 
    LEFT = [0xC003, 0x8101, 0x0300, 0x0FF0, 0x0FF0, 0x0300, 0x8101, 0xC003]
    CONFIRM = [0xC003, 0x8021, 0x0060, 0x08C0, 0x0D80, 0x0700, 0x8201, 0xC003]
    BACK = [0xC003, 0x80E1, 0x00C0, 0x04A0, 0x0410, 0x0220, 0x81C1, 0xC003]


def reset():
    oled.rect(0, oled.height() - 11, oled.width() - 1, oled.height() - 1)
    useGraphic = [None, None, None, None]

def _getStartPos(index :int):
    xCenter = (2 * index + 1) * oled.width() // ((4 if isFourButton else 3) * 2)
    xStart = xCenter - Icon.width // 2
    yStart = oled.height() - 10

    return xStart, yStart

def replaceIcon(index :int , icon :Icon):
    useGraphic[index] = icon
    xStart, yStart = _getStartPos(index)

    # start from top left
    for y in range(Icon.height):
        for x in range(Icon.width):
            if (icon[y] >> (Icon.width - x - 1)) & 1:
                oled.pixel(xStart + x, yStart + y, 1)
            else:
                oled.pixel(xStart + x, yStart + y, 0)
    oled.show()

def clearIcon(index :int):
    useGraphic[index] = None
    xStart, yStart = _getStartPos(index)
    oled.rect(xStart, yStart, xStart + Icon.width, yStart + Icon.height)
    oled.show()
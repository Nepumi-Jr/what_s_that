from src.service.config import get_config
from src.service import oled_lcd as oled

config = get_config()

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

    W_ALPHA = [0xE7E7, 0xE7E7, 0xE7E7, 0xE667, 0xE427, 0xE187, 0xE7E7, 0xFFFF]
    A_ALPHA = [0xFE7F, 0xFC3F, 0xF99F, 0xF81F, 0xF99F, 0xF99F, 0xF99F, 0xFFFF]
    I_ALPHA = [0xFC3F, 0xFE7F, 0xFE7F, 0xFE7F, 0xFE7F, 0xFE7F, 0xFC3F, 0xFFFF]
    T_ALPHA = [0xF81F, 0xFE7F, 0xFE7F, 0xFE7F, 0xFE7F, 0xFE7F, 0xFE7F, 0xFFFF]


def reset():
    oled.rect(0, oled.height() - 11, oled.width() - 1, oled.height() - 1)
    useGraphic = [None, None, None, None]

def _getStartPos(index :int, ForceFourButton = False):
    xCenter = (2 * index + 1) * oled.width() // ((4 if (isFourButton or ForceFourButton) else 3) * 2)
    xStart = xCenter - Icon.width // 2
    yStart = oled.height() - 10

    return xStart, yStart

def setButtonIcon(index :int , icon :Icon):
    useGraphic[index] = icon
    xStart, yStart = _getStartPos(index)

    # start from top left
    for y in range(Icon.height):
        for x in range(Icon.width):
            if (icon[y] >> (Icon.width - x - 1)) & 1:
                oled.pixel(xStart + x, yStart + y)
            else:
                oled.delPixel(xStart + x, yStart + y)
    
    oled.show()

def setWait():
    waitIcons = [Icon.W_ALPHA, Icon.A_ALPHA, Icon.I_ALPHA, Icon.T_ALPHA]
    for i, icon in enumerate(waitIcons):
        useGraphic[i] = icon
        xStart, yStart = _getStartPos(i, True)
        for y in range(Icon.height):
            for x in range(Icon.width):
                if (icon[y] >> (Icon.width - x - 1)) & 1:
                    oled.pixel(xStart + x, yStart + y)
                else:
                    oled.delPixel(xStart + x, yStart + y)
    oled.show()

def clearIcon(index :int):
    useGraphic[index] = None
    xStart, yStart = _getStartPos(index)
    oled.rect(xStart, yStart, xStart + Icon.width, yStart + Icon.height, True)
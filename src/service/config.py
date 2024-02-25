import configparser
from enum import Enum

class DeviceType(Enum):
    PLAY = "play"
    TRANSLATE = "translate"

class LCDDeviceType(Enum):
    SH1106 = "SH1106"
    SSD1306 = "SSD1306"


def _device_type_from_string(deviceType:str):
    if deviceType == DeviceType.PLAY:
        return DeviceType.PLAY
    elif deviceType == DeviceType.TRANSLATE:
        return DeviceType.TRANSLATE
    else:
        return None

def _lcd_device_type_from_string(lcdDeviceType:str):
    if lcdDeviceType == LCDDeviceType.SH1106:
        return LCDDeviceType.SH1106
    elif lcdDeviceType == LCDDeviceType.SSD1306:
        return LCDDeviceType.SSD1306
    else:
        return None

class Device:
    mode:DeviceType = None

class Button:
    button1:int = None
    button2:int = None
    button3:int = None
    button4:int = None

class Lcd:
    device:LCDDeviceType = None
    data:int = None
    clock:int = None

class DigitDisp:
    data:int = None
    clock:int = None

class Config:
    device:Device = None
    button:Button = None
    lcd:Lcd = None
    digitDisp:DigitDisp = None

_config = Config()
_isInit = False

def init():
    global _config

    configIni = configparser.ConfigParser()
    configIni.read('config.ini')

    _config.device = Device()
    _config.device.mode = _device_type_from_string(configIni['device']['mode'])

    _config.button = Button()
    _config.button.button1 = int(configIni['button']['button1'])
    _config.button.button2 = int(configIni['button']['button2'])
    _config.button.button3 = int(configIni['button']['button3'])
    _config.button.button4 = int(configIni['button']['button4']) if configIni['button']['button4'] != "" else None

    _config.lcd = Lcd()
    _config.lcd.device = _lcd_device_type_from_string(configIni['lcd']['device'])
    _config.lcd.data = int(configIni['lcd']['data'])
    _config.lcd.clock = int(configIni['lcd']['clock'])

    _config.digitDisp = DigitDisp()
    _config.digitDisp.data = int(configIni['digitDisp']['data'])
    _config.digitDisp.clock = int(configIni['digitDisp']['clock'])

def get_config() -> Config:
    global _isInit
    if not _isInit:
        init()
        _isInit = True
    return _config
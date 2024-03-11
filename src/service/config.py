class DeviceType():
    PLAY = "play"
    TRANSLATE = "translate"

class LCDDeviceType():
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
    uart_tx:int = None
    uart_rx:int = None
    skip_sync:bool = False

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

    configIni = configRead('config.ini')

    _config.device = Device()
    _config.device.skip_sync = configIni['device']['skip_sync'].lower() == "true"
    _config.device.mode = _device_type_from_string(configIni['device']['mode'])
    _config.device.uart_tx = int(configIni['device']['uart_tx'])
    _config.device.uart_rx = int(configIni['device']['uart_rx'])

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
    _config.digitDisp.data = int(configIni['digitDisp']['data']) if configIni['digitDisp']['data'] != "" else None
    _config.digitDisp.clock = int(configIni['digitDisp']['clock']) if configIni['digitDisp']['clock'] != "" else None

def configRead(path : str) -> dict:
    # configparser not working in micropython :(
    rawText = ""
    try:
        with open(path, 'r') as file:
            rawText = file.read()
    except Exception as e:
        print("Error reading config file: ", e)
        raise Exception("Error reading config file: ", e)
    
    config = {}
    header = None
    for l in rawText.split('\n'):
        line = l.strip()
        if '#' in line:
            line = line.split('#')[0]
        
        if "[" in line and "]" in line:
            header = line[line.index("[")+1:line.index("]")]
        
        elif "=" in line:
            chunk = line.split("=")
            key = chunk[0].strip()
            value = "=".join(chunk[1:]).strip()
            if header == None:
                raise Exception("No header found in config file")

            if header not in config:
                config[header] = {}

            config[header][key] = value
    return config


def get_config() -> Config:
    global _isInit
    if not _isInit:
        init()
        _isInit = True
    return _config


if __name__ == "__main__":
    print(DeviceType.PLAY)
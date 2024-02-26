from machine import UART
from src.service import config

config = config.get_config()                       # init with given baudrate
uart = UART(2, baudrate=9600, tx=config.device.uart_tx, rx=config.device.uart_rx)


def send(data) -> bool:
    if not uart.txdone():
        return False
    uart.write(data)
    return True


def read():
    if uart.any():
        data = uart.read()
        try:
            strData = data.decode("utf8")
            return strData
        except:
           pass 
    return None
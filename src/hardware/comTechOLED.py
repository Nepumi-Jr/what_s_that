from machine import Pin, SoftI2C
import ssd1306
from time import sleep

i2c = SoftI2C(scl = Pin(27), sda = Pin(26))

oled = ssd1306.SSD1306_I2C(128, 64, i2c)
def observer():
    while True:
        oled.fill(0)
        oled.text("Peeraphol 167-9", 0, 0, 1)
        oled.text("Tanapat 415-6", 0, 10, 1)
        oled.show()
        sleep(10)

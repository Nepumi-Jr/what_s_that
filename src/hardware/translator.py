from machine import Pin, SoftI2C
import ssd1306
from time import sleep

i2c = SoftI2C(scl = Pin(17), sda = Pin(16))

oled = ssd1306.SSD1306_I2C(128, 64, i2c)
def mainMenu():
    selectPlay = True # default
    if(selectPlay):
        oled.fill(0)
        oled.text("Main menu", 28, 10, 1)
        oled.text(">", 40, 25, 1)
        oled.text("Play", 48, 25, 1)
        oled.text("<", 80, 25, 1)
        oled.show()

def syncingPage():
    oled.fill(0)
    oled.text("Syncing...", 24, 32, 1)
    oled.show()
    
def mainGame():
    oled.fill(0)
    oled.text("Easy", 0, 0, 1)
    oled.text("1", 120, 0, 1)
    oled.text("<", 0, 20, 1)
    oled.text("PIC", 52, 20, 1)
    oled.text(">", 120, 20, 1)
    oled.text("1 2 3 4", 36, 40, 1)
    oled.show()
    
def success():
    oled.fill(0)
    oled.text("Success", 36, 32, 1)
    oled.show()
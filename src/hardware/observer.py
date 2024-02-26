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
        oled.text("Scoreboard", 24, 40, 1)
        oled.show()
    else:
        oled.fill(0)
        oled.text("Main menu", 28, 10, 1)
        oled.text("Play", 48, 25, 1)
        oled.text(">", 12, 25, 1)
        oled.text("Scoreboard", 24, 40, 1)
        oled.text("<", 108, 25, 1)
        oled.show()
        
def scoreboard():
    oled.fill(0)
    oled.text("Scoreboard", 24, 0, 1)
    rowSize = 12
    #oled.text(NAME[idx], 0, rowSize, 1)
    #oled.text(SCORE[idx] +": "+ SCORE, 88, rowSize, 1)
    #-----------------------------------------
    #oled.text(MAP_SCORE.key[idx], 0, rowSize, 1)
    #oled.text(MAP_SCORE.value[idx], 88, rowSize, 1)
    #MOCK UP
    oled.text("SUD LHOR", 0, rowSize, 1)
    oled.text("00:00", 88, rowSize, 1)
    oled.text("TOR", 0, rowSize+12, 1)
    oled.text("10:00", 88, rowSize+12, 1)
    oled.text("FEEL", 0, rowSize+24, 1)
    oled.text("20:00", 88, rowSize+24, 1)
    oled.show()
    
def syncingPage():
    oled.fill(0)
    oled.text("Syncing...", 24, 32, 1)
    oled.show()
    
def selectDiff():
    oled.fill(0)
    oled.text("Difficulty", 24, 0, 1)
    oled.text("Easy", 48, 10, 1)
    oled.text("Normal", 40, 20, 1)
    oled.text("Hard", 48, 30, 1)
    oled.text("Funny", 44, 40, 1)
    oled.show()
    
def mainGame():
    oled.fill(0)
    oled.text("Easy", 0, 0, 1)
    oled.text("1", 120, 0, 1)
    oled.text("PIC", 52, 20, 1)
    oled.text("__ __ __ __", 20, 40, 1)
    oled.show()

def answerResult(answerResult : bool):
    oled.fill(0)
    if(answerResult):
        oled.text("Correct", 36, 32, 1)
        oled.show()
    else:
        oled.text("Wrong", 44, 32, 1)
        oled.show()

def timeUp():
    oled.fill(0)
    oled.text("Time up", 36, 25, 1)
    oled.text("(Game over)", 20, 35, 1)
    oled.show()

def success():
    oled.fill(0)
    oled.text("Success", 36, 32, 1)
    oled.show()
    
def teamName():
    oled.fill(0)
    oled.text("Team name", 28, 5, 1)
    oled.text("DUCK", 48, 20, 1)
    oled.text("00:00", 44, 35, 1)
    oled.show()


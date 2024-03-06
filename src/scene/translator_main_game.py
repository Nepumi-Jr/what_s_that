from src.service import time_counter, button, oled_lcd, oled_nevigate
from src.service.oled_lcd import TextAlign
from src import game_settings
from src.util import log
from src.service import art_to as art
from time import sleep, time_ns
from src.service.scene_nevigate import SCENE as scene

FRAME_RATE = 15

def main(): # menu
    oled_lcd.clear()
    oled_nevigate.reset()
    oled_nevigate.setButtonIcon(0, oled_nevigate.Icon.CONFIRM)
    oled_nevigate.setButtonIcon(1, oled_nevigate.Icon.CONFIRM)
    oled_nevigate.setButtonIcon(2, oled_nevigate.Icon.CONFIRM)
        
    pTime = time_ns()
    while True:
        if(button.is_first_press(0) or button.is_first_press(1) or button.is_first_press(2)):
            return scene.TRANSLATOR_SYNC
        
        button.clock_tick(1 / FRAME_RATE)
        cTime = time_ns()
        dTime = cTime - pTime
        pTime = cTime
        sleep(max((1 / FRAME_RATE) - (dTime / 10000000000), 0))
        
def syncing():
    oled_lcd.clear()
    oled_nevigate.reset()
    oled_nevigate.setButtonIcon(0, oled_nevigate.Icon.W_ALPHA)
    oled_nevigate.setButtonIcon(1, oled_nevigate.Icon.A_ALPHA)
    oled_nevigate.setButtonIcon(2, oled_nevigate.Icon.I_ALPHA)
    #oled_nevigate.setButtonIcon(3, oled_nevigate.Icon.T_ALPHA)
    '''Something form UART'''
    pTime = time_ns()
    while True:
        if(button.is_first_press(0) or button.is_first_press(1) or button.is_first_press(2)):
            translator_main_game()
        button.clock_tick(1 / FRAME_RATE)
        cTime = time_ns()
        dTime = cTime - pTime
        pTime = cTime
        sleep(max((1 / FRAME_RATE) - (dTime / 10000000000), 0))
    
def translator_main_game():
    symbol = 0
    oled_lcd.clear()
    oled_nevigate.reset()
    oled_nevigate.setButtonIcon(0, oled_nevigate.Icon.LEFT)
    oled_nevigate.setButtonIcon(1, oled_nevigate.Icon.BACK)
    oled_nevigate.setButtonIcon(2, oled_nevigate.Icon.RIGHT)
    oled_lcd.text("Easy", 0, 0, TextAlign.LEFT)
    oled_lcd.text(f"Symbol {symbol + 1}#", 128, 0, TextAlign.RIGHT)
    oled_lcd.text("<", 0, 25,TextAlign.LEFT)
    '''แก้เป๋นรูป[symbol]'''
    c = art.getEasy()
    oled_lcd.insertPixelImage(c.convert_to_int32_array(), 58, 10, c.width, c.height -10, True)
    oled_lcd.text(">", 128, 25,TextAlign.RIGHT)
    oled_lcd.show()
    pTime = time_ns()
    mockUpCode=[1234,5678,1011,8956,5522]
    while True:
        if(button.is_first_press(0)):
            symbol = max(symbol-1, 0)
            oled_lcd.delRect(10, 10, 58, c.height -10)
            oled_lcd.text(f"{mockUpCode[symbol]}", 10, 25,TextAlign.LEFT)
            oled_lcd.delRect(58, 10, c.width, c.height -10)
            '''แก้เป๋นรูป[symbol]'''
            c = art.getEasy()
            oled_lcd.insertPixelImage(c.convert_to_int32_array(), 58, 10, c.width, c.height -10, True)
        if(button.is_first_press(2)):
            symbol = min(symbol+1, 4)
            oled_lcd.delRect(10, 10, 58, c.height -10)
            oled_lcd.text(f"{mockUpCode[symbol]}", 10, 25,TextAlign.LEFT)
            oled_lcd.delRect(58, 10, c.width, c.height -10)
            '''แก้เป๋นรูป[symbol]'''
            c = art.getEasy()
            oled_lcd.insertPixelImage(c.convert_to_int32_array(), 58, 10, c.width, c.height -10, True)
        oled_lcd.delRect(40, 0, 128, 10)
        oled_lcd.text(f"Symbol {symbol + 1}#", 128, 0, TextAlign.RIGHT)
        oled_lcd.show()
        button.clock_tick(1 / FRAME_RATE)
        cTime = time_ns()
        dTime = cTime - pTime
        pTime = cTime
        sleep(max((1 / FRAME_RATE) - (dTime / 10000000000), 0))
        
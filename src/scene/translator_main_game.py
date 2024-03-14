from src.service import time_counter, button, oled_lcd, oled_nevigate
from src.service.oled_lcd import TextAlign
from src.service.sound_trigger import soundTrigger
from src import game_settings
from src.util import log
from src.service import art_set as art
from time import sleep, time_ns
from src.service.scene import SCENE as scene
from src.scene import translator_sync
from src.service import main_game_service as game_service

FRAME_RATE = 15

def main(): # menu
    oled_lcd.clear()
    oled_nevigate.reset()
    oled_nevigate.setButtonIcon(0, oled_nevigate.Icon.CONFIRM)
    oled_nevigate.setButtonIcon(1, oled_nevigate.Icon.CONFIRM)
    oled_nevigate.setButtonIcon(2, oled_nevigate.Icon.CONFIRM)
    
    oled_lcd.text("Translator", 64, 10, TextAlign.CENTER)
    oled_lcd.text(">Play<", 64, 20, TextAlign.CENTER)
    oled_lcd.text("(Press to start)", 64, 30, TextAlign.CENTER)
    oled_lcd.show()
        
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
    oled_nevigate.setWait()
    '''Something form UART'''
    pTime = time_ns()
    return translator_sync.main()
    
def translator_main_game():
    symbol = 0
    cur_round = game_service.cur_round
    oled_lcd.clear()
    oled_nevigate.reset()
    oled_nevigate.setButtonIcon(0, oled_nevigate.Icon.LEFT)
    oled_nevigate.setButtonIcon(1, oled_nevigate.Icon.BACK)
    oled_nevigate.setButtonIcon(2, oled_nevigate.Icon.RIGHT)
    oled_lcd.text(f"Rd. {cur_round + 1}/{game_service.n_round}", 0, 0, TextAlign.LEFT)
    oled_lcd.text(f"Pic #{symbol + 1}", 0, 10)
    oled_lcd.text("<", 0, 25,TextAlign.LEFT)
    drawScreen(cur_round, symbol)
    oled_lcd.text(">", 128, 25,TextAlign.RIGHT)
    oled_lcd.show()
    pTime = time_ns()
    while True:
        if(button.is_first_press(0)):
            symbol = max(symbol-1, 0)
            drawScreen(cur_round, symbol)
        if(button.is_first_press(1)):
            cur_round = (cur_round + 1) % game_service.n_round
            drawScreen(cur_round, symbol)
        if(button.is_first_press(2)):
            symbol = min(symbol+1, len(game_service.fake_code_symbol[cur_round]) -1)
            drawScreen(cur_round, symbol)
        soundTrigger(False)
        button.clock_tick(1 / FRAME_RATE)
        cTime = time_ns()
        dTime = cTime - pTime
        pTime = cTime
        sleep(max((1 / FRAME_RATE) - (dTime / 10000000000), 0))
    
    '''หมดเวลา / observer เสร็จ (รอรับผ่าน uart)'''
    return scene.TRANSLATOR_RESULT

def result():
    oled_lcd.clear()
    oled_nevigate.reset()
    oled_nevigate.setButtonIcon(0, oled_nevigate.Icon.CORRECT)
    oled_nevigate.setButtonIcon(1, oled_nevigate.Icon.CORRECT)
    oled_nevigate.setButtonIcon(2, oled_nevigate.Icon.CORRECT)
        
def drawScreen(cur_round : int, symbol : int):
    oled_lcd.delRect(10, 10, 58, c.height -10)
    oled_lcd.text(f"{game_service.fake_code_symbol[cur_round][symbol].code:04d}", 16, 30,TextAlign.LEFT)
    oled_lcd.delRect(58, 10, c.width, c.height -10)
    '''แก้เป๋นรูป[symbol]'''
    c = game_service.get_canvas_from_CodeAndSymbol(game_service.fake_code_symbol[cur_round][symbol])
    oled_lcd.insertPixelImage(c.convert_to_int32_array(), 58, 0, c.width, c.height, True)
    oled_lcd.delRect(0, 10, 57, 20)
    oled_lcd.text(f"Pic #{symbol + 1}", 0, 10)
    oled_lcd.show()

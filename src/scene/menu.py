from src.service import time_counter, button, oled_lcd, oled_nevigate
from src.service import main_game_service as game_service
from src.service.main_game_service import Difficulty as diff
from src.service.scene import SCENE as scene
from src.service.oled_lcd import TextAlign
from src.service import score_board as score_service
from time import sleep, time_ns

FRAME_RATE = 30
title_logo = [0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000004, 0x00000000, 0x00000000, 0x00000000, 0x0000000C, 0x30000000, 0x00000000, 0x00000000, 0x0000000C, 0x70000000, 0x00000000, 0x00000000, 0x00000006, 0xF0000000, 0x00000000, 0x00000000, 0x00000006, 0xF0000000, 0x00000000, 0x00000000, 0x00000007, 0xB0000000, 0x00000000, 0x00000000, 0x00000007, 0x30000000, 0x00000000, 0x00000000, 0x00000006, 0x30000000, 0x00000000, 0x00000000, 0x00000000, 0x30000000, 0x00000000, 0x00000000, 0x00000000, 0x30000000, 0x00000000, 0x00000000, 0x00000000, 0x30000000, 0x00000000, 0x00000000, 0x07800000, 0x300E3000, 0x00000000, 0x00000000, 0x1FF03830, 0x303FF000, 0x00000000, 0x00000000, 0x3C787C30, 0x303BE000, 0x00000000, 0x00000000, 0x70186670, 0x30700000, 0x00000000, 0x072000C0, 0x701C6C60, 0x307E0000, 0x00000000, 0x056000C0, 0x0E1C7FE0, 0x303F8000, 0x000001F0, 0x03C000C0, 0x1F1C1FC0, 0x3003E0C2, 0x38700118, 0x000000C0, 0x1B1C0000, 0x3000E162, 0x7CF9CC18, 0x1898C786, 0x391C0000, 0x3000E0E2, 0xCD8D5810, 0x28A8D985, 0x3F1C1830, 0x3000E062, 0x040CF030, 0x189CD3C7, 0x3E1C7C30, 0x3000E062, 0x040C0060, 0x088CCFD3, 0x381C6670, 0x3E03E062, 0x040CCC60, 0x088CC8DB, 0x381C6660, 0x3E07E0F2, 0x041D4800, 0x1C8DCCCF, 0x1C1C7DE0, 0x330660BE, 0x042DF860, 0x178F4AC7, 0x1FF83FC0, 0x3706E0E6, 0x0418F060, 0x198DCCC3, 0x0FF00600, 0x1E03C000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000]


def main():
    oled_lcd.clear()
    oled_nevigate.reset()
    oled_nevigate.setButtonIcon(0, oled_nevigate.Icon.UP)
    oled_nevigate.setButtonIcon(1, oled_nevigate.Icon.DOWN)
    oled_nevigate.setButtonIcon(2, oled_nevigate.Icon.CONFIRM)
    oled_nevigate.setButtonIcon(3, oled_nevigate.Icon.CONFIRM)
    
    oled_lcd.insertPixelImage(title_logo, 0, 0, 128, 30)
    
    
    menu_selected_ind = 0
    def reload_choice():
        for i, e in enumerate(["Play", "Scoreboard"]):
            if i == menu_selected_ind:
                oled_lcd.textInLine(f"> {e} <", oled_lcd.CenterX(), 3 + i, TextAlign.CENTER)
            else:
                oled_lcd.textInLine(f"{e}", oled_lcd.CenterX(), 3 + i, TextAlign.CENTER)
        oled_lcd.show()

    reload_choice()

    pTime = time_ns()
    while True:

        if(button.is_first_press(0)) or (button.is_first_press(1)):
            menu_selected_ind = (menu_selected_ind + 1) % 2
            reload_choice()

        elif (button.is_first_press(2)) or (button.is_first_press(3)):
            if menu_selected_ind == 0:
                return scene.DIFFICULTY_SELECT
            else:
                return scene.SCORE_BOARD
        
        
        button.clock_tick(1 / FRAME_RATE)
        cTime = time_ns()
        dTime = cTime - pTime
        pTime = cTime
        sleep(max((1 / FRAME_RATE) - (dTime / 10000000000), 0))


def difficulty_select():
    oled_lcd.clear()
    oled_nevigate.reset()
    oled_nevigate.setButtonIcon(0, oled_nevigate.Icon.UP)
    oled_nevigate.setButtonIcon(1, oled_nevigate.Icon.DOWN)
    oled_nevigate.setButtonIcon(2, oled_nevigate.Icon.BACK)
    oled_nevigate.setButtonIcon(3, oled_nevigate.Icon.CONFIRM)
    
    oled_lcd.textInLine("Difficulty", oled_lcd.CenterX(), 0, TextAlign.CENTER)

    selected_diff = 0
    list_diff = [diff.EASY, diff.NORMAL, diff.HARD, diff.SILENT]
    def reload_choice():
        for i, e in enumerate(list_diff):    
            if i == selected_diff:
                oled_lcd.textInLine(f"> {e} <", oled_lcd.CenterX(), 1 + i, TextAlign.CENTER)
            else:
                oled_lcd.textInLine(f"{e}", oled_lcd.CenterX(), 1 + i, TextAlign.CENTER)
        oled_lcd.show()
    
    reload_choice()
    pTime = time_ns()
    while True:

        if(button.is_first_press(0)):
            selected_diff = (selected_diff - 1) % 4
            reload_choice()
        elif (button.is_first_press(1)):
            selected_diff = (selected_diff + 1) % 4
            reload_choice()
        elif (button.is_first_press(2)):
            return scene.MENU
        elif (button.is_first_press(3)):
            game_service.cur_diff = list_diff[selected_diff]
            print("Set difficulty to", game_service.cur_diff)
            return scene.SYNC
        
        
        button.clock_tick(1 / FRAME_RATE)
        cTime = time_ns()
        dTime = cTime - pTime
        pTime = cTime
        sleep(max((1 / FRAME_RATE) - (dTime / 10000000000), 0))

def score_board():
    oled_lcd.clear()
    oled_nevigate.reset()
    oled_nevigate.setButtonIcon(0, oled_nevigate.Icon.LEFT)
    oled_nevigate.setButtonIcon(1, oled_nevigate.Icon.RIGHT)
    oled_nevigate.setButtonIcon(2, oled_nevigate.Icon.BACK)

    oled_lcd.textInLine("Scoreboard", oled_lcd.CenterX(), 0, TextAlign.CENTER)
    diff_index = 0
    diffs = [diff.EASY, diff.NORMAL, diff.HARD, diff.SILENT]
    def reload_score_diff():
        oled_lcd.textInLine(f"< {diffs[diff_index]} >", oled_lcd.CenterX(), 1, TextAlign.CENTER)
        record = score_service.get_score_board_data(diffs[diff_index])
        for  i , (name, time_use) in enumerate(record):
            time_min = time_use // 60
            time_sec = time_use % 60
            oled_lcd.textInLine(f"{time_min:02}:{time_sec:02}", oled_lcd.width() - 1, 2 + i, TextAlign.RIGHT)
            oled_lcd.text(name, 0, (2 + i) * 10)
        oled_lcd.show()

    reload_score_diff()
    pTime = time_ns()
    while True:
        if(button.is_first_press(0)):
            diff_index = (diff_index - 1) % len(diffs)
            reload_score_diff()
        elif (button.is_first_press(1)):
            diff_index = (diff_index + 1) % len(diffs)
            reload_score_diff()
        elif (button.is_first_press(2)):
            return scene.MENU
        
        button.clock_tick(1 / FRAME_RATE)
        cTime = time_ns()
        dTime = cTime - pTime
        pTime = cTime
        sleep(max((1 / FRAME_RATE) - (dTime / 10000000000), 0))

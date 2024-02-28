from src.service import time_counter, button, oled_lcd, oled_nevigate
from src import game_settings
from src.util import log
from src.service import art_to as art
from time import sleep


FRAME_RATE = 15


def main():

    oled_lcd.clear()
    oled_nevigate.reset()
    oled_nevigate.setButtonIcon(0, oled_nevigate.Icon.UP)
    oled_nevigate.setButtonIcon(1, oled_nevigate.Icon.DOWN)
    oled_nevigate.setButtonIcon(2, oled_nevigate.Icon.LEFT)
    oled_nevigate.setButtonIcon(3, oled_nevigate.Icon.RIGHT)

    oled_lcd.textInLine("Lv. 2/3", 0, 0)
    oled_lcd.textInLine("Normal", 0, 1)    
    oled_lcd.textInLine("____O", 0, 3)
    
    c = art.getEasy()
    oled_lcd.insertPixelImage(c.convert_to_int32_array(), 60, 0, c.width, c.height, True)

    return
    time_counter.reset()
    time_limit = game_settings.number_of_stage * 15 * 60 # 10 minute per round
    while time_counter.time_use < time_limit:
        if(button.is_first_press(0)): print("HEE")
        if(button.is_hold(0)): print("HUM")
        # decrease the time, disp and wait
        time_counter.count_tick_time( 1 / FRAME_RATE)
        button.clock_tick(1 / FRAME_RATE)
        sleep(1 / FRAME_RATE)
    
    print("Time's up!")

if __name__ == "__main__":
    main()
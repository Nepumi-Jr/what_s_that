from src.service import time_counter, button, oled_lcd, oled_nevigate
from src import game_settings
from src.util import log
from src.service import art_to as art
from time import sleep, time_ns


FRAME_RATE = 15

cur_code = [0, 0, 0, 0]
cur_ind = 0

UP_ARROW = [0x0C,0x1E, 0x33] # 6 x 3
DOWN_ARROW = [0x33,0x1E,0x0C] # 6 x 3

UP_BRA = [0x3F,0x21, 0x21] # 6 x 3
DOWN_BRA = [0x21,0x21,0x3F] # 6 x 3
is_cur_num_move = False

def update_navigate():
    global cur_ind, is_cur_num_move
    ind = cur_ind
    
    if ind == 4:
        if is_cur_num_move:
            oled_nevigate.setButtonIcon(0, oled_nevigate.Icon.CONFIRM)
            oled_nevigate.clearIcon(1)
        is_cur_num_move = False
    else:
        if not is_cur_num_move:
            oled_nevigate.setButtonIcon(0, oled_nevigate.Icon.UP)
            oled_nevigate.setButtonIcon(1, oled_nevigate.Icon.DOWN)  
            
        is_cur_num_move = True

def update_code():
    global cur_code, cur_ind
    
    ind = cur_ind
    
    # clear code area
    oled_lcd.delRect(0, 30, 59, 50)
    for i in range(4):
        oled_lcd.text(str(cur_code[i]), 2 + 10 * i, 36)
    if ind == 4:
        oled_lcd.insertPixelImage(UP_BRA, 2 + 1 + 45, 30, 6, 3)
        oled_lcd.insertPixelImage(DOWN_BRA, 2 + 1 + 45, 46, 6, 3)
    else:
        oled_lcd.insertPixelImage(UP_ARROW, 2 + 1 + 10 * ind, 30, 6, 3)
        oled_lcd.insertPixelImage(DOWN_ARROW, 2 + 1 + 10 * ind, 46, 6, 3)
    oled_lcd.text("ok", 2 + 40, 36 - 1)
    update_navigate()
    oled_lcd.show()

def main():
    global FRAME_RATE, cur_code, cur_ind
    
    oled_lcd.clear()
    oled_lcd.textInLine("Rd. 2/3", 0, 0)
    oled_lcd.textInLine("Normal", 0, 1)
    
    oled_nevigate.reset()
    oled_nevigate.setButtonIcon(2, oled_nevigate.Icon.LEFT)
    oled_nevigate.setButtonIcon(3, oled_nevigate.Icon.RIGHT)
    
    c = art.getEasy()
    oled_lcd.insertPixelImage(c.convert_to_int32_array(), 60, 0, c.width, c.height, True)

    update_code()

    time_counter.reset()
    time_limit = game_settings.number_of_stage * 15 * 60 # 10 minute per round
    pTime = time_ns()
    while time_counter.time_use < time_limit:
        if(button.is_first_press(0)): # up
            if cur_ind == 4:
                #TODO: submit
                return
            else:
                cur_code[cur_ind] = (cur_code[cur_ind] + 1) % 10
                update_code()
            

        if(button.is_first_press(1)): # down
            if cur_ind != 4:
                cur_code[cur_ind] = (cur_code[cur_ind] - 1) % 10
                update_code()
        
        if(button.is_first_press(2)): # left
            cur_ind = max(cur_ind - 1, 0)
            update_code()
        

        if(button.is_first_press(3)): # right
            cur_ind = min(cur_ind + 1, 4)
            update_code()
        
        
        # decrease the time, disp and wait
        time_counter.count_tick_time( 1 / FRAME_RATE)
        button.clock_tick(1 / FRAME_RATE)
        cTime = time_ns()
        dTime = cTime - pTime
        pTime = cTime
        sleep(max((1 / FRAME_RATE) - (dTime / 10000000000), 0))
    
    print("Time's up!")

if __name__ == "__main__":
    main()
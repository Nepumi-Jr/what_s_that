from src.service import time_counter, button, oled_lcd, oled_nevigate, score_board
from src import game_settings
from src.util import log
from src.service import art_set as art
from src.service import main_game_service as game_service
from src.service.scene import SCENE as scene
from src.hardware import four_digit_disp
from time import sleep, time_ns



FRAME_RATE = 30

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

# scene
def main():
    global FRAME_RATE, cur_code, cur_ind, is_cur_num_move
    
    # reset
    cur_ind = 0
    is_cur_num_move = False
    cur_code = [
        game_service.save_pass_code // 1000,
        (game_service.save_pass_code // 100) % 10,
        (game_service.save_pass_code // 10) % 10,
        game_service.save_pass_code % 10
    ]
    
    oled_lcd.clear()
    oled_lcd.textInLine(f"Rd. {game_service.cur_round + 1}/{game_service.n_round}", 0, 0)
    oled_lcd.textInLine(game_service.cur_diff, 0, 1)
    
    oled_nevigate.reset()
    oled_nevigate.setButtonIcon(2, oled_nevigate.Icon.LEFT)
    oled_nevigate.setButtonIcon(3, oled_nevigate.Icon.RIGHT)
    
    c = game_service.get_canvas_from_CodeAndSymbol(game_service.real_code_symbol[game_service.cur_round])
    oled_lcd.insertPixelImage(c.convert_to_int32_array(), 60, 0, c.width, c.height, True)

    # for Debug
    print("Don't peak :D ", game_service.real_code_symbol[game_service.cur_round].code)

    update_code()

    time_counter.reset(game_service.save_cur_time)
    pTime = time_ns()
    while time_counter.time_use < game_service.time_limit:
        if(button.is_first_press(0)): # up
            if cur_ind == 4:
                pass_code = int("".join([str(i) for i in cur_code]))
                cur_time = time_counter.time_use

                result_check = game_service.on_submit_pass(pass_code, cur_time)

                if result_check == game_service.OnSubmitStatus.CORRECT:
                    return scene.CORRECT
                elif result_check == game_service.OnSubmitStatus.WRONG:
                    return scene.WRONG
                else:
                    return scene.WIN
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
    
    game_service.save_cur_time = time_counter.time_use
    return scene.TIME_UP

def on_correct():
    graphic = [0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00001FC0, 0x00000000, 0x00000000, 0x00000000, 0x00003FE0, 0x00000000, 0x00000000, 0x00000000, 0x00007FF8, 0x00000000, 0x00000000, 0x00000000, 0x00007FF8, 0x00000000, 0x00000000, 0x00000060, 0x0000FFFC, 0x00070E00, 0x00600000, 0x00000060, 0x0000FFFC, 0x00039C00, 0x00600000, 0x00000060, 0x0000FE0C, 0x00039800, 0x00C00000, 0x00000060, 0x0000E00C, 0x0001B0F9, 0xC6DB9E00, 0xF0F87C60, 0x00004004, 0x0001F199, 0x861FBF03, 0x9998CCC0, 0x00004004, 0x0000E30D, 0x8C1C6303, 0x130D86C0, 0x00002008, 0x0000C30D, 0x8C187F07, 0x030D86C0, 0x00002010, 0x0000C60D, 0x8C18FF06, 0x060F06C0, 0x00002010, 0x0000C719, 0x8C18E207, 0x271B8CC0, 0x00001010, 0x0001C339, 0xFC307F03, 0x33399CC0, 0x00001010, 0x0001C1F1, 0xEC303C01, 0xE1F0F9E0, 0x00000810, 0x00000000, 0x00000000, 0x00000000, 0x00000818, 0x00000000, 0x00000000, 0x00000000, 0x00000C34, 0x00000000, 0x00000000, 0x00000000, 0x00001667, 0x80000000, 0x00000000, 0x00000000, 0x0000F3CF, 0xF8000000, 0x00000000, 0x00000000, 0x0003F1DF, 0xFE000000, 0x00000000, 0x00000000, 0x000FE8FF, 0xFE000000, 0x00000000, 0x00000000, 0x001FE78F, 0xFF000000, 0x00000000, 0x00000000, 0x001FE08F, 0xFF000000, 0x00000000, 0x00000000, 0x001FE18F, 0xFF000001, 0xF0000000, 0x08400000, 0x001FE18F, 0xFF800002, 0x10000000, 0x08400000, 0x003FF18F, 0xFF800006, 0x018948C1, 0x9E400000, 0x003FF19F, 0xFF800004, 0x064E7326, 0x48C00000, 0x003FF19F, 0xFF800004, 0x04284224, 0x08800000, 0x003FF99F, 0xFFC00004, 0x0C2847EC, 0x10800000, 0x007FFDBF, 0xFFC00004, 0x0C684608, 0x10000000, 0x007FFDFF, 0xFFC00004, 0x2448424C, 0x90800000, 0x007FFFFF, 0xFFC00003, 0xC79083E7, 0xDD800000, 0x007FFFFF, 0xFFC00000, 0x00000000, 0x00000000, 0x007FFFFF, 0xE7E00000, 0x00000000, 0x00000000, 0x00FDF9FF, 0xE7E00000, 0x00000000, 0x00000000, 0x00FDC0FF, 0xE7E00000, 0x00000000, 0x00000000, 0x00FC80FF, 0xE3F00000, 0x00000000, 0x00000000]
    oled_lcd.clear()
    oled_lcd.insertPixelImage(graphic, 0, 5, 128, 40, True)
    
    oled_nevigate.reset()
    oled_nevigate.setWait()
    sleep(5)
    return scene.MAIN_GAME



def on_wrong():
    graphic = [0x00000000, 0x00000000, 0x00000000, 0x00000017, 0x00000000, 0x00000000, 0x00000000, 0x000000E3, 0x00000000, 0x00000000, 0x00000000, 0x000003C1, 0x00000000, 0x00000000, 0x00000000, 0x00000780, 0x00000000, 0x0000F800, 0x00000000, 0x00000E00, 0x319BE1F1, 0x8C7CFF80, 0x00000000, 0x00001C00, 0x33927339, 0x8CC68FFC, 0x0000003F, 0x0000F800, 0x33B6361B, 0xCD80803F, 0xE0000061, 0xC007E000, 0x37B6361B, 0xCD808000, 0x7FE00060, 0x7FFF8000, 0x15E7E41B, 0x693C8000, 0x00700060, 0x0FFC0000, 0x1CE7C41B, 0x790C8000, 0x00180040, 0x00000000, 0x1CE66633, 0x3B0C8000, 0x00180040, 0x00000000, 0x18C46772, 0x399CC000, 0x00380040, 0x00000000, 0x18CC63C6, 0x18F8FC00, 0x003C0040, 0x00000000, 0x00000000, 0x00007FC0, 0x001C0060, 0x00000C80, 0x00000000, 0x000003C0, 0x00060060, 0x00001860, 0x00000000, 0x00000060, 0x00030060, 0xF8003230, 0x00000000, 0x00000060, 0x00070061, 0x8C006798, 0x00000000, 0x00000060, 0x80FF8063, 0x06006D98, 0x00000000, 0x00000070, 0x0181C062, 0xFB0058C8, 0x00000000, 0x0000003E, 0x0278E067, 0x990058E8, 0x00000000, 0x00000007, 0x0D8C3067, 0x9D00502C, 0x00000000, 0x00000001, 0x3E001827, 0x0780502C, 0x00000000, 0x00000001, 0x60000C27, 0x0780582C, 0x00000000, 0x00000001, 0x80000627, 0x87804C68, 0x00000000, 0x00000001, 0x80000332, 0xC7006FD8, 0x00000000, 0x00000000, 0x800000F3, 0x7B7E37B0, 0x00000000, 0x00000000, 0x80000001, 0x87FF3870, 0x00000000, 0x00000000, 0x80000000, 0xCF001CC0, 0x00000000, 0x00000000, 0xC0000000, 0x7B008800, 0x00000000, 0x00000000, 0x70000000, 0x01010000, 0x00000000, 0x00000000, 0x1FF80000, 0x01830000, 0x00000000, 0x00000000, 0x00C70000, 0x00860000, 0x00000000, 0x00000000, 0x00018000, 0x00D80000, 0x00000000, 0x00000000, 0x00008000, 0x00700000, 0x00000000, 0x00000000, 0x0000C000, 0x00000000, 0x00000000, 0x00000000, 0x0000C000, 0x00000000, 0x00000000, 0x00000000, 0x00007000, 0x00000000, 0x00000000, 0x00000000, 0x00001800, 0x00000000, 0x00000000, 0x00000000, 0x00001C00, 0x00000000]
    oled_lcd.clear()
    oled_lcd.insertPixelImage(graphic, 0, 5, 128, 40)
    oled_lcd.text(f"+{int(game_service.wrong_penalty /60)} min", 2, 30, reload=True)
    
    oled_nevigate.reset()
    oled_nevigate.setWait()
    sleep(3)
    return scene.MAIN_GAME

def on_time_up():
    graphic = [0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x01FD9827, 0xE8010CF8, 0x00000000, 0x00000000, 0x00219864, 0x08010C8C, 0x00000000, 0x00000000, 0x00219864, 0x08C10C84, 0x00000000, 0x00000000, 0x00219464, 0x01210C84, 0x00000000, 0x00000000, 0x002194A7, 0xC1010C88, 0x00000000, 0x00000000, 0x002194A4, 0x00C10CF0, 0x00000000, 0x00000000, 0x002192A4, 0x00210880, 0x00000000, 0x00000000, 0x00219324, 0x00218880, 0x00000001, 0xFFE00000, 0x00219127, 0xE3C0F080, 0x0000000F, 0xFFF80000, 0x00000000, 0x00000000, 0x0000001F, 0xFFFE0000, 0x00000000, 0x00000000, 0x0000007F, 0xFFFF0000, 0x00000000, 0x00000000, 0x0000007F, 0xFFFF8000, 0x00000000, 0x00000000, 0x000000FF, 0xFFFFC000, 0x00000000, 0x00000000, 0x000000FF, 0xFFFFC000, 0x00000000, 0x00000000, 0x000001FF, 0xFFFF6000, 0x00000000, 0x00000000, 0x000001FF, 0xFFFFE000, 0x00000000, 0x00000400, 0x0000017F, 0xFFFFE000, 0x007CC37E, 0xF8007FE0, 0x000001FF, 0xFF01E000, 0x00C44240, 0x8C01FFFC, 0x000001BF, 0xFF00E000, 0x00824640, 0x8403FFFE, 0x000001BC, 0x18006000, 0x01826440, 0x8C07FFFF, 0x00000178, 0x0F006000, 0x0182247C, 0xF807FFFF, 0x00000030, 0x0FC0E000, 0x00822440, 0x980FFFFF, 0x00000060, 0x08F1F000, 0x00823840, 0x8817FFFF, 0x80000020, 0x18FFE000, 0x00C41840, 0x8C07FFFF, 0x80000030, 0x107FC000, 0x0078187E, 0x8407FFFF, 0x00000018, 0x31FFC000, 0x00000000, 0x000FBFFF, 0x0000001C, 0xFFFFC000, 0x00000000, 0x00000EFF, 0x0000000F, 0xFFFFA000, 0x00000000, 0x0000103E, 0x00000000, 0xFFFFA000, 0x00000000, 0x00103E0C, 0x00000000, 0x7FFFE000, 0x00000000, 0x00186E0C, 0x00000000, 0x17FCC000, 0x00000000, 0x0007C618, 0x00FE0000, 0x1FE1C000, 0x00000000, 0x000387F8, 0x03FF0000, 0x0407C000, 0x00000001, 0xF803FFF0, 0x07FF8000, 0x003FC000, 0x00000003, 0xFC13FF60, 0x00E38000, 0x0FFFC000, 0x00000000, 0x2411FF40, 0x00628000, 0x01FFE000, 0x00000000, 0x14081FC0, 0x03F68000, 0x07FF6000, 0x00000001, 0xFC0CFFC0, 0x04FF8000, 0x003C7000, 0x00000000, 0x7C07FF80, 0x005B8080, 0x001E7800, 0x00000000, 0x0003FF00, 0x000301F8, 0x00007F07, 0x00000000, 0x0000FF00, 0x000703FF, 0x3FE067FF, 0x00000003, 0xF8003F00, 0x000783E7, 0xE00007CF, 0x00000000, 0xFC019F00, 0x000F83E3, 0xC0001F3F, 0x00000000, 0x07803E30, 0x000D03F3, 0xFC1FF9FF]
    oled_lcd.clear()
    oled_lcd.insertPixelImage(graphic, 0, 0, 128, 50)

    oled_nevigate.reset()
    oled_nevigate.setAllButtonIcon(oled_nevigate.Icon.CONFIRM)
    four_digit_disp.on_display(game_service.save_cur_time, True)
    while True:
        if button.is_first_press(0) or button.is_first_press(1) or button.is_first_press(2) or button.is_first_press(3):
            return scene.MENU
        button.clock_tick(1/FRAME_RATE)
        sleep(1/FRAME_RATE)

def on_win():
    oled_lcd.clear()
    oled_lcd.textInLine("<cool pic here>", oled_lcd.CenterX(), 1, oled_lcd.TextAlign.CENTER)
    oled_lcd.textInLine(game_service.cur_diff, oled_lcd.CenterX(), 3, oled_lcd.TextAlign.CENTER)

    oled_nevigate.reset()
    oled_nevigate.setAllButtonIcon(oled_nevigate.Icon.CONFIRM)

    timeMin = int(game_service.save_cur_time / 60)
    timeSec = int(game_service.save_cur_time % 60)
    oled_lcd.text(f"{timeMin:02d}:{timeSec:02d}", oled_lcd.width() - 1, 40, oled_lcd.TextAlign.CENTER)
    oled_lcd.text("min.", 125, 40, oled_lcd.TextAlign.RIGHT, reload=True)

    four_digit_disp.on_display(game_service.save_cur_time, True)
    while True:
        if button.is_first_press(0) or button.is_first_press(1) or button.is_first_press(2) or button.is_first_press(3):
            if score_board.is_new_record(game_service.cur_diff, game_service.save_cur_time):
                return scene.NEW_RECORD
            return scene.MENU
        button.clock_tick(1/FRAME_RATE)
        sleep(1/FRAME_RATE)

def new_record():
    oled_lcd.clear()

    timeMin = int(game_service.save_cur_time / 60)
    timeSec = int(game_service.save_cur_time % 60)
    oled_lcd.textInLine(game_service.cur_diff, oled_lcd.width() - 1, 0, oled_lcd.TextAlign.RIGHT)
    oled_lcd.text(f"{timeMin:02d}:{timeSec:02d}", 0, 0)
    oled_lcd.textInLine("<cool pic here>", oled_lcd.CenterX(), 2, oled_lcd.TextAlign.CENTER)
    oled_lcd.textInLine("Team : ", 0, 4, reload=True)

    oled_nevigate.reset()
    oled_nevigate.setButtonIcon(0, oled_nevigate.Icon.UP)
    oled_nevigate.setButtonIcon(1, oled_nevigate.Icon.DOWN)
    oled_nevigate.setButtonIcon(2, oled_nevigate.Icon.LEFT)
    oled_nevigate.setButtonIcon(3, oled_nevigate.Icon.RIGHT)

    ALPHABET = " ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!?"
    cur_team_ind = [0 for i in range(5)]
    cur_pos_ind = 0
    is_move_to_end = False
    
    def update_team_name():
        nonlocal is_move_to_end
        oled_lcd.delRect(59, 36, 127, 52)
        for i in range(5):
            oled_lcd.text(ALPHABET[cur_team_ind[i]], 58 + 10 * i,  40)
        oled_lcd.insertPixelImage(UP_ARROW, 1 + 58 + 10 * cur_pos_ind, 36, 6, 3)
        oled_lcd.insertPixelImage(DOWN_ARROW, 1 + 58 + 10 * cur_pos_ind, 49, 6, 3)
        oled_lcd.show()

        if cur_pos_ind == 4:
            if not is_move_to_end:
                oled_nevigate.setButtonIcon(3, oled_nevigate.Icon.CONFIRM)
                is_move_to_end = True
        else:
            if is_move_to_end:
                oled_nevigate.setButtonIcon(3, oled_nevigate.Icon.RIGHT)
                is_move_to_end = False
    update_team_name()

    while True:
        if button.is_first_press(0) or button.is_hold(0):
            cur_team_ind[cur_pos_ind] = (cur_team_ind[cur_pos_ind] + 1) % len(ALPHABET)
            update_team_name()
        elif button.is_first_press(1) or button.is_hold(1):
            cur_team_ind[cur_pos_ind] = (cur_team_ind[cur_pos_ind] - 1) % len(ALPHABET)
            update_team_name()
        elif button.is_first_press(2):
            cur_pos_ind = max(cur_pos_ind - 1, 0)
            update_team_name()
        elif button.is_first_press(3):
            if cur_pos_ind == 4:
                team_name = "".join([ALPHABET[i] for i in cur_team_ind]).strip()
                score_board.add_new_record(game_service.cur_diff, team_name, game_service.save_cur_time)
                #TODO : Return to score board...
                return scene.MENU
            cur_pos_ind = min(cur_pos_ind + 1, 4)
            update_team_name()
        button.clock_tick(1/FRAME_RATE)
        sleep(1/FRAME_RATE)




if __name__ == "__main__":
    game_service.cur_diff = game_service.Difficulty.EASY
    game_service.save_cur_time = 2 * 60 + 42
    new_record()




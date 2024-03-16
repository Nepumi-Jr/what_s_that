from src.service import time_counter, button, oled_lcd, oled_nevigate, score_board
from src.service import main_game_service as game_service
from src.service.scene import SCENE as scene
from src.service import sound_trigger as sound
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
    if game_service.cur_diff == game_service.Difficulty.SILENT:
        oled_lcd.text(f"Rd. {game_service.cur_round + 1}/{game_service.n_round}", 0, 5)
        oled_lcd.text(game_service.cur_diff, 0, 15)
    else:
        oled_lcd.text(f"Rd. {game_service.cur_round + 1}/{game_service.n_round}", 0, 0)
        oled_lcd.text(game_service.cur_diff, 0, 10)
    
    oled_nevigate.reset()
    oled_nevigate.setButtonIcon(2, oled_nevigate.Icon.LEFT)
    oled_nevigate.setButtonIcon(3, oled_nevigate.Icon.RIGHT)
    
    c = game_service.get_canvas_from_CodeAndSymbol(game_service.real_code_symbol[game_service.cur_round])
    oled_lcd.insertPixelImage(c.convert_to_int32_array(), 60, 0, c.width, c.height, True)

    # for Debug
    print("Don't peak :D ", game_service.real_code_symbol[game_service.cur_round].code)

    update_code()

    sound.reset_queue()
    time_counter.reset(game_service.save_cur_time)
    pTime = time_ns()
    pSound = 0
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
        

        if game_service.cur_diff == game_service.Difficulty.SILENT:
            MAX_SOUND = 0.3
            this_sound = round(min(sound.soundTrigger() / MAX_SOUND, 1)  * 10)
            if this_sound >= pSound:
                for i in range(pSound, this_sound):
                    oled_lcd.rect(5 * i, 0, 5 * i + 3, 3)
            else:
                for i in range(this_sound, pSound):
                    oled_lcd.delRect(5 * i, 0, 5 * i + 3, 3)
            oled_lcd.show()
            if this_sound == 10:
                pass_code = int("".join([str(i) for i in cur_code]))
                cur_time = time_counter.time_use
                game_service.on_sound_penalty(pass_code, cur_time)
                return scene.LOUD
            pSound = this_sound
            sound.reload_sound_loop()

        
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
    graphic_anime = [0x00000000, 0x00000020, 0x00000000, 0x00000020, 0x00000000, 0x00000020, 0x00000004, 0x00000020, 0x00000000, 0x00000020, 0x00000000, 0x00000020, 0x00000000, 0x00000040, 0x00000004, 0x00000020, 0x00000000, 0x00000040, 0x00000004, 0x00000010, 0x319BE1F1, 0x8C7C0040, 0x00000006, 0x00000010, 0x33927339, 0x8CC60040, 0x00000002, 0x00000010, 0x33B6361B, 0xCD800080, 0x00800002, 0x00000010, 0x37B6361B, 0xCD800080, 0x00800003, 0x00000010, 0x15E7E41B, 0x693C0080, 0x00800003, 0x20000008, 0x1CE7C41B, 0x790C0080, 0x00C00407, 0x00000008, 0x1CE66633, 0x3B0C0100, 0x00C00403, 0xE0000008, 0x18C46772, 0x399C0100, 0x00C2F79D, 0xFE000004, 0x18CC63C6, 0x18F80100, 0x03C7FFE0, 0x3E000004, 0x00000000, 0x00000100, 0x0307FFC0, 0x07000004, 0x00000000, 0x00000100, 0x0403FF80, 0x01000004, 0x00000000, 0x00000110, 0x0109FFF8, 0x34000002, 0x00000000, 0x00000210, 0x0103FFF8, 0x07000002, 0x00000000, 0x00000210, 0x0301FFFD, 0xCA000032, 0x00000000, 0x00000230, 0x07BBFFFC, 0x3A800032, 0x00000000, 0x00000230, 0x07FFFFFD, 0xFF400029, 0x00000000, 0x00000230, 0x07FFFFFB, 0xEF400029, 0x00000000, 0x00000230, 0x07FFFFF7, 0x6B400029, 0x00000000, 0x00000230, 0x03FFDFEF, 0x6B400025, 0x00000000, 0x00000230, 0x03FFDFDF, 0x0B400025, 0x00000000, 0x00000230, 0x03FFFF3F, 0x1A20004D, 0x00000000, 0x00000230, 0x01FFFE3F, 0x00F00072, 0x00000000, 0x00000228, 0x01FFFC1F, 0x03E00044, 0x00000000, 0x00000228, 0x01FFFC0F, 0x03800008, 0x00000000, 0x00000224, 0x00FFFC06, 0x07000010, 0x00000000, 0x00000224, 0x007FF802, 0x06000008, 0x00000000, 0x00000122, 0x003FE000, 0x04000008, 0x00000000, 0x00000122, 0x001FF000, 0x00000008, 0x00000000, 0x00000092, 0x000FE000, 0x00000008, 0x00000000, 0x0000004C, 0x00030000, 0x00000008, 0x00000000, 0x00000020, 0x00000000, 0x00000008, 0x00000000, 0x00000040, 0x00000000, 0x00000004, 0x00000000, 0x00000040, 0x00000000, 0x10000004, 0x00000000, 0x00000040, 0x00000000, 0x00000002, 0x00000000, 0x00000080, 0x00000000, 0x00000002]
    oled_lcd.clear()
    if game_service.cur_diff == game_service.Difficulty.EASY:
        oled_lcd.insertPixelImage(graphic_anime, 0, 5, 128, 40)
    else:
        oled_lcd.insertPixelImage(graphic, 0, 5, 128, 40)
    oled_lcd.text(f"+{int(game_service.wrong_penalty /60)} min", 2, 30, reload=True)
    
    oled_nevigate.reset()
    oled_nevigate.setWait()
    sleep(3)
    return scene.MAIN_GAME

def on_loud():
    graphic = [0x78000000, 0x0F000000, 0x00000000, 0x00000000, 0x3C000000, 0x0F000000, 0x00000000, 0x00000000, 0x0F000000, 0x1F000000, 0x00000000, 0x00000000, 0x07C00000, 0x7F000000, 0x00000000, 0x00000000, 0x01C00000, 0x76000000, 0x00000000, 0x00000000, 0x00FFFF80, 0xE60007D7, 0xE07EFFEF, 0xCFBFF380, 0x007FFFFC, 0xCE000C33, 0xC03C7863, 0xC737B380, 0x000000FF, 0xCC001C13, 0xC03C7923, 0xE2279380, 0x00800007, 0x8C001F03, 0xC03C7903, 0xF2078380, 0x00600000, 0x0E000FC3, 0xC03C7F02, 0xFA078100, 0x0E180000, 0x078007F3, 0xC03C7902, 0x7A078100, 0x0F860000, 0x83C001F3, 0xC03C7902, 0x3E078100, 0x0FF10003, 0x00E01073, 0xC23C7822, 0x3E078000, 0x0FF80004, 0x00601863, 0xC63C7867, 0x1E078380, 0x0FF80000, 0xFC7017C7, 0xFE7EFFEF, 0x8E0FC380, 0x07FC0001, 0xFC300000, 0x00000000, 0x00000000, 0x01FC0003, 0xFC380000, 0x00000000, 0x00000000, 0x007C0003, 0xFC188800, 0x00004000, 0x00080002, 0x00000001, 0xF8188800, 0x00004040, 0x00080002, 0xC0000000, 0x00188811, 0x430C48F3, 0x0C08C48A, 0x300003F0, 0x00188869, 0xA4925044, 0x92092496, 0x10007FF8, 0x00188821, 0x18826048, 0x610A14A2, 0x0C007FF8, 0x00188819, 0x1F9E5048, 0x610A14A2, 0x03003FF8, 0x00188809, 0x24225044, 0x51091492, 0x00000FF0, 0x00787879, 0xE79E4877, 0x9E0DE79E, 0x000007E0, 0x07980001, 0x00000000, 0x00000000, 0x1FC00380, 0xF8180001, 0x00000000, 0x00000000, 0xE0000300, 0x00180001, 0x00000000, 0x00000000, 0x00000300, 0x00180000, 0x00000000, 0x00000000, 0x00400300, 0xFFF80000, 0x00000000, 0x00000000, 0x0F800300, 0x00300000, 0x00000000, 0x00000000, 0x70000300, 0x40300000, 0x00000000, 0x00000000, 0x80000300, 0x3C700000, 0x00000000, 0x00000000, 0x00000FC0, 0x03E00000, 0x00000000, 0x00000000, 0x00007FF0, 0x00E00000, 0x00000000, 0x00000000, 0x0003F87C, 0x01C00000, 0x00000000, 0x00000000, 0x0E0FC01C, 0x03800000, 0x00000000, 0x00000000, 0x300E0000, 0x03000000, 0x00000000, 0x00000000, 0xC0000000, 0x07000000, 0x00000000, 0x00000000, 0x00000000, 0x0E000000, 0x00000000, 0x00000000]
    oled_lcd.clear()
    oled_lcd.insertPixelImage(graphic, 0, 5, 128, 40)
    oled_lcd.text(f"+{int(game_service.wrong_penalty /60)} min", 48, 35, reload=True)
    
    oled_nevigate.reset()
    oled_nevigate.setWait()
    sleep(5)
    return scene.MAIN_GAME

def on_time_up():
    graphic = [0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00001800, 0x000000F0, 0x00000000, 0x00000000, 0x00002200, 0x000003F0, 0x00000000, 0x00000000, 0x00003100, 0x000007F0, 0x00000000, 0x00000000, 0x00001040, 0x00C00FF0, 0x00000000, 0x00000000, 0x00000000, 0x0F8007F0, 0x7FE30C07, 0x1FEC0006, 0x063F8808, 0xC00007F0, 0x06030C07, 0x100C0006, 0x06218803, 0x000003F0, 0x06030E07, 0x100C0006, 0x0620CC00, 0x000003F0, 0x06030E0F, 0x100C3006, 0x0620C480, 0xC00003F0, 0x06030A0B, 0x1000FC06, 0x0620C607, 0xFF0003E0, 0x06030B0B, 0x1FC08806, 0x0620C67F, 0xFFE001C0, 0x0603091B, 0x1FC0C006, 0x0623820F, 0xFFF80040, 0x06030913, 0x10007006, 0x063F020F, 0xFC1C0000, 0x060309B3, 0x10001C06, 0x06200627, 0xFC060000, 0x060308A3, 0x10000C02, 0x06200227, 0xFC420000, 0x060308A3, 0x10000403, 0x06200A17, 0xFE060000, 0x060308E3, 0x10008C03, 0x8C200F0F, 0xFF0E0000, 0x06030843, 0x1FE0F801, 0xF82007FF, 0xFEEC3000, 0x00000000, 0x00000000, 0x000005F8, 0x7F9C0000, 0x00000000, 0x00000000, 0x000000F0, 0x7FFC0000, 0x00000000, 0x00000000, 0x00000071, 0x7FFF0000, 0x00000000, 0x00000000, 0x000000F0, 0xFFF80000, 0x00000000, 0x00000000, 0x000003F0, 0xFFFC0004, 0x00000000, 0x00000000, 0x000001F8, 0xFFFFF804, 0x00000000, 0x00000000, 0x000003FC, 0xFFFFFC00, 0x00000000, 0x00000000, 0x000003FE, 0xFFFF0000, 0x00000000, 0x00000000, 0x000003FF, 0x3FFF8000, 0x00000000, 0x00000000, 0x000001FC, 0x13FFC000, 0x00000000, 0x00000000, 0x000000F8, 0x107E8000, 0x00000000, 0x00000000, 0x000001BC, 0x003FE180, 0x00000000, 0x00000000, 0x0000000C, 0x001FFC00, 0x0001980E, 0x01C03807, 0x00E00084, 0x0FCFFC02, 0x0001FE3F, 0x87F0FE1F, 0xC3F80042, 0x3FEFFE02, 0x0001C661, 0x8C318630, 0xC6180033, 0x3FEFFFCE, 0x00018260, 0xCC198330, 0x660C003F, 0x3FDFFFFE, 0x00018240, 0xC8190320, 0x640C007F, 0xBFBFFFFF, 0x00018240, 0xC8190320, 0x640C007F, 0xBFFFFFFF, 0x00018240, 0xC8190320, 0x640C007F, 0xFF7FFFFF, 0x00018260, 0xCC198330, 0x660C007F, 0xDEFFFFFF, 0x00018231, 0x8630C618, 0xC318007F, 0xD37FFFFF, 0x0001821F, 0x03E07C0F, 0x81F0007F, 0xFF7FFFFF, 0x00000000, 0x00000000, 0x0000007F, 0xFE7FFFFE, 0x00000000, 0x00000000, 0x0000003F, 0xC3FFFFFC, 0x00000000, 0x00000000, 0x0000003F, 0xC3FFFFF8, 0x00000000, 0x00000000, 0x0000001F, 0xE0FFFFF8, 0x00000000, 0x00000000, 0x0000001F, 0xE07FFFF0, 0x00000000, 0x00000000, 0x0000001F, 0xE07FFFF8, 0x00000000, 0x00000000, 0x0000003F, 0xE03FFFF0, 0x00000000, 0x00000000, 0x0000001F, 0xE01FFFF0]
    graphic_hard = [0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x01FD9827, 0xE8010CF8, 0x00000000, 0x00000000, 0x00219864, 0x08010C8C, 0x00000000, 0x00000000, 0x00219864, 0x08C10C84, 0x00000000, 0x00000000, 0x00219464, 0x01210C84, 0x00000000, 0x00000000, 0x002194A7, 0xC1010C88, 0x00000000, 0x00000000, 0x002194A4, 0x00C10CF0, 0x00000000, 0x00000000, 0x002192A4, 0x00210880, 0x00000000, 0x00000000, 0x00219324, 0x00218880, 0x00000001, 0xFFE00000, 0x00219127, 0xE3C0F080, 0x0000000F, 0xFFF80000, 0x00000000, 0x00000000, 0x0000001F, 0xFFFE0000, 0x00000000, 0x00000000, 0x0000007F, 0xFFFF0000, 0x00000000, 0x00000000, 0x0000007F, 0xFFFF8000, 0x00000000, 0x00000000, 0x000000FF, 0xFFFFC000, 0x00000000, 0x00000000, 0x000000FF, 0xFFFFC000, 0x00000000, 0x00000000, 0x000001FF, 0xFFFF6000, 0x00000000, 0x00000000, 0x000001FF, 0xFFFFE000, 0x01043082, 0x18000400, 0x0000017F, 0xFFFFE000, 0x010C3086, 0x18007FE0, 0x000001FF, 0xFF01E000, 0x01085084, 0x2801FFFC, 0x000001BF, 0xFF00E000, 0x0308D184, 0x6803FFFE, 0x000001BC, 0x18006000, 0x03F891FC, 0x4807FFFF, 0x00000178, 0x0F006000, 0x02099104, 0xC807FFFF, 0x00000030, 0x0FC0E000, 0x0219F90C, 0xFC0FFFFF, 0x00000060, 0x08F1F000, 0x02130909, 0x8417FFFF, 0x80000020, 0x18FFE000, 0x06120B09, 0x0407FFFF, 0x80000030, 0x107FC000, 0x00000000, 0x0007FFFF, 0x00000018, 0x31FFC000, 0x00000000, 0x000FBFFF, 0x0000001C, 0xFFFFC000, 0x00000000, 0x00000EFF, 0x0000000F, 0xFFFFA000, 0x00000000, 0x0000103E, 0x00000000, 0xFFFFA000, 0x00000000, 0x00103E0C, 0x00000000, 0x7FFFE000, 0x00000000, 0x00186E0C, 0x00000000, 0x17FCC000, 0x00000000, 0x0007C618, 0x00FE0000, 0x1FE1C000, 0x00000000, 0x000387F8, 0x03FF0000, 0x0407C000, 0x00000001, 0xF803FFF0, 0x07FF8000, 0x003FC000, 0x00000003, 0xFC13FF60, 0x00E38000, 0x0FFFC000, 0x00000000, 0x2411FF40, 0x00628000, 0x01FFE000, 0x00000000, 0x14081FC0, 0x03F68000, 0x07FF6000, 0x00000001, 0xFC0CFFC0, 0x04FF8000, 0x003C7000, 0x00000000, 0x7C07FF80, 0x005B8080, 0x001E7800, 0x00000000, 0x0003FF00, 0x000301F8, 0x00007F07, 0x00000000, 0x0000FF00, 0x000703FF, 0x3FE067FF, 0x00000003, 0xF8003F00, 0x000783E7, 0xE00007CF, 0x00000000, 0xFC019F00, 0x000F83E3, 0xC0001F3F, 0x00000000, 0x07803E30, 0x000D03F3, 0xFC1FF9FF]
    oled_lcd.clear()

    if game_service.cur_diff == game_service.Difficulty.HARD:
        oled_lcd.insertPixelImage(graphic_hard, 0, 0, 128, 50)
    else:
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
    graphic_anime = [0xFFDEFFD8, 0x0781FEC9, 0x1F9F80FF, 0xFFF80000, 0xFFFFBFFF, 0xF80FFE81, 0x1FCF807F, 0xFFFC0000, 0xFFFFE7F3, 0xFC3FFC02, 0x1FCFE07F, 0xE80C0000, 0xFFFFFF7B, 0xFFFFFC01, 0x0FF7F01F, 0xC0020000, 0xFF7FFFFF, 0xFFFFF401, 0x0FFFFC1F, 0x80000000, 0xFC1FFFFF, 0xFFF3FA00, 0xC7FFFF07, 0x83F80000, 0xF9DFFFFF, 0xFFF3EA00, 0xE7FFFF87, 0x8FFC0000, 0xFBF060C5, 0xA420FE00, 0xF7EFFFF8, 0xFFFF0000, 0xF3F764D9, 0x9D93EC00, 0x7BBFFFFF, 0xFFFF0004, 0xF3E72E9D, 0xBE13EE00, 0x7FFCFFFF, 0xFFFF0000, 0xFBE72E9D, 0xB993EE00, 0x3FC07FFF, 0xFFFF0002, 0x79976ED9, 0xB993EE00, 0x1F003FFF, 0xFFFF8002, 0x3C306EC5, 0xBC18F400, 0x1E003FFF, 0xFFFF8006, 0xBFFFFFFD, 0xFFFFE404, 0x080FFFFF, 0xFFFF8006, 0xDFFFFFD9, 0xFFFFE200, 0x003FFFFF, 0xFFFF8004, 0xEFFFFFC3, 0xFFFFC001, 0x00FFFFEF, 0xFFFF800C, 0xF3FF9FFF, 0xC3E70001, 0x81FFFFEF, 0xFFFF800C, 0xF831BFFF, 0x81200000, 0x7BFFFFFF, 0xFFFF0018, 0xFC07FFFF, 0x03200000, 0x3FFFFFFF, 0xFFFF0019, 0xFF3FFD3C, 0x03010000, 0x1FFFFFFF, 0xF7FF0031, 0xFFFF7400, 0x02030000, 0x8FFFFFFF, 0x07FE0033, 0x7FFFD000, 0x00020010, 0xA7FFFFF8, 0x03FE0063, 0xFFFF8000, 0x00000000, 0x01FFFFC0, 0x07FC00C7, 0xDFFE0030, 0x00602000, 0x007FFF00, 0x07FC0087, 0x7FE000E0, 0x01418001, 0x001FFF00, 0xF7F8010F, 0xFFC000E0, 0x02070000, 0x0007FF81, 0xFFF0031F, 0xFF000180, 0x021C0080, 0x00FFFFC7, 0xFFF0023B, 0xFC000100, 0x01F00180, 0x803FFFEF, 0xFFC0087F, 0xF0000300, 0x5FE00180, 0x011FFFFD, 0xFFC0187F, 0x80000201, 0xFF000180, 0x408FFFFF, 0xFF0010FF]
    graphic = [0x0007E000, 0x00000000, 0x00000000, 0x0007E000, 0x000FF000, 0x00000000, 0x00000000, 0x000FF000, 0x001FFC00, 0xC37EF986, 0x0F8F87C6, 0x0C3FF800, 0x003FFE00, 0xC6409CCC, 0x18D9CCE4, 0x187FFC00, 0x003FFE00, 0x46C18CD8, 0x3030D86C, 0x187FFC00, 0x003F0600, 0x64FD8C70, 0x3030D86C, 0x1860FC00, 0x00380600, 0x6CFDF870, 0x2020D06C, 0x18601C00, 0x00100200, 0x68C1F060, 0x2020D06C, 0x18400800, 0x00100200, 0x78C19860, 0x303198CC, 0x00400800, 0x00080800, 0x30FD1860, 0x3B3B9DCF, 0x90101000, 0x00080800, 0x31FB1860, 0x1F1E0F1F, 0xB8101000, 0x00040800, 0x00000000, 0x00000000, 0x00102000, 0x00040801, 0xFFFFFFFF, 0xFFFFFFFF, 0xF8102000, 0x00020800, 0x00000000, 0x00000000, 0x00104000, 0x00020C00, 0x00000000, 0x00000000, 0x00304000, 0x00031A00, 0x00000000, 0x00000000, 0x0058C000, 0x003CE7F8, 0x007C0000, 0x00004200, 0x1FE73C00, 0x00FCEFFE, 0x00C40000, 0x00004200, 0x7FF73F00, 0x01FA7FFE, 0x00803161, 0xA518F200, 0x7FFE5F80, 0x03F9C7FE, 0x0180C992, 0x66264200, 0x7FE39FC0, 0x03F847FE, 0x01808D12, 0x24024200, 0x7FE21FC0, 0x03F8C7FE, 0x00818516, 0x243E4200, 0x7FE31FC0, 0x03F8C7FF, 0x00808516, 0x24224000, 0xFFE31FC0, 0x07FCCFFF, 0x00C48912, 0x24264200, 0xFFF33FE0, 0x07FCCFFF, 0x007C7913, 0xE43A3200, 0xFFF33FE0, 0x07FECFFF, 0x80000000, 0x20000001, 0xFFF37FE0, 0x0FFFDFFF, 0x80000000, 0x20000001, 0xFFFBFFF0, 0x0FFFFFFF, 0x80000003, 0xC0000001, 0xFFFFFFF0, 0x0FFFFFFF, 0x80000000, 0x00000001, 0xFFFFFFF0, 0x0FFFFFFF, 0x80000000, 0x00000001, 0xFFFFFFF0]

    oled_lcd.clear()
    if game_service.cur_diff == game_service.Difficulty.EASY:
        oled_lcd.insertPixelImage(graphic_anime, 0, 0, 128, 30)
    else:
        oled_lcd.insertPixelImage(graphic, 0, 0, 128, 30)
    oled_lcd.textInLine(game_service.cur_diff, oled_lcd.CenterX(), 3, oled_lcd.TextAlign.CENTER)

    oled_nevigate.reset()
    oled_nevigate.setAllButtonIcon(oled_nevigate.Icon.CONFIRM)

    timeMin = int(game_service.save_cur_time / 60)
    timeSec = int(game_service.save_cur_time % 60)
    oled_lcd.text(f"{timeMin:02d}:{timeSec:02d}", oled_lcd.CenterX(), 40, oled_lcd.TextAlign.CENTER)
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
    graphic = [0x007E0000, 0x00000000, 0x00000000, 0x00003F00, 0x00FF0000, 0x00000000, 0x00000000, 0x00007F80, 0x01FFC000, 0x00000000, 0x00000000, 0x0001FFC0, 0x03FFE031, 0x9FE330F8, 0xFCF8F8F8, 0xF8C3FFE0, 0x03FFE039, 0x983730CC, 0xC1CD9CCC, 0xCCC3FFE0, 0x03F06039, 0x983720CC, 0xC1818CCC, 0xC6C307E0, 0x0380603D, 0x9F3560CC, 0xFB0306CC, 0xC6C300E0, 0x01002037, 0x9F35E0F8, 0xFB0306F8, 0xC6C20040, 0x01002037, 0x981DE0F8, 0xC30304F8, 0xC6820040, 0x00808033, 0x981CE0CC, 0xC1818CCC, 0xC6008080, 0x00808031, 0x9F98C0CC, 0xFDCDDCCC, 0xFCC08080, 0x00408031, 0x9F98C0CE, 0xFCF8F8CE, 0xF9C08100, 0x00408000, 0x00000000, 0x00000000, 0x00008100, 0x00208000, 0x00000000, 0x00000000, 0x00008200, 0x0020C000, 0x00000000, 0x00000000, 0x00018200, 0x0031A000, 0x00000000, 0x00000000, 0x0002C600, 0x03CE7F80, 0x00000000, 0x00000000, 0x00FF39E0, 0x0FCEFFE0, 0x00000000, 0x00000000, 0x03FFB9F8, 0x1FA7FFE0, 0x00000000, 0x00000000, 0x03FFF2FC, 0x3F9C7FE0, 0x00000000, 0x00000000, 0x03FF1CFE, 0x3F847FE0, 0x00000000, 0x00000000, 0x03FF10FE, 0x3F8C7FE0, 0x00000000, 0x00000000, 0x03FF18FE]
    oled_lcd.clear()

    timeMin = int(game_service.save_cur_time / 60)
    timeSec = int(game_service.save_cur_time % 60)
    oled_lcd.textInLine(game_service.cur_diff, oled_lcd.width() - 1, 0, oled_lcd.TextAlign.RIGHT)
    oled_lcd.text(f"{timeMin:02d}:{timeSec:02d}", 0, 0)
    oled_lcd.insertPixelImage(graphic, 0, 10, 128, 22)
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
                team_name = "".join([ALPHABET[i] for i in cur_team_ind]).replace(" ", "")
                if team_name == "":
                    team_name = "NONAM"
                score_board.add_new_record(game_service.cur_diff, team_name, int(game_service.save_cur_time))
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







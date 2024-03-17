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
        button.clock_tick(1 / FRAME_RATE)
        cTime = time_ns()
        dTime = cTime - pTime
        pTime = cTime
        sleep(max((1 / FRAME_RATE) - (dTime / 10000000000), 0))
        if (translator_sync.translatorSyncEnding()):
            return scene.TRANSLATOR_RESULT

def result():
    oled_lcd.clear()
    oled_nevigate.reset()
    if(game_service.time_limit > game_service.save_cur_time):
        on_win()
    else:
        on_time_up()
        
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

if __name__ == "__main__":
    result()
    
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
            return scene.TRANSLATOR_MANU
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
            return scene.TRANSLATOR_MANU
        button.clock_tick(1/FRAME_RATE)
        sleep(1/FRAME_RATE)


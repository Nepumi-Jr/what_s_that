from src.service import oled_lcd as oled
from src.service.oled_lcd import TextAlign
from src.service import oled_nevigate as oled_nav
from src.service import uart, config, button
from src.service import main_game_service as game_service
from src.service.scene import SCENE as scene


from time import sleep
from random import randint

connectingPixel = [0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00001F80, 0x00000000, 0x00100000, 0x00000000, 0x00003040, 0x00000000, 0x00100800, 0x00000000, 0x00002000, 0x00000000, 0x00100000, 0x00000000, 0x0000200F, 0xC9E4F1E0, 0xF8383827, 0x8FE00000, 0x00002018, 0x6A351A11, 0x08100828, 0xD8200000, 0x00002010, 0x2C160A19, 0x04100830, 0x50200000, 0x00002010, 0x28140BF9, 0x00100820, 0x50200000, 0x00002010, 0x28140A01, 0x00100820, 0x50200000, 0x00003058, 0x68140A01, 0x00100820, 0x58200000, 0x00001F8F, 0xC81409F8, 0xFC0E3E20, 0x47E00000, 0x00000000, 0x00000000, 0x00000000, 0x00200000, 0x00000000, 0x00000000, 0x00000000, 0x00600000, 0x00000000, 0x00000000, 0x00000000, 0x0F800000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x003F1C00, 0x00000000, 0x00000404, 0x00000000, 0x00208400, 0x00000000, 0x00000004, 0x00000000, 0x00208400, 0x00000000, 0x24800404, 0x00000000, 0x0020841E, 0x1F9F9E00, 0x249F8C0E, 0x00000000, 0x003F0421, 0x20B02100, 0x24A08404, 0x00000000, 0x0020043F, 0x209F3F00, 0x24A08404, 0x00000000, 0x00200420, 0x21812000, 0x24A18404, 0x04040400, 0x00200420, 0x2381A000, 0x24A38404, 0x0E0E0E00, 0x00201E1F, 0x1CBE1F00, 0x1B1C9E03, 0x84040400, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000]
connectingPixel2 = [0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00001F80, 0x00000000, 0x00100000, 0x00000000, 0x00003040, 0x00000000, 0x00100800, 0x00000000, 0x00002000, 0x00000000, 0x00100000, 0x00000000, 0x0000200F, 0xC9E4F1E0, 0xF8383827, 0x8FE00000, 0x00002018, 0x6A351A11, 0x08100828, 0xD8200000, 0x00002010, 0x2C160A19, 0x04100830, 0x50200000, 0x00002010, 0x28140BF9, 0x00100820, 0x50200000, 0x00002010, 0x28140A01, 0x00100820, 0x50200000, 0x00003058, 0x68140A01, 0x00100820, 0x58200000, 0x00001F8F, 0xC81409F8, 0xFC0E3E20, 0x47E00000, 0x00000000, 0x00000000, 0x00000000, 0x00200000, 0x00000000, 0x00000000, 0x00000000, 0x00600000, 0x00000000, 0x00000000, 0x00000000, 0x0F800000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x003F1C00, 0x00000000, 0x00000404, 0x00000000, 0x00208400, 0x00000000, 0x00000004, 0x00000000, 0x00208400, 0x00000000, 0x24800404, 0x00000000, 0x0020841E, 0x1F9F9E00, 0x249F8C0E, 0x00000000, 0x003F0421, 0x20B02100, 0x24A08404, 0x00000000, 0x0020043F, 0x209F3F00, 0x24A08404, 0x00000000, 0x00200420, 0x21812000, 0x24A18404, 0x04040400, 0x00200420, 0x2381A000, 0x24A38404, 0x0E0E0E00, 0x00201E1F, 0x1CBE1F00, 0x1B1C9E03, 0x84040400, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000]

def showStatusText(msg):
    oled.textInLine(msg, oled.CenterX(), 4, TextAlign.CENTER, True)

def showError(msg):
    oled.clear(False)
    oled.text("ERROR DURING SYNC", oled.CenterX(), 10, TextAlign.CENTER, False)
    oled.text(msg, oled.CenterX(), 20, TextAlign.CENTER, False)
    oled.text("PRESS ANY TO BACK.", oled.CenterX(), 30, TextAlign.CENTER, True)
    oled_nav.setAllButtonIcon(oled_nav.Icon.BACK)


def pressAnyToReturn():
    while True:
        for i in range(button.get_button_number()):
            if button.is_first_press(i):
                return scene.TRANSLATOR_MENU
        button.clock_tick(0.03)
        sleep(0.03)

TIME_FRAME = 0.1
def translatorSyncEnding():
    read_data = uart.read()
    if read_data is not None and read_data.startswith("end"):
        game_service.save_cur_time = read_data.split(" ")[1].strip()
        return True
    else:
        return False
    
def main():
    time_out = 10
    oled.clear(False)
    oled.insertPixelImage(connectingPixel, 0, 0, 128, 40, True)
    oled_nav.reset()
    oled_nav.setWait()

    showStatusText(f"Drawing symbol.")

    showStatusText(f"Waiting resp.")
    while True:
        # TODO : add timeout
        read_data = uart.read()
        if read_data is not None and read_data.startswith("diff"):
            #diff {main_game_service.cur_diff} seed {ob_seed}
            diff = read_data.split(" ")[1].strip()
            recv_seed = int(read_data.split(" ")[3].strip())
            game_service.set_seed(recv_seed)
            #split DIFF
            game_service.set_diff_from_str(diff)
            game_service.reset_game()
            break

        if time_out < 0:
            if not is_text_changed:
                oled.insertPixelImage(connectingPixel2, 0, 0, 128, 40)
                oled.textInLine("Waiting resp.", oled.CenterX(), 3, TextAlign.CENTER)
                oled.textInLine("Hold to exit", oled.CenterX(), 4, TextAlign.CENTER, True)
                is_text_changed = True
        else:
            time_out -= TIME_FRAME
        
        if button.is_hold(0) or button.is_hold(1) or button.is_hold(2):
            return scene.TRANSLATOR_MENU

        button.clock_tick(TIME_FRAME)

        sleep(TIME_FRAME)
    
    hashed = game_service.get_hash_cur_game_setting()
    uart.send(f"hash {hashed}")
    showStatusText(f"Syncing...")
    while True:
        read_data = uart.read()
        if read_data is not None and read_data.startswith("mann"):
            uart.send(f"starto")
            return scene.TRANSLATOR_MAIN_GAME
        elif read_data is not None and read_data.startswith("not mann"):
            pressAnyToReturn()
            return scene.TRANSLATOR_MENU
        sleep(TIME_FRAME)
        
if __name__ == "__main__":
    main()
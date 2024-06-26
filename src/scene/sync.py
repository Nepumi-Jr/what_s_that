from src.service import oled_lcd as oled
from src.service.oled_lcd import TextAlign
from src.service import oled_nevigate as oled_nav
from src.service import uart, button, main_game_service
from src.service.scene import SCENE as scene
from src.service.config import get_config
from time import sleep

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
                return scene.MENU
        button.clock_tick(0.03)
        sleep(0.03)

TIME_FRAME = 0.1


def main():
    time_out = 10
    time_re_seed = 0
    is_text_changed = False
    time_send = 0

    oled.clear(False)
    oled.insertPixelImage(connectingPixel, 0, 0, 128, 40, True)
    oled_nav.reset()
    oled_nav.setWait()


    showStatusText(f"Drawing symbol.")
    ob_seed = main_game_service.set_seed()
    main_game_service.reset_game()
    main_game_service.print_cur_game_status()

    if get_config().device.skip_sync:
        showStatusText(f"Press any...")
        pressAnyToReturn()
        return scene.MAIN_GAME
    
    showStatusText(f"Waiting resp.")
    while True:
        read_data = uart.read()
        if read_data is not None and read_data.startswith("hash"):
            recv_hash = read_data.split(" ")[1].strip()
            main_hash = main_game_service.get_hash_cur_game_setting()
            print("Received hash", recv_hash, "expected", main_hash)
            if recv_hash == str(main_hash):
                showStatusText(f"Seed matched.")
                break
            else:
                showError(f"Not match :(")
                uart.send("not mann")
                pressAnyToReturn()
                return scene.MENU
        
        if time_out < 0:
            if not is_text_changed:
                oled.insertPixelImage(connectingPixel2, 0, 0, 128, 40)
                oled.textInLine("Waiting resp.", oled.CenterX(), 3, TextAlign.CENTER)
                oled.textInLine("Hold to exit", oled.CenterX(), 4, TextAlign.CENTER, True)
                is_text_changed = True
        else:
            time_out -= TIME_FRAME

        time_re_seed -= TIME_FRAME
        if time_re_seed < 0:
            uart.send(f"diff {main_game_service.cur_diff} seed {ob_seed} ")
            print("sending seed and diff", time_send, "time...")
            time_send += 1
            time_re_seed = 1
        
        if button.is_hold(0) or button.is_hold(1) or button.is_hold(2) or button.is_hold(3):
            return scene.MENU

        button.clock_tick(TIME_FRAME)
        sleep(TIME_FRAME)
    
    uart.send("mann")
    showStatusText(f"Syncing...")

    while True:
        read_data = uart.read()
        if read_data is not None and read_data.strip() == "starto":
            return scene.MAIN_GAME
        sleep(TIME_FRAME)



if __name__ == "__main__":
    main()


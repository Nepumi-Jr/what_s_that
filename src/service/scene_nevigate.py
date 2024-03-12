from src.scene import main_game, sync, menu
from src.scene import translator_main_game as translate_scene
from src.service.scene import SCENE
from src.service import config


def main():
    # start with...
    cur_scene = SCENE.MENU

    conf = config.get_config()
    if conf.device.mode == config.DeviceType.PLAY:
        while True:
            if cur_scene == SCENE.MENU:
                cur_scene = menu.main()
            elif cur_scene == SCENE.SCORE_BOARD:
                cur_scene = menu.score_board()
            elif cur_scene == SCENE.DIFFICULTY_SELECT:
                cur_scene = menu.difficulty_select()
            elif cur_scene == SCENE.SYNC:
                cur_scene = sync.main()
            elif cur_scene == SCENE.MAIN_GAME:
                cur_scene = main_game.main()
            elif cur_scene == SCENE.CORRECT:
                cur_scene = main_game.on_correct()
            elif cur_scene == SCENE.WRONG:
                cur_scene = main_game.on_wrong()
            elif cur_scene == SCENE.WIN:
                cur_scene = main_game.on_win()
            elif cur_scene == SCENE.TIME_UP:
                cur_scene = main_game.on_time_up()
            elif cur_scene == SCENE.NEW_RECORD:
                cur_scene = main_game.new_record()
            elif cur_scene == SCENE.EXIT:
                break

            else:
                raise ValueError(f"Invalid scene: {cur_scene}")
    else:
        cur_scene = SCENE.TRANSLATOR_MENU
        while True:
            if cur_scene == SCENE.TRANSLATOR_MENU:
                cur_scene = translate_scene.main() # TODO:
            elif cur_scene == SCENE.TRANSLATOR_SYNC:
                cur_scene = translate_scene.syncing()
            elif cur_scene == SCENE.TRANSLATOR_MAIN_GAME:
                cur_scene = translate_scene.translator_main_game()
            elif cur_scene == SCENE.TRANSLATOR_RESULT:
                cur_scene = translate_scene.result()
            elif cur_scene == SCENE.EXIT:
                break

            else:
                raise ValueError(f"Invalid scene: {cur_scene}")

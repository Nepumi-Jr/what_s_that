from src.scene import main_game, sync
from src.scene.translator_main_game import syncing

class SCENE:
    MENU = 0
    MAIN_GAME = 1
    SYNC = 2

    CORRECT = 3
    WRONG = 4
    WIN = 5
    TIME_UP = 6

    # Translator
    TRANSLATOR_SYNC = 7


def main():
    cur_scene = SCENE.MENU
    while True:
        if cur_scene == SCENE.MENU:
            cur_scene = main_game.main()
        elif cur_scene == SCENE.MAIN_GAME:
            cur_scene = main_game.main()
        elif cur_scene == SCENE.SYNC:
            cur_scene = sync.main()
        elif cur_scene == SCENE.CORRECT:
            cur_scene = main_game.on_correct()
        elif cur_scene == SCENE.WRONG:
            cur_scene = main_game.on_wrong()
        elif cur_scene == SCENE.WIN:
            cur_scene = main_game.on_win()
        elif cur_scene == SCENE.TIME_UP:
            cur_scene = main_game.on_time_up()
        
        elif cur_scene == SCENE.TRANSLATOR_SYNC:
            cur_scene = syncing()

        else:
            raise ValueError(f"Invalid scene: {cur_scene}")

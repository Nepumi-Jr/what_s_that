from src.scene import main_game, sync
from src.scene.translator_main_game import syncing
from src.service.scene import SCENE

def main():
    cur_scene = SCENE.MENU
    while True:
        if cur_scene == SCENE.MENU:
            cur_scene = main_game.main() # TODO:
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

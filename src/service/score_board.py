from src.service.main_game_service import Difficulty

file_name = "score_board.txt"
score_board_data = {}

is_init = False
def _load():
    global score_board_data
    with open(file_name, "r") as file:
        for l in file.readlines():
            
            line = l.strip()
            # remove comment
            if "--" in line: line = line.split("--")[0]
            if "#" in line: line = line.split("#")[0]
            line = line.strip()

            if line.startswith("=="):
                current_diff = line.replace("=", "").strip()
                score_board_data[current_diff] = []
            else:
                chunk = line.split(" ")
                if len(chunk) != 2:
                    continue
                name, time_use = l.split(" ")
                if not _isint(time_use):
                    continue

                if current_diff is None:
                    continue
                
                if current_diff not in score_board_data:
                    score_board_data[current_diff] = []
                
                score_board_data[current_diff].append((name, int(time_use)))
    
    # validate
    for diff in [Difficulty.EASY, Difficulty.NORMAL, Difficulty.HARD, Difficulty.SILENT]:
        assert diff in score_board_data, f"Missing {diff} in score_board_data"
        assert len(score_board_data[diff]) == 3, f" {diff} should have 3 records (found {len(score_board_data[diff])}"
        score_board_data[diff] = sorted(score_board_data[diff], key=lambda x: x[1])

def load_or_init():
    global is_init, score_board_data
    if is_init:
        return
    
    is_init = True
    try:
        _load()
    except Exception as e:
        print(f"Error loading score_board_data: {e}")
        print("Creaing new")
        score_board_data = {}
    else:
        return
    
    # create new
    score_board_data = {
        Difficulty.EASY : [
            ("SWIFT", 10 * 60),
            ("BLAZE", 12 * 60),
            ("SQUAD", 15 * 60)
        ],
        Difficulty.NORMAL : [
            ("PULSE", 35 * 60),
            ("PIXEL", 37 * 60),
            ("FUSE", 39 * 60),
        ],
        Difficulty.HARD : [
            ("FLEX", 40 * 60),
            ("FIRE", 42 * 60),
            ("FLASH", 45 * 60)
        ],
        Difficulty.SILENT : [ # TODO: change that later
            ("SILENT", 50 * 60),
            ("SILENT", 55 * 60),
            ("SILENT", 60 * 60)
        ]
    }
    write_score_board_data()

def get_score_board_data(diff : Difficulty):
    load_or_init()
    return score_board_data[diff]

def is_new_record(diff : Difficulty, time_use : int) -> bool:
    load_or_init()
    return time_use < score_board_data[diff][-1][1]

def add_new_record(diff : Difficulty, name : str, time_use : int):
    load_or_init()
    score_board_data[diff].append((name, time_use))
    score_board_data[diff] = sorted(score_board_data[diff], key=lambda x: x[1])
    score_board_data[diff] = score_board_data[diff][:3]
    write_score_board_data()

def write_score_board_data():
    with open(file_name, "w") as file:
        for diff in [Difficulty.EASY, Difficulty.NORMAL, Difficulty.HARD, Difficulty.SILENT]:
            file.write(f"=={diff}==\n")
            for name, time_use in score_board_data[diff]:
                file.write(f"{name} {time_use}\n")
            file.write("\n")


def _isint(txt:str) -> bool:
    try:
        int(txt)
    except:
        return False
    return True

"""Score board format

==easy==
name1 300 -- time in seconds
name2 400
name3 500

==normal==
...

"""


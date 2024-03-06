import random
from src.util import random as urandom
from src.service import art_set as art

n_round = 3
cur_round = 0
save_cur_time = 0.0 # in second
save_pass_code = 0 # in int
cur_diff = None # in Difficulty
time_limit = 0.0 # in second

real_code_symbol = [] # list of CodeAndSymbol
fake_code_symbol = [] # list of list of CodeAndSymbol

# game setting
wrong_penalty = 5.0 # in second

class OnSubmitStatus:
    CORRECT = 0
    WRONG = 1
    WIN = 2

class Difficulty:
    EASY = "Easy"
    NORMAL = "Normal"
    HARD = "Hard"
    SILENT = "Silent"

    # Custom (in future)

class CodeAndSymbol:
    def __init__(self, code : int, name : str, type : int):
        self.code = code
        self.name = name
        self.type = type
    
    def __str__(self):
        return f"Code: {self.code}, Name: {self.name}, Type: {self.type}"


def on_submit_pass(pass_code : int, time_use: float) -> OnSubmitStatus:
    global cur_round, save_cur_time, save_pass_code

    save_cur_time = time_use
    if pass_code == real_code_symbol[cur_round].code:
        save_pass_code = 0
        cur_round += 1
        if cur_round == n_round:
            return OnSubmitStatus.WIN
        else:
            return OnSubmitStatus.CORRECT
    else:
        save_pass_code = pass_code
        save_cur_time += wrong_penalty
        return OnSubmitStatus.WRONG

def reset():
    global cur_round, save_cur_time, save_pass_code, real_code_symbol, fake_code_symbol
    cur_round = 0
    save_cur_time = 0.0 # in second
    save_pass_code = 0 # in int

    real_code_symbol.clear()
    fake_code_symbol.clear()



def reset_easy():
    global n_round, save_pass_code, real_code_symbol, fake_code_symbol, wrong_penalty, cur_diff, time_limit

    reset()

    n_round = 2
    wrong_penalty = 60 * 2.0 # 2 minute

    #! TODO : Remove this
    wrong_penalty = 60 * 15.0 # 15 minute

    time_limit = 60 * 10.0 * n_round # 10 minute per round
    cur_diff = Difficulty.EASY

    #* generate symbol
    #? for easy
    #? set of symbol : easy
    #? fake symbol : use 3 symbol within 2 set of symbol (6 symbol) for each round
    for r_ind in range(n_round):
        symbols_set = list(art.easy_symbols.keys())
        urandom.shuffle(symbols_set)

        real_set = symbols_set.pop()
        fake_set = symbols_set.pop()

        allCodes = urandom.sample_int(0, 9999, 10)

        real_type_set = urandom.sample_int(0, art.easy_symbols[real_set].n_type, 3)
        real_code_symbol.append(CodeAndSymbol(allCodes[0], real_set, real_type_set[0]))

        fake_type_set =  urandom.sample_int(0, art.easy_symbols[fake_set].n_type, 3)
        fake_code_symbol_mix = [CodeAndSymbol(allCodes[0], real_set, real_type_set[0])]
        fake_code_symbol_mix.extend([CodeAndSymbol(allCodes[1 + i], fake_set, fake_type_set[i]) for i in range(3)])
        fake_code_symbol_mix.extend([CodeAndSymbol(allCodes[3 + i], real_set, real_type_set[i]) for i in range(1, 3)])
        urandom.shuffle(fake_code_symbol_mix)
        fake_code_symbol.append(fake_code_symbol_mix)






def reset_normal():
    #* generate symbol
    #? for normal
    #? set of symbol : hard
    #? fake symbol : use 3 symbol within 3 set of symbol (9 symbol) for each round
    pass

def reset_hard():
    #* generate symbol
    #? for hard
    #? set of symbol : hard
    #? fake symbol : use 5 symbol with the same set of the real, and other will use 2 symbol within 3 set of symbol (6 symbol) for each round

    pass

def get_canvas_from_CodeAndSymbol(cas : CodeAndSymbol):
    if cur_diff == Difficulty.EASY:
        return art.easy_symbols[cas.name].getCanvasFromType(cas.type)
    else:
        return art.hard_symbols[cas.name].getCanvasFromType(cas.type)

if __name__ == "__main__":
    reset_easy()
    for r in range(n_round):
        print(f"Round {r+1}")
        print("Real :", real_code_symbol[r])
        for f in fake_code_symbol[r]:
            print("fake :", f)
        print()

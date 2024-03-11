import random
from src.util import random as urandom
from src.service import art_set as art

n_round = 3
cur_round = 0
save_cur_time = 0.0 # in second
save_pass_code = 0 # in int
cur_diff = None # in Difficulty
time_limit = 0.0 # in second

cur_seed = 0

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

def set_diff_from_str(diff : str):
    global cur_diff
    if diff.lower() == "easy":
        cur_diff = Difficulty.EASY
    elif diff.lower() == "normal":
        cur_diff = Difficulty.NORMAL
    elif diff.lower() == "hard":
        cur_diff = Difficulty.HARD
    elif diff.lower() == "silent":
        cur_diff = Difficulty.SILENT
    else:
        print(f"WARNING : Unknow difficulty {diff}, set to easy.")
        cur_diff = Difficulty.EASY

class CodeAndSymbol:
    def __init__(self, code : int, name : str, type : int):
        self.code = code
        self.name = name
        self.type = type
    
    def __str__(self):
        return f"Code: {self.code}, Name: {self.name}, Type: {self.type}"
    
    def __hash__(self) -> int:
        return hash((self.code, self.name, self.type))


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

def set_seed(seed : int = -1):
    if seed == -1:
        seed = random.randint(0, 999999999)
    random.seed(seed)
    return seed

def _reset_inner_data():
    global cur_round, save_cur_time, save_pass_code, real_code_symbol, fake_code_symbol
    cur_round = 0
    save_cur_time = 0.0 # in second
    save_pass_code = 0 # in int

    real_code_symbol.clear()
    fake_code_symbol.clear()



def _reset_easy():
    global n_round, save_pass_code, real_code_symbol, fake_code_symbol, wrong_penalty, cur_diff, time_limit

    n_round = 2
    wrong_penalty = 60 * 2.0 # 2 minute
    time_limit = 60 * 10.0 * n_round # 10 minute per round

    #* generate symbol
    #? for easy
    #? 2 round
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


def _reset_normal():

    e_n_round = 2
    h_n_round = 1
    n_round = e_n_round + h_n_round
    wrong_penalty = 60 * 3.0 # 3 minute
    time_limit = 60 * 15.0 * n_round # 15 minute per round

    #* generate symbol
    #? for normal
    #? 3 round
    #? set of symbol : easy 2 round, hard 1 round
    #? fake symbol : use 3 symbol within 3 set of symbol (9 symbol) for each round
    for r_ind in range(e_n_round):
        symbols_set = list(art.easy_symbols.keys())
        urandom.shuffle(symbols_set)

        real_set = symbols_set.pop()
        fake_sets = [symbols_set.pop() for _ in range(2)]

        allCodes = urandom.sample_int(0, 9999, 12)

        real_type_set = urandom.sample_int(0, art.easy_symbols[real_set].n_type, 3)
        real_code_symbol.append(CodeAndSymbol(allCodes[-1], real_set, real_type_set[0]))
        
        fake_code_symbol_mix = []
        fake_code_symbol_mix.extend([CodeAndSymbol(allCodes.pop(), real_set, real_type_set[i]) for i in range(0, 3)])
        for fake_set in fake_sets:
            fake_type_set =  urandom.sample_int(0, art.easy_symbols[fake_set].n_type, 3)
            fake_code_symbol_mix.extend([CodeAndSymbol(allCodes.pop(), fake_set, fake_type_set[i]) for i in range(3)])
            
        urandom.shuffle(fake_code_symbol_mix)
        fake_code_symbol.append(fake_code_symbol_mix)
    
    for r_ind in range(h_n_round):
        symbols_set = list(art.hard_symbols.keys())
        urandom.shuffle(symbols_set)

        real_set = symbols_set.pop()
        fake_sets = [symbols_set.pop() for _ in range(2)]

        allCodes = urandom.sample_int(0, 9999, 12)

        real_type_set = urandom.sample_int(0, art.hard_symbols[real_set].n_type, 3)
        real_code_symbol.append(CodeAndSymbol(allCodes[-1], real_set, real_type_set[0]))
        
        fake_code_symbol_mix = []
        fake_code_symbol_mix.extend([CodeAndSymbol(allCodes.pop(), real_set, real_type_set[i]) for i in range(0, 3)])
        for fake_set in fake_sets:
            fake_type_set =  urandom.sample_int(0, art.hard_symbols[fake_set].n_type, 3)
            fake_code_symbol_mix.extend([CodeAndSymbol(allCodes.pop(), fake_set, fake_type_set[i]) for i in range(3)])
            
        urandom.shuffle(fake_code_symbol_mix)
        fake_code_symbol.append(fake_code_symbol_mix)

def _reset_hard():

    n_round = 3
    wrong_penalty = 60 * 4.0 # 4 minute
    time_limit = 60 * 15.0 * n_round # 15 minute per round

    #* generate symbol
    #? for hard
    #? set of symbol : hard
    #? fake symbol : use 5 symbol with the same set of the real, and other will use 2 symbol within 3 set of symbol (6 symbol) for each round
    
    for r_ind in range(n_round):
        symbols_set = list(art.hard_symbols.keys())
        urandom.shuffle(symbols_set)

        real_set = symbols_set.pop()
        fake_sets = [symbols_set.pop() for _ in range(3)]

        allCodes = urandom.sample_int(0, 9999, 15)

        real_type_set = urandom.sample_int(0, art.hard_symbols[real_set].n_type, 5)
        real_code_symbol.append(CodeAndSymbol(allCodes[-1], real_set, real_type_set[0]))
        
        fake_code_symbol_mix = []
        fake_code_symbol_mix.extend([CodeAndSymbol(allCodes.pop(), real_set, real_type_set[i]) for i in range(0, 5)])
        for fake_set in fake_sets:
            fake_type_set =  urandom.sample_int(0, art.hard_symbols[fake_set].n_type, 2)
            fake_code_symbol_mix.extend([CodeAndSymbol(allCodes.pop(), fake_set, fake_type_set[i]) for i in range(2)])
            
        urandom.shuffle(fake_code_symbol_mix)
        fake_code_symbol.append(fake_code_symbol_mix)


def reset_game():
    global cur_diff
    _reset_inner_data()

    if cur_diff == Difficulty.EASY:
        _reset_easy()
    elif cur_diff == Difficulty.NORMAL:
        _reset_normal()
    elif cur_diff == Difficulty.HARD:
        _reset_hard()
    else:
        print("WARNING : Difficulty not set")
        cur_diff = Difficulty.EASY
        _reset_easy()

def get_canvas_from_CodeAndSymbol(cas : CodeAndSymbol):
    if cur_diff == Difficulty.EASY:
        return art.easy_symbols[cas.name].getCanvasFromType(cas.type)
    else:
        return art.hard_symbols[cas.name].getCanvasFromType(cas.type)

def get_hash_cur_game_setting():
    hh = hash("Meow")
    for r_ind in range(n_round):
        for sym in fake_code_symbol[r_ind]:
            hh ^= hash(sym)
    
    return hh

if __name__ == "__main__":
    reset_easy()
    for r in range(n_round):
        print(f"Round {r+1}")
        print("Real :", real_code_symbol[r])
        for f in fake_code_symbol[r]:
            print("fake :", f)
        print()

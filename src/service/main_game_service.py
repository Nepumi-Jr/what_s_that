import random
from src.service import art_set as art

n_round = 3
cur_round = 0
save_cur_time = 0.0 # in second
save_pass_code = 0 # in int

real_code_symbol = [] # list of CodeAndSymbol
fake_code_symbol = [] # list of list of CodeAndSymbol

# game setting
wrong_penalty = 5.0 # in second

class OnSubmitStatus:
    CORRECT = 0
    WRONG = 1
    WIN = 2

class CodeAndSymbol:
    def __init__(self, code : int, name : str, type : int):
        self.code = code
        self.name = name
        self.type = type


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

def reset_easy():
    global n_round, cur_round, save_cur_time, save_pass_code, real_code_symbol, fake_code_symbol, wrong_penalty

    n_round = 2
    cur_round = 0
    save_cur_time = 0.0 # in second
    save_pass_code = 0 # in int
    wrong_penalty = 60 * 2.0

    #* generate symbol
    #? for easy
    #? set of symbol : easy
    #? fake symbol : use 3 symbol within 2 set of symbol (6 symbol) for each round
    for r_ind in range(n_round):
        symbols_set = list(art.easy_symbols.keys())
        print(symbols_set)
        shuffle(symbols_set)

        real_set = symbols_set.pop()
        fake_set = symbols_set.pop()

        # TODO: use util random
        allCodes = []
        while allCodes < 3 * 2:
            c = random.randint(0, 9999)
            if c not in allCodes:
                allCodes.append(c)

        real_set_ids = [ CodeAndSymbol(allCodes.pop(), real_set, i) for i in range(art.easy_symbols[real_set].n_type)]
        shuffle(real_set_ids)
        real_code_symbol.append(real_set_ids.pop())

        fake_set_ids =  [ CodeAndSymbol(allCodes.pop(), fake_set, i) for i in range(art.easy_symbols[fake_set].n_type)]
        shuffle(fake_set_ids)
        fake_code_symbol_mix = [real_code_symbol[-1]]
        fake_code_symbol_mix.extend(fake_set_ids[:3])
        fake_code_symbol_mix.extend(real_set_ids[:2])
        shuffle(fake_code_symbol_mix)
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

if __name__ == "__main__":
    reset_easy()
    print(real_code_symbol)
    print(fake_code_symbol)
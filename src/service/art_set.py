# import art here
from src.service.arts import pushing_boulder, flower, eight_segment, flower_hard, sixteen_segment
from src.service.art_canvas import Canvas
from random import randint, choice

class Symbol:
    def __init__(self, symbolName : str, n_type : int, getCanvasFromType):
        self.symbolName = symbolName
        self.n_type = n_type
        self.getCanvasFromType = getCanvasFromType


easy_symbols = {
    "pushing_boulder" : Symbol("pushing_boulder", pushing_boulder.n_type, pushing_boulder.get),
    "flower" : Symbol("flower", flower.n_type, flower.get),
    "8-seg" : Symbol("8-Seg", eight_segment.n_type, eight_segment.get)
}

hard_symbols = {
    "pushing_boulder" : Symbol("pushing_boulder", pushing_boulder.n_type, pushing_boulder.get), #! remove this later
    "flower" : Symbol("flower", flower_hard.n_type, flower_hard.get),
    "16-seg" : Symbol("16-Seg", sixteen_segment.n_type, sixteen_segment.get)
}

def getRandomCanvas() -> Canvas:
    """เอาไว้ทดสอบ เฉย ๆ"""
    if randint(0, 1) == 0:
        symbol = choice(list(easy_symbols.values()))
    else:
        symbol = choice(list(hard_symbols.values()))
    
    return symbol.getCanvasFromType(randint(0, symbol.n_type - 1))
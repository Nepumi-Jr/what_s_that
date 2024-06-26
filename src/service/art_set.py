# import art here
from src.service.arts import pushing_boulder, flower, flower_hard4, flower_hard5, flower_hard6, eight_segment, cato, cato_hard, arrow, three_alpha, two_thai_alpha
from src.service.arts import sixteen_segment4, sixteen_segment5, sixteen_segment6, sixteen_segment7
from src.service.art_canvas import Canvas
from random import randint, choice

class Symbol:
    def __init__(self, symbolName : str, n_type : int, getCanvasFromType):
        self.symbolName = symbolName
        self.n_type = n_type
        self.getCanvasFromType = getCanvasFromType

silent_symbols = {
    "three_alpha" : Symbol("three_alpha", three_alpha.n_type, three_alpha.get),
    "two_thai_alpha": Symbol("two_thai_alpha", two_thai_alpha.n_type, two_thai_alpha.get)
}

easy_symbols = {
    "arrow" : Symbol("arrow", arrow.n_type, arrow.get),
    "pushing_boulder" : Symbol("pushing_boulder", pushing_boulder.n_type, pushing_boulder.get),
    "flower" : Symbol("flower", flower.n_type, flower.get),
    "8-seg" : Symbol("8-Seg", eight_segment.n_type, eight_segment.get),
    "cat" : Symbol("cat", cato.n_type, cato.get)
}

hard_symbols = {
    "cat_hard" : Symbol("cat_hard", cato_hard.n_type, cato_hard.get),
    "flower_hard4" : Symbol("flower_hard4", flower_hard4.n_type, flower_hard4.get),
    "flower_hard5" : Symbol("flower_hard5", flower_hard5.n_type, flower_hard5.get),
    "flower_hard6" : Symbol("flower_hard6", flower_hard6.n_type, flower_hard6.get),
    "16-seg4" : Symbol("16-Seg4", sixteen_segment4.n_type, sixteen_segment4.get),
    "16-seg5" : Symbol("16-Seg5", sixteen_segment5.n_type, sixteen_segment5.get),
    "16-seg6" : Symbol("16-Seg6", sixteen_segment6.n_type, sixteen_segment6.get),
    "16-seg7" : Symbol("16-Seg7", sixteen_segment7.n_type, sixteen_segment7.get)
} #! ชื่อใน dict (ทั้ง easy และ hard) ต้องไม่ซ้ำกัน

def getRandomCanvas() -> Canvas:
    """เอาไว้ทดสอบ เฉย ๆ"""
    if randint(0, 1) == 0:
        symbol = choice(list(easy_symbols.values()))
    else:
        symbol = choice(list(hard_symbols.values()))
    
    return symbol.getCanvasFromType(randint(0, symbol.n_type - 1))
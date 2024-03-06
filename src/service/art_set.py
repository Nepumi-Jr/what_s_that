# import art here
from src.service.arts import pushing_boulder, flower

class Symbol:
    def __init__(self, symbolName : str, n_type : int, getCanvasFromType):
        self.symbolName = symbolName
        self.n_type = n_type
        self.getCanvasFromType = getCanvasFromType


easy_symbols = {
    "pushing_boulder" : Symbol("pushing_boulder", pushing_boulder.n_type, pushing_boulder.get),
    "flower" : Symbol("flower", flower.n_type, flower.get),
}

hard_symbols = {
}
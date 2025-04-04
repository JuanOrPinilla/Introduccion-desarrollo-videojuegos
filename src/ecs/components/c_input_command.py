from enum import Enum


class CInputCommand:
    def __init__(self, name:str, key:int)-> None:
        self.name = name
        self.key = key
        self.phase = CommandPhase.NA
        
class CommandPhase(Enum):
    NA = 0 #No aplicable
    START = 1 #que comienza cuando se hace un accion
    END = 2
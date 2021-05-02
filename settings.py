from enum import Enum

COLOR_BLUE = "\x1b[1;36m"  # X Color

COLOR_RED = "\x1b[1;31m"  # O Color

COLOR_RESET = "\x1b[0m"  # Reset Color

REWARD_WIN = 1
REWARD_LOSS = -100
REWARD_TIE = 0


class AIType(Enum):
    MinMax = 1
    MCTs = 2
    TensorFlow = 3

class Settings:
    def __init__(self):
        # Global Settings
        self._blank_val = '-'
        self._o_val = 'O'
        self._x_val = 'X'
        self._tie_val = 'T'
        # Board Settings
        self._board_size = 5
        self._board_win_length = 4
        # AI Settings
        self._AI_recursion_depth = 5
        self._ai_one = AIType.MinMax
        self._ai_two = AIType.MCTs

    # Set Functions
    def setBlankVal(self, blankval):
        self._blank_val = blankval

    def setOVal(self, oval):
        self._o_val = oval

    def setXVal(self, xval):
        self._x_val = xval

    def setTieVal(self, tieval):
        self._tie_val = tieval

    def setBoardSize(self, boardsize):
        self._board_size = boardsize

    def setWinLength(self, winlength):
        self._board_win_length = winlength

    def setRecursionDepth(self, recursion):
        self._AI_recursion_depth = recursion

    # Get Functions
    def getBlankVal(self):
        return self._blank_val

    def getOVal(self):
        return self._o_val

    def getXVal(self):
        return self._x_val

    def getTieVal(self):
        return self._tie_val

    def getBoardSize(self):
        return self._board_size

    def getWinLength(self):
        return self._board_win_length

    def getRecursionDepth(self):
        return self._AI_recursion_depth

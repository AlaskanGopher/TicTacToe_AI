from settings import Settings

gameSettings = Settings()


class Move:
    def __init__(self, x=int(), y=int(), score=int()):
        self.x = x
        self.y = y
        self.score = score


class Board:
    # Variables
    def __init__(self):
        self.board_size = gameSettings.getBoardSize()
        self.board_win_length = gameSettings.getWinLength()

        self.blank_val = gameSettings.getBlankVal()
        self.o_val = gameSettings.getOVal()
        self.x_val = gameSettings.getXVal()
        self.tie_val = gameSettings.getTieVal()

        self.board = [[self.blank_val for x in range(self.board_size)] for y in range(self.board_size)]

        self.moves = 0
    # Set Functions
    def addState(self, x, y, player):
        self.board[x][y] = player

    def addState_flat(self, i, player):
        self.board[int(i / 5)][int(i % 5)] = player

    def addBoard(self, list):
        for x in range(0, self.board_size):
            for y in range(0, self.board_size):
                self.board[x][y] = list[x][y]

    def addBoard_flat(self, list):
        for i in range(0, self.board_size):
            self.board[int(i / 5)][int(i % 5)] = list[i]

    # Get Functions
    def getState(self, x, y):
        return self.board[x][y]

    def getState_flat(self, i):
        return self.board[int(i / 5)][int(i % 5)]

    def getBoard(self):
        return self.board[self.board_size][self.board_size]

    def getBoard_flat(self):
        flatBoard = []
        for x in range(self.board_size):
            for y in range(self.board_size):
                flatBoard.append(self.board[x][y])
        return flatBoard

    def getSize(self):
        return len(self.board)

    def validMove(self, x, y):
        return self.board[x][y] == self.blank_val and self.validBounds(x, y)

    def validBounds(self, x, y):
        if x < 0 or y < 0 or x >= self.board_size or y >= self.board_size:
            return False
        return True

    def isFull(self):
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.board[x][y] == self.blank_val:
                    return False
        return True

    def isVict(self):
        xbases = [ 0, 0, 0, self.board_size - 1 ]
        ybases = [ 0, 0, 0, 0 ]
        xdirections = [ 1, 1, 1, -1 ]
        xlengths = [ self.board_size - self.board_win_length + 1,
                    self.board_size,
                    self.board_size - self.board_win_length + 1,
                    self.board_size - self.board_win_length + 1 ]
        ylengths = [ self.board_size,
                   self.board_size - self.board_win_length + 1,
                   self.board_size - self.board_win_length + 1,
                   self.board_size - self.board_win_length + 1 ]
        xmods = [ 1, 0, 1, -1 ]
        ymods = [ 0, 1, 1,  1 ]

        for im in range(4):
            xbase = xbases[im]
            ybase = ybases[im]
            xdirection = xdirections[im]
            xlength = xlengths[im]
            ylength = ylengths[im]
            xmod = xmods[im]
            ymod = ymods[im]
            for ix in range(xlength):
                for iy in range(ylength):
                    bx = (xdirection * ix) + xbase
                    by = iy + ybase
                    start_piece = self.board[by][bx]
                    if start_piece == self.blank_val:
                        continue
                    matched = True
                    s = 1
                    for s in range(self.board_win_length):
                        nx = bx + (xmod * s)
                        ny = by + (ymod * s)
                        next_piece = self.board[ny][nx]
                        if start_piece != next_piece:
                            matched = False
                            break
                    if matched:
                        return start_piece
        if(self.isFull()):
            return self.tie_val
        return self.blank_val





from settings import COLOR_BLUE
from settings import COLOR_RED
from settings import COLOR_RESET

from board import gameSettings
from board import Board


class GUI:
    def print(self, board):
        tempstr = "\n  "
        state = ''
        for xline in range(gameSettings.getBoardSize()):
            tempstr += f"{xline + 1} "
        tempstr += "\n"
        for y in range(gameSettings.getBoardSize()):
            tempstr += f"{y + 1} "
            for x in range(gameSettings.getBoardSize()):
                state = board.getState(x,y);
                if state == gameSettings.getXVal():
                    tempstr += COLOR_BLUE
                    tempstr += state
                    tempstr += " "
                elif state == gameSettings.getOVal():
                    tempstr += COLOR_RED
                    tempstr += state
                    tempstr += " "
                else:
                    tempstr += COLOR_RESET
                    tempstr += state
                    tempstr += " "
            tempstr += "\n"
        return tempstr;

    def menu(self, gamePlayed):
        print("Would you like to play against an AI or do you wish to watch a game?")
        print("1. Train AI")
        print("2. Exit")
        return int(input())

    def saveBoard(self, replay):
        board = Board()
        gui = GUI()

        ostream = open("last_game.txt", 'w')
        for i in len(replay):
            board.addState(replay[i].x, replay[i].y, gameSettings.getXVal())
            ostream += gui.print(board)
            i+1
            if i < len(replay):
                board.addState(replay[i].x, replay[i].y, gameSettings.getOVal())
                ostream += gui.print(board)

        winner = board.isVict()
        if winner == gameSettings.getXVal or winner == gameSettings.getOVal():
            print(f"The Winner is: {winner} \n")
        else:
            print("The game is a tie! \n")
        ostream.close()

    def replayBoard(self, replay):
        board = Board()
        gui = GUI()

        for i in len(replay):
            board.addState(replay[i].x, replay[i].y, gameSettings.getXVal())
            print(gui.print(board))
            i+1
            if i < len(replay):
                board.addState(replay[i].x, replay[i].y, gameSettings.getOVal())
                print(gui.print(board))

        winner = board.isVict()
        if winner == gameSettings.getXVal or winner == gameSettings.getOVal():
            print(f"The Winner is: {winner} \n")
        else:
            print("The game is a tie! \n")

    def settings(self):
        tempchar = chr
        tempint = int

        print(f"Blank Value: (Currently - {gameSettings.getBlankVal()}) \n")
        tempchar = input()[0]
        gameSettings.setBlankVal(tempchar)
        print(f"O Value: (Currently - {gameSettings.getOVal()} ) \n")
        tempchar = input()[0]
        gameSettings.setOVal(tempchar)
        print(f"X Value: (Currently - {gameSettings.getXVal()} ) \n")
        tempchar = input()[0]
        gameSettings.setXVal(tempchar)
        print(f"Tie Value: (Currently - {gameSettings.getTieVal()} ) \n")
        tempchar = input()[0]
        gameSettings.setTieVal(tempchar)

        print("------------------------------------------------------\n")

        print(f"Board Size: (Currently - {gameSettings.getBoardSize()} ) \n")
        tempint = int(input()[0])
        gameSettings.setBoardSize(tempint)
        print(f"Win Length: (Currently - {gameSettings.getWinLength()} ) \n")
        tempint = int(input()[0])

        gameSettings.setWinLength(tempint)

        print("------------------------------------------------------\n")

        print(f"AI Recursion Dpeth: (Currently - {gameSettings.getRecursionDepth()} ) \n")
        tempint = int(input()[0])
        gameSettings.setRecursionDepth(tempint)

    def processedCount(self, board_count):
        print(f"\n{board_count} boards were processed in that last game.\n")

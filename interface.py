from gui import GUI
from board import Board
from board import Move
from board import gameSettings
from qai import QAI
import collections
import matplotlib.pyplot as plt
import matplotlib.ticker
import numpy as np


class Interface:
    def __init__(self):
        self.board_count = 0
        self.replay = []

    def play(self):
        running = True
        gamePlayed = False
        emptyReplay = []
        while(running):
            board = Board()
            gui = GUI()
            result = gui.menu(gamePlayed)
            if result == 1:
                x = QAI()
                train = int(input("How many games to you want the AI to process? { Recommended: 2000 }"))
                epoc = int(input("How often do you want your model to attempt a move rather than randomly move? "
                                 "Percentage "
                                 "{ Recommended: 90 }"))
                while True:
                    x.train(train, float(epoc / 100))
            elif result == 2:
                running = False
            else:
                print("Please choose an available response. \n")






"""
# QAI : Q-Learning AI


"""

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import load_model
import random
import numpy as np
import math

from board import gameSettings
from board import Board

BOARD_SIZE = gameSettings.getBoardSize()

class QAI:
    def __init__(self):
        self.x_train = True
        self.model = Sequential()
        self.model.add(Dense(units=130, activation='relu', input_dim=(BOARD_SIZE ** 2) * 3,
                             kernel_initializer='random_uniform', bias_initializer='zeros'))
        self.model.add(Dense(units=250, activation='relu', kernel_initializer='random_uniform',
                             bias_initializer='zeros'))
        self.model.add(Dense(units=140, activation='relu', kernel_initializer='random_uniform',
                             bias_initializer='zeros'))
        self.model.add(Dense(units=60, activation='relu', kernel_initializer='random_uniform',
                             bias_initializer='zeros'))
        self.model.add(Dense(BOARD_SIZE ** 2, kernel_initializer='random_uniform', bias_initializer='zeros'))
        self.model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])

        self.model_2 = Sequential()
        self.model_2.add(Dense(units=130, activation='relu', input_dim=(BOARD_SIZE ** 2) * 3,
                               kernel_initializer='random_uniform', bias_initializer='zeros'))
        self.model_2.add(Dense(units=250, activation='relu', kernel_initializer='random_uniform',
                               bias_initializer='zeros'))
        self.model_2.add(Dense(units=140, activation='relu', kernel_initializer='random_uniform',
                               bias_initializer='zeros'))
        self.model_2.add(Dense(units=60, activation='relu', kernel_initializer='random_uniform',
                               bias_initializer='zeros'))
        self.model_2.add(Dense(BOARD_SIZE ** 2, kernel_initializer='random_uniform', bias_initializer='zeros'))
        self.model_2.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])
        self.board = Board()
        self.games = []
        self.current_game = []
        self.count = 0
        self.eg: float
        try:
            self.model = load_model('tic_tac_toe_x.h5')
            self.model_2 = load_model('tic_tac_toe_o.h5')
            print('Models Loaded')
        except:
            print('No Pre-made Models Found')

    def hotstate(self):
        self.current_state = []

        for i in range(0, (BOARD_SIZE**2)):
            if self.board.getState_flat(i) == gameSettings.getBlankVal():
                self.current_state.append(1)
                self.current_state.append(0)
                self.current_state.append(0)
            elif self.board.getState_flat(i) == gameSettings.getXVal():
                self.current_state.append(0)
                self.current_state.append(1)
                self.current_state.append(0)
            elif self.board.getState_flat(i) == gameSettings.getOVal():
                self.current_state.append(0)
                self.current_state.append(0)
                self.current_state.append(1)

        return self.current_state

    def reward_outcome(self, game):
        total_reward = 0
        board = Board()
        board.addBoard_flat(game)
        win = board.isVict()
        if self.x_train:
            if win == gameSettings.getXVal():
                return 1
            elif win == gameSettings.getOVal():
                return -1
        elif not self.x_train:
            if win == gameSettings.getXVal():
                return -1
            elif win == gameSettings.getOVal():
                return 1
        return 0


    def train(self, train_length: int, epoch_greed: float):
        self.eg = epoch_greed
        for i in range(0, train_length):

            playing = True
            nn_turn = True
            x_choice = 0
            y_choice = 0
            self.current_game = []
            self.current_game.append(self.board.getBoard_flat())
            nn_board = self.board
            while playing:
                if nn_turn:
                    if random.uniform(0, 1) <= self.eg:
                        choosing = True
                        while choosing:
                            x_choice = random.randint(0, (BOARD_SIZE ** 2) - 1)
                            if self.board.getState_flat(x_choice) == gameSettings.getBlankVal():
                                choosing = False
                                self.board.addState_flat(x_choice, gameSettings.getXVal())
                                self.current_game.append(self.board.getBoard_flat())
                    else:
                        pre = self.model.predict(np.asarray([self.hotstate()]), batch_size=1)[0]
                        highest = -1000
                        num = -1
                        for i in range(0, (BOARD_SIZE ** 2)):
                            if self.board.getState_flat(i) == gameSettings.getBlankVal():
                                if pre[i] > highest:
                                    highest = pre[i].copy()
                                    num = i
                        choosing = False
                        self.board.addState_flat(num, gameSettings.getXVal())
                        self.current_game.append(self.board.getBoard_flat())
                else:
                    if random.uniform(0, 1) <= self.eg:
                        choosing = True
                        while choosing:
                            x_choice = random.randint(0, (BOARD_SIZE ** 2) - 1)
                            if self.board.getState_flat(x_choice) == gameSettings.getBlankVal():
                                choosing = False
                                self.board.addState_flat(x_choice, gameSettings.getOVal())
                                self.current_game.append(self.board.getBoard_flat())
                    else:
                        pre = self.model_2.predict(np.asarray([self.hotstate()]), batch_size=1)[0]
                        highest = -1000
                        num = -1
                        for i in range(0, (BOARD_SIZE ** 2)):
                            if self.board.getState_flat(i) == gameSettings.getBlankVal():
                                if pre[i] > highest:
                                    highest = pre[i].copy()
                                    num = i
                        choosing = False
                        self.board.addState_flat(num, gameSettings.getOVal())
                        self.current_game.append(self.board.getBoard_flat())

                if self.board.isFull() or not self.board.isVict() == gameSettings.getBlankVal():
                    playing = False

                nn_turn = not nn_turn

            self.games.append(self.current_game)
            self.board = Board()

        self.process_games()
        self.games = []


    def process_games(self):
        xt = 0
        ot = 0
        dt = 0
        states = []
        q_values = []
        states_2 = []
        q_values_2 = []
        for game in self.games:
            total_reward = self.reward_outcome(game[len(game) - 1])
            if total_reward == -1:
                ot += 1
            elif total_reward == 1:
                xt += 1
            else:
                dt += 1

            for i in range(0, len(game) - 1):
                if i % 2 == 0:
                    for j in range(0, (BOARD_SIZE**2)):
                        if not game[i][j] == game[i + 1][j]:
                            reward_vector = np.zeros((BOARD_SIZE**2))
                            reward_vector[j] = total_reward * (self.eg ** (math.floor((len(game) - i) / 2) - 1))
                            states.append(game[i].copy())
                            q_values.append(reward_vector.copy())
                else:
                    for j in range(0, (BOARD_SIZE**2)):
                        if not game[i][j] == game[i + 1][j]:
                            reward_vector = np.zeros((BOARD_SIZE**2))
                            reward_vector[j] = -1 * total_reward * (self.eg ** (math.floor((len(game) - i) / 2) - 1))
                            states_2.append(game[i].copy())
                            q_values_2.append(reward_vector.copy())

        if self.x_train:
            zipped = list(zip(states, q_values))
            random.shuffle(zipped)
            states, q_values = zip(*zipped)
            new_states = []
            for state in states:
                new_states.append(self.hotstate())

            self.model.fit(np.asarray(new_states), np.asarray(q_values), epochs=4, batch_size=len(q_values),
                      verbose=1)
            self.model.save('tic_tac_toe_x.h5')
            del self.model
            self.model = load_model('tic_tac_toe_x.h5')
            print(xt / 20, ot / 20, dt / 20)
        else:
            zipped = list(zip(states_2, q_values_2))
            random.shuffle(zipped)
            states_2, q_values_2 = zip(*zipped)
            new_states = []
            for state in states_2:
                new_states.append(self.hotstate())


            self.model_2.fit(np.asarray(new_states), np.asarray(q_values_2), epochs=4, batch_size=len(q_values_2),
                        verbose=1)
            self.model_2.save('tic_tac_toe_o.h5')
            del self.model_2
            self.model_2 = load_model('tic_tac_toe_o.h5')
            print(xt / 20, ot / 20, dt / 20)

        self.x_train = not self.x_train
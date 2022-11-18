from pickletools import read_uint1
from Board import Board
from Window import Window
from Player import Player
from Constants import ACTIONS, NUM_EPISODES, EPSILON, STEPS
import random
import operator
import copy

class QLearner(object):
    qTable = {} # Maps cell to possible actions. Actions then map to reward
    discount = 0.3
    alpha = 0.1
    currState = (0,0)
    state_actions = []

    # model function
    model = {}

    def __init__(self, b=Board()):
        self.board = b
        self.initQTable()

    def initQTable(self):
        for cell in self.board.getCells():
            self.qTable[cell] = {}
            for action in ACTIONS:
                if self.board.isValidCell(cell, action):
                    self.qTable[cell][action] = 0

    def learn(self):
        for episode in range(NUM_EPISODES):
            self.currState = (0, 0)
            while not self.board.isTerminalCell(self.currState):

                action = self.epsilonGreedy(self.currState)
                self.state_actions.append((self.currState,action))

                nxtState = self.board.getCellAfterAction(self.currState,action)

                reward = self.board.getCellValue(nxtState)

                # update Q-value
                self.qTable[self.currState][action]+= self.alpha*(reward + max(list(self.qTable[nxtState].values())) - self.qTable[self.currState][action])

                # update model
                if self.currState not in self.model.keys():
                    self.model[self.currState] = {}
                self.model[self.currState][action] = (reward, nxtState)
                self.currState = nxtState

                # loop n times to randomly update Q-value
                for _ in range(STEPS):
                   # randomly choose an state
                   rand_idx = random.choice(range(len(self.model.keys())))  
                   _state = list(self.model)[rand_idx]
                   # randomly choose an action
                   rand_idx = random.choice(range(len(self.model[_state].keys())))  
                   _action = list(self.model[_state])[rand_idx]

                   _reward, _nxtState = self.model[_state][_action]

                   self.qTable[_state][_action]+= self.alpha*(_reward + max(list(self.qTable[_nxtState].values())) - self.qTable[_state][_action])

        return self.qTable

    def epsilonGreedy(self, state):
        action = ""
        mx_nxt_reward = -9999

        randInt = random.randint(1,11)
        if randInt <= EPSILON:
            validActions = list(filter(lambda action: self.board.isValidCell(state, action), ACTIONS))
            action = random.choice(validActions)

        else:
            # greedy action
            current_position = state

            # if all actions have same value, then select randomly
            if len(set(self.qTable[current_position].values())) == 1:
                validActions = list(filter(lambda action: self.board.isValidCell(state, action), ACTIONS))
                action = random.choice(validActions)
            else:
                for ac in list(filter(lambda action: self.board.isValidCell(state, action), ACTIONS)):
                    nxt_reward = self.qTable[current_position][ac]
                    if nxt_reward >= mx_nxt_reward:
                        action = ac
                        mx_nxt_reward = nxt_reward

        return action

    # Q(s,a)+=α⋅[r+γ⋅maxαQ(s′)−Q(s,a)]
    def evalQFunction(self,coord, action):
        nextCell = self.board.getCellAfterAction(coord, action)
        reward = self.board.getCellValue(nextCell)
        maxQSPrime = max([self.qTable[nextCell][action2] for action2 in ACTIONS if self.board.isValidCell(nextCell, action2)])
        self.qTable[coord][action] += (self.alpha * (reward + self.discount * maxQSPrime - self.qTable[coord][action]))

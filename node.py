import random
import chess
import math

# Nothing to do here :)
class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.score = 0

    # This function is used to select the child node that should be explored next in the Monte Carlo Tree Search algorithm.
    # It takes an exploration parameter as input and returns the child node with the highest 
    # score according to a formula that balances exploration and exploitation.
    def select_child(self, exploration_param):
        best_score = float('-inf')
        best_child = None
        for child in self.children:
            if child.visits == 0:
                score = float('inf')
            else:
                score = child.score / child.visits + exploration_param * \
                    math.sqrt(math.log(self.visits) / child.visits)
            if score > best_score:
                best_score = score
                best_child = child
        return best_child

    # This function is used to expand the current node by adding child nodes to it. 
    # It does this by generating a list of legal moves for the current state, 
    # creating a new state for each move, and then creating a new child node for each new state.
    def expand(self):
        legal_moves = list(self.state.legal_moves)
        for move in legal_moves:
            new_state = self.state.copy()
            new_state.push(move)
            self.children.append(Node(new_state, parent=self))

    # This function is used to update the statistics of a node based on the result of a simulation. 
    # It increases the visit count of the node by one and adds the score of the simulation to the total score of the node.
    def update(self, score):
        self.visits += 1
        self.score += score

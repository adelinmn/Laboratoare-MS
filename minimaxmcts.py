from node import Node
from mcts import MCTS
import random
import chess

class MiniMaxMCTS:
    def __init__(self, depth=3, exploration_param=1.4, max_iterations=1000):
        self.depth = depth
        self.exploration_param = exploration_param
        self.max_iterations = max_iterations
        self.piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 100
        }

    # TODO You can use the same evaluation function as above, or you can do something more complex here
    def evaluate(self, board: chess.Board):
        if board.is_checkmate():
            if board.turn == chess.WHITE:
                return -999 
            else:
                return 999

        pieces = board.piece_map()

        white_score = 0
        black_score = 0

        for piece in pieces.values():
            if piece.color == chess.WHITE:
                white_score += self.piece_values[piece.piece_type]
            else:
                black_score += self.piece_values[piece.piece_type]

        return white_score - black_score

    # The main function of the MiniMax with MCTS algorithm, gets a state and returns the best move to play from that state
    def search(self, state):
        best_move = None
        best_score = float('-inf')
        legal_moves = list(state.legal_moves)
        mcts = MCTS(exploration_param=self.exploration_param, max_iterations=self.max_iterations)

        for move in legal_moves:
            # Create a new state with the current move and search for the best state using MCTS
            new_state = state.copy()
            new_state.push(move)
            # Get the minimum score that can be achieved from that state
            mcts_best_state = mcts.search(new_state)
            score = self.min_value(mcts_best_state, self.depth-1)
            # Update the best score if the minimum score that can be achieved is better than the last one
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    # This function represents the perspective of the maximizing player
    # and recursively computes the maximum possible score that player 
    # can achieve by assuming the minimizing player will play optimally.
    def max_value(self, state, depth):
        if depth == 0 or state.is_game_over():
            return self.evaluate(state)

        value = float('-inf')

        for move in state.legal_moves:
            state.push(move)
            value = max(value, self.min_value(state, depth - 1))
            state.pop()

        return value

    # This function represents the perspective of the minimizing player 
    # and recursively computes the minimum possible score that player 
    # can achieve by assuming the maximizing player will play optimally.
    def min_value(self, state, depth):
        if depth == 0 or state.is_game_over():
            return self.evaluate(state)

        value = float('inf')

        for move in state.legal_moves:
            state.push(move)
            value = min(value, self.max_value(state, depth - 1))
            state.pop()

        return value
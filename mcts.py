from node import Node
import random
import chess

class MCTS:
    def __init__(self, exploration_param=1.4, max_iterations=1000):
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

    def search(self, state):
        root = Node(state)
        
        # Max iterations will determine how many children will be explored by this search
        for i in range(self.max_iterations):
            # Select a child node to explore based on the UCB1 formula (use the select_child method)
            node = root
            while node.children:
                node = node.select_child(self.exploration_param)
            # You should check if the node has been previously visited, if not, expand it
            if not node.state.is_game_over():
                node.expand()
                node = random.choice(node.children)
            # Simulate a game that starts from the chosen node, update the node, and backpropagate the score update until you reach the root
            result = self.simulate(node.state)

            while node is not None:
                if node.state.turn == chess.WHITE:
                    node.update(result)
                else:
                    node.update(-result)
                node = node.parent

        # select the best child (that has the highest score)
        if not root.children:
            return state
        best_child = max(root.children, key = lambda c: c.visits)
        # Returns the state of the game for the best outcome
        return best_child.state

    # This function is used by the MCTS algorithm to simulate a game from a given state.
    def simulate(self, state):
        rollout_state = state.copy()

        while not rollout_state.is_game_over():
            move = random.choice(list(rollout_state.legal_moves))
            rollout_state.push(move)

        return self.evaluate(rollout_state)

# mcts = MCTS()
# board = chess.Board()
# print(mcts.evaluate(board))
# board.push_uci("e2e4")
# board.push_uci("d7d5")
# board.push_uci("e4d5")
# print(mcts.evaluate(board))
# board.push_uci("b8c6")
# print(mcts.evaluate(board))
# board.push_uci("d5c6")
# # board.push_uci("a7a6")
# print(mcts.evaluate(board))
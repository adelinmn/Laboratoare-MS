from minimaxmcts import MiniMaxMCTS
import chess

# Create a MiniMaxMCTS object with a depth of 14, exploration parameter of 8, and max iterations of 1000
algo = MiniMaxMCTS(depth=4, exploration_param=8, max_iterations=1000)

# Create a chess board object for the Tricky Queen Triangulation puzzle setup by D. Joseph. This puzzle requires 13 moves to get the checkmate.
board = chess.Board(f"1k1K4/1p5P/1P6/8/8/8/p7/8 w - - 0 1")

# Use the MiniMaxMCTS algorithm to select the best move for the starting position
best_move = algo.search(board)

# Print the best move
print("Best move: ", best_move.uci())
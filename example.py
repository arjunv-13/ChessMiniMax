import chess
import chess.engine

from eval import evalBoard

# Step 1: Set up the chess board and define the initial position
def get_initial_board():
    return chess.Board()

# Step 2: Implement the evaluation function
pieceValues = {"r": -5, "n": -3, "b": -3, "q": -9, "k": -100, "p": -1, ".": 0, "R": 5, "N": 3, "B": 3, "Q": 9, "K": 100, "P": 1}
def toArray(board):
    stringBoard = str(board)
    stringBoard = stringBoard.replace(" ", "")
    stringBoard = stringBoard.replace("\n", "")
    arrayBoard = []
    for i in range(8):
        arrayBoard.append(stringBoard[i * 8: i * 8 + 8])
    return arrayBoard
    

def evaluate_board(board):
    return evalBoard(board)
    """arrayBoard = toArray(board)
    eval = 0
    for row in range(8):
        for col in range(8):
            eval += pieceValues[arrayBoard[row][col]]"""
    return eval
    # Your evaluation function goes here.
    # This function should return a numerical value representing the board's evaluation.


# Step 3: Create the minimax function with alpha-beta pruning
def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if maximizing_player:
        max_eval = float("-inf")
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float("inf")
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

# Step 4: Implement the main loop to run the engine
def find_best_move(board, depth):
    best_move = None
    max_eval = float("-inf")
    alpha = float("-inf")
    beta = float("inf")

    for move in board.legal_moves:
        board.push(move)
        eval = minimax(board, depth - 1, alpha, beta, False)
        board.pop()

        if eval > max_eval:
            max_eval = eval
            best_move = move

    return best_move

def main():
    board = get_initial_board()

    while not board.is_game_over():
        print(board)
        if board.turn == chess.WHITE:
            # Change the depth value to set the engine's search depth (higher depth takes more time).
            best_move = find_best_move(board, depth=5)
            board.push(best_move)
        else:
            move_str = input("Your move: ")
            move = chess.Move.from_uci(move_str)
            board.push(move)

    print("Game Over")
    print("Result:", board.result())

if __name__ == "__main__":
    main()

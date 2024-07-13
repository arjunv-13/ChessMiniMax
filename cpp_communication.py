import chess
import chess.polyglot
import random
import subprocess
from database_interface import get_opening_move, get_endgame_move

EXECUTABLE_NAME = '/Users/arjunverma/Desktop/C++ Chess Engine/main'

def get_movelist(board):
    movelist = []
    while board.move_stack:
        movelist.append(board.uci(board.pop()))
    movelist.reverse()
    for move in movelist:
        board.push_san(move)
    return movelist
    return " ".join(movelist)

def get_engine_move(board, depth, capture_depth):
    move = get_opening_move(board)
    if move is not None:
        return move
    move = get_endgame_move(board)
    if move is not None:
        return move

    engine_move = communicate_with_cpp_engine(get_movelist(board), depth, capture_depth)

    # outdated use of fen not movelist
    # fen_position = board.fen()
    # engine_move = communicate_with_cpp_engine(fen_position, depth)

    return engine_move


def communicate_with_cpp_engine(moves, depth, capture_depth):
    # Call the C++ engine as a subprocess
    time_ms = 2000
    
    arg_list = [EXECUTABLE_NAME] + moves + [str(depth), str(capture_depth), str(time_ms)]
    process = subprocess.Popen(arg_list, stdout=subprocess.PIPE, text=True)
    
    # Capture the output (engine's move suggestion)
    engine_output = process.stdout.read().strip()
    
    # Close the subprocess
    process.wait()

    return engine_output
import chess
import chess.engine
import sys
import pygame as pg
import random
import time
#sys.path.append('ChessCoding')

import engine
from board import printBoard, playMoveSound, printCheckmate

class Bot:
    def __init__(self, engine_function):
        self.engine = engine_function
    
    def getMove(self, board):
        return self.engine(board)
    
    def getEngineName(self):
        return self.engine.__name__

def findBestMove_Arjun_depth3(board):
    return board.parse_uci(engine.findBestMove(board, 3, 2, False, 0.1)[0])

def findBestMove_Arjun_depth2(board):
    return board.parse_uci(engine.findBestMove(board, 2, 2, True, 0.1)[0])

def stockfish_move_time(board):
    engine = chess.engine.SimpleEngine.popen_uci("/opt/homebrew/bin/stockfish")
    result = engine.play(board, chess.engine.Limit(time=0.1))
    engine.quit()
    return result.move

def stockfish_move_depth(board):
    engine = chess.engine.SimpleEngine.popen_uci("/opt/homebrew/bin/stockfish")
    result = engine.play(board, chess.engine.Limit(depth=5))
    engine.quit()
    return result.move

def stockfish_move_nodes(board):
    engine = chess.engine.SimpleEngine.popen_uci("/opt/homebrew/bin/stockfish")
    result = engine.play(board, chess.engine.Limit(nodes = 3))
    engine.quit()
    return result.move

def randomMove(board):
    moves = list(board.legal_moves)
    return random.choice(moves)

def initializeBots():
    botA = Bot(findBestMove_Arjun_depth3)
    botB = Bot(stockfish_move_time)
    return botA, botB

def simGame(botA, botB, window):
    board = chess.Board()
    while not board.is_game_over():
        printBoard(window, board)
        if board.turn:
            move = botA.getMove(board)
        else:
            move = botB.getMove(board)
        san_move = board.san(move)
        board.push(move)
        playMoveSound(san_move)
    printCheckmate(window, board)
    time.sleep(2)
    result = board.result()
    if result == "1/2-1/2":
        return 0
    elif result == "1-0":
        return 1
    else:
        return -1
    
def simGames_one_side(num_games, botA, botB, window, completed, total):
    a_wins = 0
    b_wins = 0
    draws = 0
    for i in range(num_games):
        result = simGame(botA, botB, window)
        print(f"Game {completed + i + 1} of {total} complete")
        if result == 1:
            a_wins += 1
        elif result == -1:
            b_wins += 1
        else:
            draws += 1
    return a_wins, b_wins, draws


if __name__ == "__main__":
    WIDTH, HEIGHT = 750, 750
    FPS = 60
    WIN = pg.display.set_mode((WIDTH, HEIGHT))
    pg.init()
    font = pg.font.SysFont(None, 80)
    pg.display.set_caption("Chess!")

    GAMES_PER_SIDE = 2

    botA, botB = initializeBots()
    a_wins = 0
    b_wins = 0
    draws = 0
    result = simGames_one_side(GAMES_PER_SIDE, botA, botB, WIN, 0, 2 * GAMES_PER_SIDE)
    a_wins += result[0]
    b_wins += result[1]
    draws += result[2]
    result = simGames_one_side(GAMES_PER_SIDE, botB, botA, WIN, GAMES_PER_SIDE, 2 * GAMES_PER_SIDE)
    a_wins += result[1]
    b_wins += result[0]
    draws += result[2]

    print(f"Bot A ({botA.getEngineName()}) wins:", a_wins)
    print(f"Bot B ({botB.getEngineName()}) wins:", b_wins)
    print("Draws:", draws)
    
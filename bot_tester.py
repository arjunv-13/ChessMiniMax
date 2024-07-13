import chess
import chess.engine
import sys
import pygame as pg
import random
import time
import math
from cpp_communication import get_engine_move 

import engine
from board import printBoard, playMoveSound, printCheckmate, playerMoveGUI
from gameInfoBar import drawInfoBar
import timerClass

WHITE = (255, 255, 255)
TIME_PER_GAME = 60
INCREMENT = 3


class Bot:
    def __init__(self, engine_function):
        self.engine = engine_function
        self.eval_loss = []
    
    def getMove(self, board, window):
        return self.engine(board, window)
    
    def addEvalLoss(self, loss):
        self.eval_loss.append(loss)

    def printEvalStats(self):
        if not self.eval_loss:
            return
        
        mate_inclusive_avg = round(sum(self.eval_loss)/len(self.eval_loss), 3)
        exclude_mates = [i for i in self.eval_loss if i < 100]
        mate_exclusive_avg =round(sum(exclude_mates)/len(exclude_mates), 3)

        exclude_negatives = [i for i in exclude_mates if i >= 0]
        negative_exclusive_avg =round(sum(exclude_negatives)/len(exclude_negatives), 3)
        
        print(f"{self.getEngineName()} had an average eval loss of {mate_inclusive_avg}, an average eval loss of {mate_exclusive_avg} excluding mate outliers, an average eval loss of {negative_exclusive_avg} excluding negatives outliers.")
    
    def getEngineName(self):
        return self.engine.__name__

def findBestMove_Arjun_depth3(board, window):
    return board.parse_uci(engine.findBestMove(board, 3, 2, False, 0.1)[0])

def findBestMove_Arjun_depth2(board, window):
    return board.parse_uci(engine.findBestMove(board, 2, 2, True, 0.1)[0])

def cpp_engine(board, window):
    return board.parse_uci(get_engine_move(board, 3, 2))

def two_cpp_engine(board, window):
    return board.parse_uci(get_engine_move(board, 5, 3))

def player_move(board, window):
    return board.parse_san(playerMoveGUI(board, window))

def stockfish_move_time(board, window):
    engine = chess.engine.SimpleEngine.popen_uci("/opt/homebrew/bin/stockfish")
    result = engine.play(board, chess.engine.Limit(time=.1))
    engine.quit()
    return result.move

def stockfish_move_depth(board, window):
    engine = chess.engine.SimpleEngine.popen_uci("/opt/homebrew/bin/stockfish")
    result = engine.play(board, chess.engine.Limit(depth=1))
    engine.quit()
    return result.move

def stockfish_move_nodes(board, window):
    engine = chess.engine.SimpleEngine.popen_uci("/opt/homebrew/bin/stockfish")
    result = engine.play(board, chess.engine.Limit(nodes = 3))
    engine.quit()
    return result.move

def randomMove(board, window):
    moves = list(board.legal_moves)
    return random.choice(moves)

def initializeBots():
    botA = Bot(two_cpp_engine)
    botB = Bot(two_cpp_engine)
    return botA, botB

def simGame(botA, botB, window):
    window.fill(WHITE)
    board = chess.Board()
    whiteTimer = timerClass.Timer(TIME_PER_GAME, INCREMENT)
    blackTimer = timerClass.Timer(TIME_PER_GAME, INCREMENT)
    whitePlayer = botA.getEngineName()
    blackPlayer = botB.getEngineName()
    curr_eval = None

    while not board.is_game_over():
        printBoard(window, board)
        engine = chess.engine.SimpleEngine.popen_uci("/opt/homebrew/bin/stockfish")
        prev_eval = curr_eval
        curr_eval = round(engine.analyse(board, chess.engine.Limit(time=0.3))['score'].white().score(mate_score=100000)/100, 2)

        if curr_eval > 500:
            curr_eval = 1000
        elif curr_eval < -500:
            curr_eval = -1000
        engine.quit()
        drawInfoBar(window, curr_eval, whitePlayer, blackPlayer, whiteTimer.get_time_string(), blackTimer.get_time_string())

        if board.turn:
            whiteTimer.start()
            move = botA.getMove(board, window)
            whiteTimer.stop()
        else:
            blackTimer.start()
            move = botB.getMove(board, window)
            blackTimer.stop()

        if prev_eval is not None:
            if board.turn:
                botB.addEvalLoss(curr_eval - prev_eval)
            else:
                botA.addEvalLoss(prev_eval - curr_eval)
        
        san_move = board.san(move)
        board.push(move)
        playMoveSound(san_move)
    printCheckmate(window, board)
    time.sleep(1)
    result = board.result()
    #print(board.outcome().termination)
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
    WIDTH, HEIGHT = 1000, 750
    FPS = 60
    WIN = pg.display.set_mode((WIDTH, HEIGHT))
    pg.init()
    font = pg.font.SysFont(None, 80)
    pg.display.set_caption("Chess!")

    GAMES_PER_SIDE = 1

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

    botA.printEvalStats()
    botB.printEvalStats()
    
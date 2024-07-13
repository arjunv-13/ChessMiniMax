import pygame as pg
import chess
#from noTreeEngine import findBestMove
from engine import findBestMove, setDepthReturn
from board import printBoard, playerMoveGUI, playMoveSound, printCheckmate
from gameInfoBar import drawInfoBar
import time
import chess.engine

from cpp_communication import get_engine_move
import random
import timerClass


normalSound = pg.mixer.Sound("chessPieces/move.mp3")
captureSound = pg.mixer.Sound("chessPieces/capture.mp3")
castleSound = pg.mixer.Sound("chessPieces/castle.mp3")
promoteSound = pg.mixer.Sound("chessPieces/promote.mp3")
checkSound = pg.mixer.Sound("chessPieces/check.mp3")

WHITE = (255, 255, 255)
WIDTH, HEIGHT = 1000, 750
FPS = 60
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.init()
font = pg.font.SysFont(None, 80)
pg.display.set_caption("Chess!")

def chooseColor():
    valid = False
    while not valid:
        color = input("Choose your color ('W' or 'B'): ")
        color = color.lower()
        if color == "b":
            white = False
            valid = True
        if color == "w":
            white = True
            valid = True
    return white

# def computerMove(board, main_depth, capture_search_depth, augment_depth, variance):
#     printBoard(WIN, board)
#     bestMove = findBestMove(board, main_depth, capture_search_depth, augment_depth, variance)
#     standard = board.san(board.parse_uci(bestMove[0]))
#     board.push_san(bestMove[0])
#     bestMove[0] = standard
#     return bestMove

def computerMove(board, main_depth, capture_search_depth, augment_depth, variance):
    move = get_engine_move(board, main_depth, capture_search_depth)
    san_move = board.san(board.parse_uci(move))
    board.push_uci(move)
    return str(san_move), 0, 0
    
def playerMove(board):
    valid = False
    while not valid:
        move = input("Input your move in standard algebraic notation (like Nf6): ")
        try:
            standard = board.san(board.parse_san(move))
            board.push_san(move)
            valid = True
        except:
            print("Invalid move")    
    return standard            

def main():
    board = chess.Board()
    halfMoveCounter = 0
    WIN.fill(WHITE)
    printBoard(WIN, board)
    pg.display.update()
    main_depth, capture_depth, variance = setDepthReturn()

    playerTimer = timerClass.Timer(60, 2)
    engineTimer = timerClass.Timer(60, 2)
    

    playerWhite = chooseColor()
    if playerWhite:
        whitePlayer = "You"
        white_time = playerTimer.get_time_string()
        blackPlayer = "Engine"
        black_time = engineTimer.get_time_string()
    else:
        whitePlayer = "Engine"
        white_time = engineTimer.get_time_string()
        blackPlayer = "You"
        black_time = playerTimer.get_time_string()

    curr_eval = 0

    while not board.is_game_over():
        printBoard(WIN, board)
        engine = chess.engine.SimpleEngine.popen_uci("/opt/homebrew/bin/stockfish")
        # curr_eval = round(engine.analyse(board, chess.engine.Limit(time=0.1))['score'].white().score(mate_score=100000)/100, 2)
        curr_eval = 0
        if curr_eval > 500:
            curr_eval = 1000
        elif curr_eval < -500:
            curr_eval = -1000
        engine.quit()
        drawInfoBar(WIN, curr_eval, whitePlayer, blackPlayer, white_time, black_time)
        
        if halfMoveCounter % 2 != playerWhite:
            playerTimer.start()
            if playerWhite:
                whiteTimer = playerTimer
                blackTimer = engineTimer
            else:
                whiteTimer = engineTimer
                blackTimer = playerTimer

            move = playerMoveGUI(board, WIN, curr_eval, whitePlayer, blackPlayer, whiteTimer, blackTimer)
            board.push_san(move)
            playerTimer.stop()
            if playerWhite:
                white_time = playerTimer.get_time_string()
            else:
                black_time = playerTimer.get_time_string()
            
        else:
            engineTimer.start()
            print("Thinking...")
            bestMove = computerMove(board, main_depth, capture_depth, True, variance)
            move, bestEval, playedEval = bestMove[0], bestMove[1], bestMove[2]
            print(f"The computer played {move} ({playedEval}) with an evaluation of {bestEval}")
            curr_eval = playedEval
            engineTimer.stop()

            if playerWhite:
                black_time = engineTimer.get_time_string()
            else:
                white_time = engineTimer.get_time_string()
        halfMoveCounter += 1
        playMoveSound(move)
    printBoard(WIN, board)
    printCheckmate(WIN, board)
    drawInfoBar(WIN, curr_eval, whitePlayer, blackPlayer, white_time, black_time)
    print("Game Over")
    print("Result:", board.result())
    time.sleep(2)



if __name__ == "__main__":
    main()
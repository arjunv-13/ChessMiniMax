import pygame as pg
import chess
from engine import findBestMove
#from noTreeEngine import findBestMove
from board import printBoard
import time

normalSound = pg.mixer.Sound("chessPieces/move.mp3")
captureSound = pg.mixer.Sound("chessPieces/capture.mp3")
castleSound = pg.mixer.Sound("chessPieces/castle.mp3")
promoteSound = pg.mixer.Sound("chessPieces/promote.mp3")
checkSound = pg.mixer.Sound("chessPieces/check.mp3")

WIDTH, HEIGHT = 750, 750
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

def computerMove(board):
    bestMove = findBestMove(board)
    standard = board.san(board.parse_uci(bestMove[0]))
    board.push_san(bestMove[0])
    bestMove[0] = standard
    return bestMove
    
def playerMove(board):
    valid = False
    while not valid:
        move = input("Input your move in standard algebraic notation (like Nf6): ")
        try:
            board.push_san(move)
            valid = True
        except:
            print("Invalid move")    
    return            

def main():
    board = chess.Board()
    halfMoveCounter = 0

    playerWhite = True
    time.sleep(1.5)

    while not board.is_game_over():
        printBoard(WIN, board)
        
        if halfMoveCounter % 2 != playerWhite:
            print("Thinking...")
            bestMove = computerMove(board)
            move, eval = bestMove[0], bestMove[1]
            print("The computer played", move, "with an evaluation of", eval)
        else:
            print("Thinking...")
            bestMove = computerMove(board)
            move, eval = bestMove[0], bestMove[1]
            print("The computer played", move, "with an evaluation of", eval)
        if "+" in move or "#" in move:
            sound = checkSound
        elif "x" in move:
            sound = captureSound
        elif "O" in move:
            sound = castleSound
        elif "=" in move:
            sound = promoteSound
        else:
            sound = normalSound
        halfMoveCounter += 1
        pg.mixer.Sound.play(sound)
        pg.mixer.music.stop()
    printBoard(WIN, board)
    print("Game Over")
    print("Result:", board.result())
    time.sleep(2)



if __name__ == "__main__":
    main()
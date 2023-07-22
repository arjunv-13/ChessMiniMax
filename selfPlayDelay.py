import pygame as pg
import chess
from engine import findBestMove
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

    time.sleep(1.5)

    game = []

    boardView = chess.Board()
    printBoard(WIN, boardView)

    while not board.is_game_over():
        print("Thinking...")
        bestMove = computerMove(board)
        move, eval = bestMove[0], bestMove[1]
        print("The computer played", move, "with an evaluation of", eval)
        game.append([move, eval])
        halfMoveCounter += 1
    print(f"Game calculated with {halfMoveCounter} ply or {halfMoveCounter/2} moves")
    
    show = input("Type anything to view the game")
    time.sleep(2)
    
    
    for move in game:
        boardView.push_san(move[0])
        print("The computer played", move[0], "with an evaluation of", move[1])
        printBoard(WIN, boardView)
        if "+" in move[0] or "#" in move[0]:
            sound = checkSound
        elif "x" in move[0]:
            sound = captureSound
        elif "O" in move[0]:
            sound = castleSound
        elif "=" in move[0]:
            sound = promoteSound
        else:
            sound = normalSound
        pg.mixer.Sound.play(sound)
        pg.mixer.music.stop()
        time.sleep(1)
    print("Result:", board.result())



if __name__ == "__main__":
    main()
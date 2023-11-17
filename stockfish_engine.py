import chess
import chess.engine
from stockfish import Stockfish
from board import printBoard
import pygame as pg

WIDTH, HEIGHT = 750, 750
FPS = 60
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.init()
font = pg.font.SysFont(None, 80)
pg.display.set_caption("Chess!")

engine = chess.engine.SimpleEngine.popen_uci("/opt/homebrew/bin/stockfish")

board = chess.Board()
while not board.is_game_over():
    result = engine.play(board, chess.engine.Limit(time=0.1))
    board.push(result.move)
    printBoard(WIN, board)

engine.quit()
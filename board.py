import pygame as pg
import time
from eval import toArray
import chess

WIDTH, HEIGHT = 750, 750
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT = (242, 232, 218)
DARK = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (52, 178, 52)

board = chess.Board()


FPS = 60
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.init()
font = pg.font.SysFont(None, 80)
pg.display.set_caption("Chess!")

def draw_window(window):
    window.fill(WHITE)
    row = 0
    box_width = (WIDTH - 30)/8
    box_height = (HEIGHT - 30)/8
    while row * box_width < HEIGHT - 30:
        col = 0
        while col * box_width < WIDTH - 30:
            squareColor = DARK if (row + col) % 2 == 1 else LIGHT
            #print(squareColor)
            pg.draw.rect(window, squareColor, pg.Rect(col * box_width + 15, row * box_height + 15, box_width, box_height))
            col+=1
        row += 1
pieceDict = {"b": "black-bishop.png", "k": "black-king.png", "n":"black-knight.png", "p": "black-pawn.png", "q": "black-queen.png", "r": "black-rook.png", "B": "white-bishop.png", "K": "white-king.png", "N":"white-knight.png", "P": "white-pawn.png", "Q": "white-queen.png", "R": "white-rook.png"}

def getPiece(piece):
    return f"chessPieces/{pieceDict[piece]}"
    
def draw_pieces(window, board):
    box_width = (WIDTH - 30)/8
    box_height = (HEIGHT - 30)/8
    arrayBoard = toArray(board)
    for row in range(8):
        for col in range(8):
            piece = arrayBoard[row][col]
            if piece != ".":
                #imp = pg.image.load(getPiece(piece)).convert_alpha()
                img = pg.image.load(getPiece(piece))
                img = pg.transform.scale(img, (box_width - 5, box_height - 5))
                imp = img.convert_alpha()
                window.blit(imp, (col * box_width + 15, row * box_width + 15))


def printBoard(window, board):
    draw_window(window)
    draw_pieces(window, board)
    pg.display.update()
    
    
def main():
    clock = pg.time.Clock()
    run = True
    keyPressed = False
    while run:
        clock.tick(FPS)
        draw_window()
        draw_pieces(board)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    "x"        

        pg.display.update()
    
    pg.quit()

if __name__ == "__main__":
    main()
import pygame as pg
import time
from evalOpening import toArray
from gameInfoBar import drawInfoBar
import chess
import math

WIDTH, HEIGHT = 750, 750
WHITE = (255, 255, 255)
GREY = (127, 127, 127)
BLACK = (0, 0, 0)
LIGHT = (242, 232, 218)
DARK = (128, 128, 128)
RED = (255, 0, 0)
LIGHTRED = (255, 200, 200)

ROYALBLUE =  (65, 105, 225)
ROYALBLUE2 = (45, 85, 205)
START_SQUARE_COLOR = (14, 101, 160)
END_SQUARE_COLOR = (109, 172, 207)
GREEN = (52, 178, 52)

board = chess.Board()


FPS = 10
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.init()
font = pg.font.SysFont(None, 80)
pg.display.set_caption("Chess!")

def draw_window(window):
    #window.fill(WHITE)
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


def printBoard(window, board, highlighted=[]):
    draw_window(window)
    draw_highlights(window, highlighted)
    draw_prev_move(window, board)
    draw_pieces(window, board)
    pg.display.update()

def printCheckmate(window, board):
    winner = board.result()
    if winner == "1-0":
        isWhite = True
    elif winner == "0-1":
        isWhite = False
    else:
        return
    draw_window(window)
    draw_prev_move(window, board)
    
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None and piece.piece_type == chess.KING and piece.color != isWhite:
            king = chess.square_name(square)
    box_width = (WIDTH - 30)/8
    box_height = (HEIGHT - 30)/8
    x = (ord(king[0]) - 97) * box_width + 15
    y = HEIGHT - (int(king[1]) * box_height + 15)
    pg.draw.rect(window, LIGHTRED, pg.Rect(x, y, box_width, box_height),  0)
    draw_pieces(window, board)
    font = pg.font.SysFont(None, 80)
    text = font.render("Checkmate!", True, RED)
    window.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    pg.display.update()
    time.sleep(2)


def playMoveSound(move):
    normalSound = pg.mixer.Sound("chessPieces/move.mp3")
    captureSound = pg.mixer.Sound("chessPieces/capture.mp3")
    castleSound = pg.mixer.Sound("chessPieces/castle.mp3")
    promoteSound = pg.mixer.Sound("chessPieces/promote.mp3")
    checkSound = pg.mixer.Sound("chessPieces/check.mp3")
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
    pg.mixer.Sound.play(sound)
    pg.mixer.music.stop()


def draw_prev_move(window, board):
    if not board.move_stack:
        return
    uci_move = board.peek().uci()
    squares = [uci_move[:2], uci_move[2:4]]
    box_width = (WIDTH - 30)/8
    box_height = (HEIGHT - 30)/8
    i = 0
    color = START_SQUARE_COLOR
    for square in squares:
        if i == 1:
            color = END_SQUARE_COLOR
        x = (ord(square[0]) - 97) * box_width + 15
        y = HEIGHT - (int(square[1]) * box_height + 15)
        pg.draw.rect(window, color, pg.Rect(x, y, box_width, box_height),  0)
        i += 1

def draw_highlights(window, highlights):
    box_width = (WIDTH - 30)/8
    box_height = (HEIGHT - 30)/8
    for highlight in highlights:
        x = (ord(highlight[0]) - 97) * box_width + 15
        y = HEIGHT - (int(highlight[1]) * box_height + 15)
        pg.draw.rect(window, RED, pg.Rect(x, y, box_width, box_height),  4)


def draw_promotion_options(window, pieces, img_size):
    img_width = img_size
    img_height = img_size
    i = 0
    for piece in pieces:
        img = pg.image.load(getPiece(piece))
        img = pg.transform.scale(img, (img_width, img_height))
        imp = img.convert_alpha()
        pg.draw.rect(window, RED, pg.Rect(60 + (WIDTH - 120)/24 + i * (WIDTH - 120)/4, HEIGHT/2 - img_height * .5, img_width, img_height))
        window.blit(imp, (60 + (WIDTH - 120)/24 + i * (WIDTH - 120)/4, HEIGHT/2 - img_height * .5))
        i += 1


def getPromotion(window, board):
    #return "q"
    img_size = (WIDTH - 120)/6
    if board.turn:
        pieces = ["Q", "R", "N", "B"]
    else:
        pieces = ["q", "r", "n", "b"]
    
    clock = pg.time.Clock()
    while True:
        clock.tick(FPS)
        draw_window(window)
        draw_pieces(window, board)
        draw_promotion_options(window, pieces, img_size)        
        
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP:
                x, y = pg.mouse.get_pos()
                if (HEIGHT/2) - (img_size)/2 < y < (HEIGHT/2) + (img_size)/2:
                    x = x - 60 - (WIDTH - 120)/24
                    if 0 < x < img_size:
                        return "q"
                    elif (WIDTH - 120)/4 < x < (WIDTH - 120)/4 + img_size:
                        return "r"
                    elif (WIDTH - 120)/4 * 2 < x < (WIDTH - 120)/4 * 2 + img_size:
                        return "n"
                    elif (WIDTH - 120)/4 * 3 < x < (WIDTH - 120)/4 * 3 + img_size:
                        return "b"
        pg.display.update()
    return "q"

def getEvalPercentFull(eval):
    if eval == -1000:
        return 1
    if eval == 1000:
        return 0
    if eval > 10:
        return 0.05
    if eval < -10:
        return 0.95
    if eval < 0:
        return 0.5 + math.sqrt(-eval/62.5)
    else:
        return 0.5 - math.sqrt(eval/62.5)

def getEvalText(eval):
    font = pg.font.SysFont(None, 30)
    if eval == 1000:
        return font.render("M+", True, BLACK)
    if eval == -1000:
        return font.render("M-", True, WHITE)
    if eval < 0:
        return font.render(str(eval), True, WHITE)
    if eval > 0:
        return font.render (f"+{eval}", True, BLACK)
    return font.render ("0.0", True, WHITE)

def drawEvalBar(eval_window, eval):
    eval_window.fill(WHITE)
    EVAL_HEIGHT = 600
    EVAL_WIDTH = 100
    BUFFER = 15
    percent_full = getEvalPercentFull(eval)
    bar_height = percent_full * (EVAL_HEIGHT - BUFFER * 2)
    pg.draw.rect(eval_window, BLACK, pg.Rect(BUFFER, BUFFER, EVAL_WIDTH - BUFFER * 2, bar_height))
    pg.draw.rect(eval_window, BLACK, pg.Rect(BUFFER, BUFFER, EVAL_WIDTH - BUFFER * 2, EVAL_HEIGHT - BUFFER * 2), 1)
    pg.draw.rect(eval_window, GREY, pg.Rect(BUFFER, EVAL_HEIGHT/2 - 3, EVAL_WIDTH - BUFFER * 2, 6))
    text = getEvalText(eval)
    if eval <= 0:
        text_offset = -20
    else:
        text_offset = 20
    eval_window.blit(text, (EVAL_WIDTH/2 - text.get_width()/2, EVAL_HEIGHT/2 - text.get_height()/2 + text_offset))
    pg.display.update()

def drawLegalMoves(window, moves):
    box_width = (WIDTH - 30)/8
    box_height = (HEIGHT - 30)/8
    for move in moves:
        x = ((ord(move[2]) - 97) + 0.5) * box_width + 15
        y = HEIGHT - ((int(move[3]) - 0.5) * box_height + 15)
        circle_center = (x, y)
        pg.draw.circle(window, RED, circle_center, box_width/5)

def playerMoveGUI(board, window, curr_eval, whitePlayer, blackPlayer, whiteTimer, blackTimer):
    map = board.piece_map()
    legal_moves = {}
    for move in board.legal_moves:
        uci_move = board.uci(move)
        start_square = uci_move[:2]
        if start_square in legal_moves:
            legal_moves[start_square].append(uci_move)
        else:
            legal_moves[start_square] = [uci_move]
    valid_start_squares = set(legal_moves.keys())
    moved = False
    clock = pg.time.Clock()
    square = ""
    selected = []
    selected_possible_moves = []
    selected_end_squares = []
    while True:
        clock.tick(FPS)
        draw_window(window)
        draw_prev_move(window, board)
        draw_pieces(window, board)
        draw_highlights(window, selected)
        drawLegalMoves(window, selected_possible_moves)
        
        white_time = whiteTimer.get_time_string()
        black_time = blackTimer.get_time_string()
        drawInfoBar(WIN, curr_eval, whitePlayer, blackPlayer, white_time, black_time)         
        
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP:
                x, y = pg.mouse.get_pos()
                square = getSquare(x, y)
                if square in valid_start_squares:
                    selected = [square]
                    selected_possible_moves = legal_moves[square]
                    selected_end_squares = {x[2:4]:(len(x) == 5) for x in selected_possible_moves}
                elif square in selected_end_squares:
                    move = f"{selected[0]}{square}"
                    if selected_end_squares[square]:
                        move += getPromotion(window, board)
                    return board.san(board.parse_uci(move))         
        pg.display.update()           


def getSquare(x, y):
    if not ((15 < x < 735) and (15 < y < 735)):
        return False
    box_width = (WIDTH - 30)/8
    box_height = (HEIGHT - 30)/8
    letter = chr(int((x - 15)//box_width) + 97)
    number = str(int(8 - (y - 15)//box_height))
    return letter + number
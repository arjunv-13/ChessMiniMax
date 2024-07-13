import pygame as pg
import time
import chess
import math


BOARD_BUFFER = 750
WHITE = (255, 255, 255)
GREY = (127, 127, 127)
BLACK = (0, 0, 0)

FPS = 60
WIN = pg.display.set_mode((1000, 750))
pg.init()
font = pg.font.SysFont(None, 80)
pg.display.set_caption("Game Info")

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
    EVAL_HEIGHT = 750
    EVAL_WIDTH = 100
    BUFFER = 15
    percent_full = getEvalPercentFull(eval)
    bar_height = percent_full * (EVAL_HEIGHT - BUFFER * 2)
    pg.draw.rect(eval_window, BLACK, pg.Rect(BOARD_BUFFER + BUFFER, BUFFER, EVAL_WIDTH - BUFFER * 2, bar_height))
    pg.draw.rect(eval_window, BLACK, pg.Rect(BOARD_BUFFER + BUFFER, BUFFER, EVAL_WIDTH - BUFFER * 2, EVAL_HEIGHT - BUFFER * 2), 1)
    pg.draw.rect(eval_window, GREY, pg.Rect(BOARD_BUFFER + BUFFER, EVAL_HEIGHT/2 - 3, EVAL_WIDTH - BUFFER * 2, 6))
    text = getEvalText(eval)
    if eval <= 0:
        text_offset = -20
    else:
        text_offset = 20
    eval_window.blit(text, (BOARD_BUFFER + EVAL_WIDTH/2 - text.get_width()/2, EVAL_HEIGHT/2 - text.get_height()/2 + text_offset))

def drawPlayerNames(window, white_name, black_name):
    LEFT_BUFFER = 100
    VERTICAL_BUFFER = 25
    TOTAL_HEIGHT = 750
    font = pg.font.SysFont(None, 25)
    w = font.render(f"White: {white_name}", True, BLACK)
    b = font.render(f"Black: {black_name}", True, BLACK)
    window.blit(b, (BOARD_BUFFER + LEFT_BUFFER, VERTICAL_BUFFER))
    window.blit(w, (BOARD_BUFFER + LEFT_BUFFER, TOTAL_HEIGHT - VERTICAL_BUFFER - w.get_height()))

def drawPlayerTimes(window, white_time, black_time):
    LEFT_BUFFER = 100
    VERTICAL_BUFFER = 50
    TOTAL_HEIGHT = 750
    font = pg.font.SysFont(None, 25)
    w = font.render(f"White: {white_time}", True, BLACK)
    b = font.render(f"Black: {black_time}", True, BLACK)
    window.blit(b, (BOARD_BUFFER + LEFT_BUFFER, VERTICAL_BUFFER))
    window.blit(w, (BOARD_BUFFER + LEFT_BUFFER, TOTAL_HEIGHT - VERTICAL_BUFFER - w.get_height()))

def drawInfoBar(window, eval, white_name, black_name, white_time, black_time):
    pg.draw.rect(window, WHITE, pg.Rect(BOARD_BUFFER, 0, 250, 750))
    drawEvalBar(window, eval)
    drawPlayerNames(window, white_name, black_name)
    drawPlayerTimes(window, white_time, black_time)
    pg.display.update()

import chess
from eval import evalBoard
import random

DEPTH = 3
CAPTURE_SEARCH = 1
VARIANCE = .1

def capture_quiescence_search(board, max_depth):
    if not max_depth:
        return evalBoard(board)
    
    outcome = board.outcome()
    if outcome:
        if outcome.winner == chess.WHITE:
            return 1000
        elif outcome.winner == chess.BLACK:
            return -1000
        else:
            return 0
    else:
        captures = []
        for move in board.legal_moves:
            if board.is_capture(move):
                captures.append(move)
        if not captures:
            return evalBoard(board)
        turn = board.turn
        if turn:
            max_eval = evalBoard(board)
            for x in captures:         
                board.push(x)
                max_eval = max((capture_quiescence_search(board, max_depth - 1)), max_eval)
                board.pop()
            return max_eval
        else:
            min_eval = evalBoard(board)
            for x in captures:
                board.push(x)
                min_eval = min((capture_quiescence_search(board, max_depth - 1)), min_eval)
                board.pop()
            return min_eval


def search(board, depth, alpha, beta):   

    if depth == 0:
        return capture_quiescence_search(board, CAPTURE_SEARCH)

    outcome = board.outcome()
    if outcome:
        if outcome.winner == chess.WHITE:
            return 1000
        elif outcome.winner == chess.BLACK:
            return -1000
        else:
            return 0
    else:
        turn = board.turn
        lm = board.legal_moves
        if turn:
            max_eval = float("-inf")
            for x in lm:
                board.push(x)
                max_eval = max((search(board, depth - 1, alpha, beta)), max_eval)
                board.pop()
                alpha = max(alpha, max_eval)
                if beta <= alpha:
                   break
            return max_eval
        else:
            min_eval = float("inf")
            for x in lm:
                board.push(x)
                min_eval = min((search(board, depth - 1, alpha, beta)), min_eval)
                board.pop()
                beta = min(beta, min_eval)
                if beta <= alpha:
                    break
            return min_eval

def findBestMove(board):
    moves = {}
    bestMoves = []
    for move in board.legal_moves:
        san = board.san(move)
        board.push(move)
        moves[san] = search(board, DEPTH, float("-inf"), float("inf"))
        board.pop()
    if board.turn:
        bestEval = max(moves.values())
    else:
        bestEval = min(moves.values())
    for move in moves:
        if -VARIANCE < bestEval - moves[move] < VARIANCE:
            bestMoves.append(board.uci(board.parse_san(move)))
    return [random.choice(bestMoves), bestEval]


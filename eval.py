import chess
import time
import numpy as np

WhitePawnValue = np.array([
    [9, 9, 9, 9, 9, 9, 9, 9],
    [2.25, 2.75, 2.75, 2.8, 2.8, 2.75, 2.75, 2.25],
    [1.4, 1.45, 1.5, 1.6, 1.6, 1.5, 1.45, 1.4],
    [1.25, 1.3, 1.3, 1.4, 1.4, 1.3, 1.3, 1.25],
    [1.025, 1.05, 1.05, 1.1, 1.1, 1.05, 1.05, 1.025],
    [1.01, 1.02, 1.02, 1.025, 1.025, 1.02, 1.02, 1.01],
    [1, 1, 1, 1, 1, 1, 1.1, 1.05],
    [0, 0, 0, 0, 0, 0, 0, 0]
])

BlackPawnValue = -WhitePawnValue[::-1]
        
WhiteKnightValue = np.array([
    [1.5, 2.5, 2.6, 2.7, 2.7, 2.6, 2.5, 1.5],
    [2.5, 2.6, 2.7, 2.8, 2.8, 2.7, 2.6, 2.5],
    [2.6, 2.7, 3.1, 3.1, 3.1, 3.1, 2.7, 2.6],
    [2.8, 3, 3.3, 3.4, 3.4, 3.3, 3, 2.8],
    [2.8, 3, 3.3, 3.4, 3.4, 3.3, 3, 2.8],
    [2.6, 2.7, 3.1, 3.1, 3.1, 3.1, 2.7, 2.6],
    [2.5, 2.6, 2.7, 2.8, 2.8, 2.7, 2.6, 2.5],
    [1.5, 2.5, 2.6, 2.7, 2.7, 2.6, 2.5, 1.5],    
])
    
BlackKnightValue = -WhiteKnightValue[::-1]

WhiteBishopValue = np.array([
    [2.5, 2.7, 2.8, 2.8, 2.8, 2.8, 2.7, 2.5],
    [2.7, 2.8, 2.9, 2.9, 2.9, 2.9, 2.8, 2.7],
    [2.8, 2.9, 3, 3, 3, 3, 2.9, 2.8],
    [2.8, 2.95, 3.05, 3.05, 3.05, 3.05, 2.95, 2.8],
    [2.8, 2.95, 3.05, 3.05, 3.05, 3.05, 2.95, 2.8],
    [2.8, 2.9, 3, 3, 3, 3, 2.9, 2.8],
    [2.7, 3, 2.9, 2.9, 2.9, 2.9, 3, 2.7],
    [2.5, 2.7, 2.8, 2.8, 2.8, 2.8, 2.7, 2.5]    
])

BlackBishopValue = -WhiteBishopValue[::-1]

WhiteRookValue = np.array([
    [4.8, 4.8, 5, 5.1, 5.1, 5, 4.8, 4.8],
    [6, 6, 6, 6, 6, 6, 6, 6],
    [4.8, 4.9, 5, 5.1, 5.1, 5, 4.9, 4.8],
    [4.8, 4.9, 5, 5.1, 5.1, 5, 4.9, 4.8],
    [4.8, 4.9, 5, 5.1, 5.1, 5, 4.9, 4.8],
    [4.8, 4.9, 5, 5.1, 5.1, 5, 4.9, 4.8],
    [4.7, 4.9, 5, 5.1, 5.1, 5, 4.9, 4.7],
    [4.8, 4.8, 5, 5.1, 5.1, 5, 4.8, 4.8]   
])
    
"""BlackRookValue = [
    [-x for x in row] for row in WhiteRookValue[::-1]
]"""
BlackRookValue = -WhiteRookValue[::-1]

WhiteQueenValue = np.array([
    [8.6, 8.7, 8.8, 8.9, 8.9, 8.8, 8.7, 8.6],
    [8.7, 8.8, 8.9, 9, 9, 8.9, 8.8, 8.7],
    [8.8, 8.9, 9, 9.1, 9.1, 9, 8.9, 8.8],
    [8.9, 9, 9.1, 9.2, 9.2, 9.1, 9, 8.9],
    [8.9, 9, 9.1, 9.2, 9.2, 9.1, 9, 8.9],
    [8.8, 8.9, 9, 9.1, 9.1, 9, 8.9, 8.8],
    [8.7, 8.8, 8.9, 9, 9, 8.9, 8.8, 8.7],
    [8.6, 8.7, 8.8, 8.9, 8.9, 8.8, 8.7, 8.6],
])
    
BlackQueenValue = -WhiteQueenValue[::-1]

WhiteKingValue = np.array([
    [1000, 1000, 999.9, 999.7, 999.7, 999.9, 1000, 1000],
    [999.9, 999.85, 999.8, 999.7, 999.7, 999.8, 999.85, 999.9],
    [999.8, 999.75, 999.7, 999.6, 999.6, 999.7, 999.75, 999.8],
    [999.7, 999.7, 999.7, 1000, 1000, 999.7, 999.7, 999.7],
    [999.7, 999.7, 999.7, 999.7, 999.7, 999.7, 999.7, 999.7],
    [999.8, 999.75, 999.7, 999.6, 999.6, 999.7, 999.75, 999.8],
    [999.9, 999.85, 999.8, 999.5, 999.5, 999.8, 999.85, 999.9],
    [1000, 1000, 999.9, 999.7, 999.7, 999.9, 1000, 1000],
])
    
"""BlackKingValue = [
    [-x for x in row] for row in WhiteKingValue[::-1]
]"""
BlackKingValue = -WhiteKingValue[::-1]

pieceValues = {"R": WhiteRookValue, "r": BlackRookValue, "N": WhiteKnightValue, "n": BlackKnightValue, "B": WhiteBishopValue, "b": BlackBishopValue, "Q": WhiteQueenValue, "q": BlackQueenValue, "K": WhiteKingValue, "k": BlackKingValue, "P": WhitePawnValue, "p": BlackPawnValue}
#pieceValues = {"r": -5, "n": -3, "b": -3, "q": -9, "k": -100, "p": -1, ".": 0, "R": 5, "N": 3, "B": 3, "Q": 9, "K": 100, "P": 1}


def evalPiece(square, piece):
    row = 7 - square//8
    col = square % 8
    return pieceValues[piece][row, col]
    #return pieceValues[piece]

def toArray(board):
    stringBoard = str(board)
    stringBoard = stringBoard.replace(" ", "")
    stringBoard = stringBoard.replace("\n", "")
    arrayBoard = []
    for i in range(8):
        arrayBoard.append(stringBoard[i * 8: i * 8 + 8])
    return np.array(arrayBoard)

def toArray2(board):
    i = 0
    arrayBoard = np.empty((8, 8), dtype=int)
    while i < 8:
        n = 0
        while n < 8:
            piece = board.piece_at(8 * i + n)
            if piece is not None:
                arrayBoard[7 - i, n] = ord(piece.symbol())
            else:
                arrayBoard[7 - i, n] = ord(".")  # Or any other value to represent an empty square.
            n+= 1
        i+= 1
    return arrayBoard

"""def evalBoard(board):    
    eval = 0
    map = board.piece_map()
    for square in map:
        eval += evalPiece(square, map[square].symbol())
    return eval"""

def evalBoard(board):
    eval = 0
    map = board.piece_map()
    squares = np.array(list(map.keys()))
    pieces = np.array([map[square].symbol() for square in squares])

    # Use NumPy indexing to efficiently evaluate piece values
    eval_func = np.vectorize(evalPiece)
    eval = np.sum(eval_func(squares, pieces))

    return eval

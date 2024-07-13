import chess
import chess.polyglot
import random
import chess.gaviota

def get_opening_move(board):
    with chess.polyglot.open_reader("./openings/baron30.bin") as reader:
        l = [entry for entry in reader.find_all(board)]
    if l:
        return str(random.choice(l).move)
    return None

def get_endgame_move(board):

    start_dtm = None
    with chess.gaviota.open_tablebase("gaviota") as tablebase:
        start_dtm = tablebase.get_dtm(board)
    
        if start_dtm is None:
            return None
        best_move = None
        best_dtm = -1000000
        for move in board.legal_moves:
            board.push(move)
            dtm = tablebase.get_dtm(board)
            if not dtm:
                if board.is_checkmate():
                    board.pop()
                    return str(move)
                board.pop()
                continue
            if dtm > best_dtm:
                best_move = move
                best_dtm = dtm
            board.pop()
        if best_move is None:
            return None
        return str(best_move)

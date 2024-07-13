import chess

def get_movelist(board):
    movelist = []
    while board.move_stack:
        movelist.append(board.uci(board.pop()))
    movelist.reverse()
    for move in movelist:
        board.push_san(move)
    return " ".join(movelist)


def play_game(board):
    while not board.is_game_over():
        for move in board.legal_moves:
            m = move
        #print(board.san(m))
        board.push(m)

board = chess.Board()
play_game(board)
print(get_movelist(board))
#print(board)

board2 = chess.Board("r1bq1rk1/pp1nbppp/2n1p3/2PpP1B1/6QP/2NB4/PPP2PP1/R3K1NR b KQ - 0 9")
print(board2)


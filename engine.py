import chess
from evalOpening import evalOpening
from evalMiddlegame import evalMiddlegame
from evalEndgame import evalEndgame
import random

MIN_DEPTH = 3
DEPTH = MIN_DEPTH
CAPTURE_SEARCH = 3
VARIANCE = 0.1
evalBoard = evalOpening

def order_moves(board):
    lm = board.legal_moves
    special = []
    normal = []
    for move in lm:
        if board.is_capture(move) or board.gives_check(move):
            special.append(move)
        else:
            normal.append(move)
    return special + normal


def viewTree(root, max_depth, depth, file):
    if depth == max_depth:
        return
    
    for child in root.children:
        file.write(f"{' ' * depth * 5}D{depth} {child.white}, Move: , {child.move}, {child.eval}\n")
        viewTree(child, max_depth, depth + 1, file)
    
    return

class moveNode:
    def __init__(self, move, eval, white, board):
        self.move = move
        self.children = []
        self.eval = eval
        self.white = white
    
    def addChild(self, childNode):
        self.children.append(childNode)

    def getEval(self):
        return self.eval
    
    def calcEval(self):
        childEvals = [x.eval for x in self.children]
        try:
            if self.white:
                self.eval = max(childEvals)
            else:
                self.eval = min(childEvals)
        except:
            print(self.move)

def capture_quiescence_search(board, root, max_depth):
    if not max_depth:
        return
    
    outcome = board.outcome()
    if outcome:
        if outcome.winner == chess.WHITE:
            root.eval = 1000
        elif outcome.winner == chess.BLACK:
            root.eval = -1000
        else:
            root.eval = 0
    else:
        captures = []
        for move in board.legal_moves:
            if board.is_capture(move):
                captures.append(move)
        if not captures:
            root.eval = evalBoard(board)
            #print("No captures")
            return
        #print(captures)
        turn = not board.turn
        if turn:
            for x in captures:         
                move = str(chess.Move.from_uci(str(x)))         
                board.push_san(move)
                evaluation = evalBoard(board) if max_depth == 1 else 0
                next = moveNode(move, evaluation, turn, board)
                root.addChild(next)
                (capture_quiescence_search(board, next, max_depth - 1))
                board.pop()
            root.calcEval()
            root.eval = min(root.eval, evalBoard(board))
        else:
            for x in captures:
                move = str(chess.Move.from_uci(str(x)))         
                board.push_san(move)
                evaluation = evalBoard(board) if max_depth == 1 else 0
                next = moveNode(move, evaluation, turn, board)
                root.addChild(next)
                (capture_quiescence_search(board, next, max_depth - 1))
                board.pop()
            root.calcEval()
            root.eval = max(root.eval, evalBoard(board))
        

    return


def search(board, depth, root, alpha, beta):   

    if depth == 0:
        return capture_quiescence_search(board, root, CAPTURE_SEARCH)
    if not root:
        start = True
        root = moveNode(None, 0, board.turn, board)
    else:
        start = False

    outcome = board.outcome()
    if outcome:
        if outcome.winner == chess.WHITE:
            root.eval = 1000
        elif outcome.winner == chess.BLACK:
            root.eval = -1000
        else:
            root.eval = 0
    else:
        turn = not board.turn
        lm = order_moves(board)
        if turn:
            min_eval = float("inf")
            for x in lm:
                move = str(x)         
                board.push(x)
                evaluation = evalBoard(board)# if depth == 1 else 0
                next = moveNode(move, evaluation, turn, board)
                root.addChild(next)
                (search(board, depth - 1, next, alpha, beta))
                board.pop()
                min_eval = min(min_eval, next.eval)
                beta = min(beta, min_eval)
                if beta + VARIANCE <= alpha:
                    break
                
        else:
            max_eval = float("-inf")
            for x in lm:
                move = str(x)       
                board.push(x)
                evaluation = evalBoard(board) if depth == 1 else 0
                next = moveNode(move, evaluation, turn, board)
                root.addChild(next)
                (search(board, depth - 1, next, alpha, beta))
                board.pop()
                max_eval = max(max_eval, next.eval)
                alpha = max(alpha, max_eval)
                if beta + VARIANCE <= alpha:
                   break
                
        root.calcEval()
    if start:
        return root
    
    else:
        return root.eval

def findBestMove(board, ply):
    global evalBoard
    global DEPTH
    num_pieces = len(board.piece_map())
    if ply < 20 or num_pieces > 24:
        evalBoard = evalOpening
    elif ply < 50 or num_pieces > 14:
        evalBoard = evalMiddlegame
    elif num_pieces > 6:
        DEPTH = MIN_DEPTH + 1
        evalBoard = evalEndgame
    else:
        evalBoard = evalEndgame
        DEPTH = MIN_DEPTH + 2
    winning_move = None
    for move in board.legal_moves:
        board.push(move)
        if board.is_checkmate():
            winning_move = str(move)
            board.pop()
            break
        board.pop()
    
    if winning_move:
        if board.turn:
            return [winning_move, 1000, 1000]
        else:
            return [winning_move, -1000, -1000]
            

    treeRoot = search(board, DEPTH, None, float("-inf"), float("inf"))
    f = open("myfile.txt", "w") 
    viewTree(treeRoot, 4, 0, f)
    f.close
    bestMoves = []
    for child in treeRoot.children:
        if -VARIANCE < (child.eval - treeRoot.eval) < VARIANCE:
            bestMoves.append([child.move, round(treeRoot.eval, 3), round(child.eval, 3)])
    return random.choice(bestMoves)


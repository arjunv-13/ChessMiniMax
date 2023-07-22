import chess
from eval import evalBoard
import random

DEPTH = 3
CAPTURE_SEARCH = 1
VARIANCE = 0.001

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
        lm = board.legal_moves
        if turn:
            min_eval = float("inf")
            for x in lm:
                move = str(chess.Move.from_uci(str(x)))         
                board.push(x)
                evaluation = evalBoard(board) if depth == 1 else 0
                next = moveNode(move, evaluation, turn, board)
                root.addChild(next)
                (search(board, depth - 1, next, alpha, beta))
                board.pop()
                min_eval = min(min_eval, next.eval)
                beta = min(beta, min_eval)
                #if beta <= alpha:
                #    break
                
        else:
            max_eval = float("-inf")
            for x in lm:
                move = str(chess.Move.from_uci(str(x)))         
                board.push(x)
                evaluation = evalBoard(board) if depth == 1 else 0
                next = moveNode(move, evaluation, turn, board)
                root.addChild(next)
                (search(board, depth - 1, next, alpha, beta))
                board.pop()
                max_eval = max(max_eval, next.eval)
                alpha = max(alpha, max_eval)
                #if beta <= alpha:
                #   break
                
        root.calcEval()
    if start:
        return root
    
    else:
        return root.eval

def findBestMove(board):
    treeRoot = search(board, DEPTH, None, float("-inf"), float("inf"))
    f = open("myfile.txt", "w") 
    viewTree(treeRoot, 4, 0, f)
    f.close
    bestMoves = []
    for child in treeRoot.children:
        if -VARIANCE < (child.eval - treeRoot.eval) < VARIANCE:
            bestMoves.append([child.move, treeRoot.eval])
    return random.choice(bestMoves)


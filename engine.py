import chess
import chess.polyglot
from evalOpening import evalOpening
from evalMiddlegame import evalMiddlegame
from evalEndgame import evalEndgame
import random

MIN_DEPTH = 1
DEPTH = MIN_DEPTH
CAPTURE_SEARCH = 1
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


def setDepth():
    global MIN_DEPTH
    MIN_DEPTH = 0
    print("Before the game, input some engine parameters.\nFirst, the number of ply that the computer should search. It should be from 1 to 5, inclusive. For best balance, select 3.\n")
    while MIN_DEPTH < 1 or MIN_DEPTH > 5:
        try:
            MIN_DEPTH = int(input("Enter the starting normal depth: "))
            DEPTH = MIN_DEPTH
        except:
            pass
    global CAPTURE_SEARCH
    CAPTURE_SEARCH = -1
    print("\n\nNext, the capture quiescence search depth. This should be from 0 to 4 inclusive with 3 being a good balance.\n")
    while CAPTURE_SEARCH < 0 or CAPTURE_SEARCH > 4:
        try:
            CAPTURE_SEARCH = int(input("Enter the capture search depth: "))
        except:
            pass
    global VARIANCE
    VARIANCE = 0
    print("\n\nNext, the evaluation variance to use when selecting moves. This is the max difference from the best evaluation that the computer will use to select moves. Evaluations are in terms of pawns, so it can be any decimal between 0.01 and 5. 0.1 or 0.2 is recommended for a balance between variability and strength.\n")
    while VARIANCE < 0.01 or VARIANCE > 5:
        try:
            VARIANCE = float(input("Enter the desired eval variance when selecting moves: "))
        except:
            pass    

def setDepthReturn():
    min_depth = 0
    print("Before the game, input some engine parameters.\nFirst, the number of ply that the computer should search. It should be from 1 to 5, inclusive. For best balance, select 3.\n")
    while min_depth < 1 or min_depth > 5:
        try:
            min_depth = int(input("Enter the starting normal depth: "))
        except:
            pass
    capture_search_depth = -1
    print("\n\nNext, the capture quiescence search depth. This should be from 0 to 4 inclusive with 3 being a good balance.\n")
    while capture_search_depth < 0 or capture_search_depth > 4:
        try:
            capture_search_depth = int(input("Enter the capture search depth: "))
        except:
            pass
    variance = 0
    print("\n\nNext, the evaluation variance to use when selecting moves. This is the max difference from the best evaluation that the computer will use to select moves. Evaluations are in terms of pawns, so it can be any decimal between 0.01 and 5. 0.1 or 0.2 is recommended for a balance between variability and strength.\n")
    while variance < 0.01 or variance > 5:
        try:
            variance = float(input("Enter the desired eval variance when selecting moves: "))
        except:
            pass

    return min_depth, capture_search_depth, variance           

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
            return
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


def search(board, depth, root, alpha, beta, capture_search_depth):   

    if depth == 0:
        return capture_quiescence_search(board, root, capture_search_depth)
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
                search(board, depth - 1, next, alpha, beta, capture_search_depth)
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
                search(board, depth - 1, next, alpha, beta, capture_search_depth)
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

def findBestMove(board, main_depth, capture_search_depth, augment_depth, variance):
    with chess.polyglot.open_reader("./openings/baron30.bin") as reader:
        l = [entry for entry in reader.find_all(board)]
    if l:
        return [str(random.choice(l).move), 0, 0]
    ply = board.fullmove_number/2
    num_pieces = len(board.piece_map())
    if ply < 20 or num_pieces > 24:
        evalBoard = evalOpening
    elif ply < 50 or num_pieces > 14:
        evalBoard = evalMiddlegame
    elif num_pieces > 6:
        if augment_depth:
            main_depth += 1
        evalBoard = evalEndgame
    else:
        evalBoard = evalEndgame
        if augment_depth:
            main_depth += 2
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
            

    treeRoot = search(board, main_depth, None, float("-inf"), float("inf"), capture_search_depth)
    bestMoves = []
    for child in treeRoot.children:
        if -variance < (child.eval - treeRoot.eval) < variance:
            bestMoves.append([child.move, round(treeRoot.eval, 3), round(child.eval, 3)])
    return random.choice(bestMoves)


import chess
import time

class moveNode:
    def __init__(self, move, eval, white):
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

            
pieceValues = {"r": -5, "n": -3, "b": -3, "q": -9, "k": -100, "p": -1, ".": 0, "R": 5, "N": 3, "B": 3, "Q": 9, "K": 100, "P": 1}

def toArray(board):
    stringBoard = str(board)
    stringBoard = stringBoard.replace(" ", "")
    stringBoard = stringBoard.replace("\n", "")
    arrayBoard = []
    for i in range(8):
        arrayBoard.append(stringBoard[i * 8: i * 8 + 8])
    return arrayBoard

def evalBoard(board):
    arrayBoard = toArray(board)
    eval = 0
    for row in range(8):
        for col in range(8):
            eval += pieceValues[arrayBoard[row][col]]
    return eval
        

def search(board, depth, root):   

    if depth == 0:
        return 
    if not root:
        start = True
        root = moveNode(None, 0, board.turn)
        print(board.turn)
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
        for x in board.legal_moves:
            move = str(chess.Move.from_uci(str(x)))
            turn = board.turn
            board.push_san(move)
            evaluation = evalBoard(board) if depth == 1 else 0
            next = moveNode(move, evaluation, turn)
            root.addChild(next)
            #print(board)
            (search(board, depth - 1, next))
            board.pop()
        root.calcEval()
    if start:
        return root
    
    else:
        return



#board = chess.Board()
board = chess.Board("1k1r4/pp1b1R2/3q2pp/4p3/2B5/4Q3/PPP2B2/2K5 b - - 0 1")

print(board)
print(evalBoard(board))


treeRoot = search(board, 4, None)
#print(len(treeRoot.children))

print(treeRoot.eval)
"""for child in treeRoot.children:
    print(" 1:", child.eval)
    for grandchild in child.children:
        print("2:", grandchild.eval)"""
print(board.turn)
for child in treeRoot.children:
    if child.eval == treeRoot.eval:
        print(child.move)
print(board)
# Contains all piece classes for chess 3D
from constant import *
from utils import *

board = [[([None] * 8) for row in range(8)] for i in range(2)]
# the board keeps track of the locations of all the pieces
class Piece(object):
    def __init__(self, color, modelPath, pos, node, scale=1):
        # number is so different pieces arent equivalent and can be selected
        # individually
        self.model = loader.loadModel(modelPath)
        self.model.reparentTo(node)
        self.model.setColor(color)
        self.model.setPos(squarePos(pos))
        self.model.setScale(scale)
        self.position = pos
        self.color = None
    def move(self, newCoor):
        # just moves the model to a new spot
        if self.testCollision(newCoor): # test legal later
            print("no collision")
            newPos = tupleToIndex(newCoor)
            origCoor = indexToTuple(self.position)
            print("new Coor:", newCoor, "old Coor:", origCoor)
            # a tuple containing the pieces original location
            board[origCoor[0]][origCoor[1]][origCoor[2]] = None
            print("board1", board)
            board[newCoor[0]][newCoor[1]][newCoor[2]] = self
            print("board2", board)
            # sets old spot on board to None and new to the piece
            self.position = newPos
            self.model.setPos(squarePos(newPos))
            return True
        else:
            return False
    def testCollision(self, curCoor):
        # tests if a piece can move somewhere
        squareVal = board[curCoor[0]][curCoor[1]][curCoor[2]]
        # the object currently located at the board location
        print("squareVal:", squareVal)
        if squareVal == None:
            print("empty space")
            return True
        else:
            if squareVal == self:
                return False
            elif squareVal.color == self.color:
                print("same color:", self.color)
                return False
            else:
                self.takePiece(squareVal)
                print("different color")
                return True
    def takePiece(self, piece):
        # add piece to list of taken pieces and removes from board
        piece.model.removeNode() # call detachNode() to not draw but not delete
        print("piece taken")

class Pawn(Piece):
    def __init__(self, number, color, node, board):
        if color == "black":
            col = BLACKP
            pos = number + 48
            board[0][6][number] = self
        else:
            col = WHITEP
            pos = number + 8
            board[0][1][number] = self
        super(Pawn, self).__init__(col, "models/pawn", pos, node)
        self.color = color

class Rook(Piece):
    def __init__(self, number, color, node, board):
        if color == "black":
            col = BLACKP
            pos = number * 7 + 56
            board[0][7][number * 7] = self
        else:
            col = WHITEP
            pos = number * 7
            board[0][0][number * 7] = self
        super(Rook, self).__init__(col, "models/rook", pos, node)
        self.color = color

class Knight(Piece):
    def __init__(self, number, color, node, board):
        if color == "black":
            col = BLACKP
            pos = number * 5 + 57
            board[0][7][number * 5 + 1] = self
        else:
            col = WHITEP
            pos = number * 5 + 1
            board[0][0][number * 5 + 1] = self
        super(Knight, self).__init__(col, "models/knight", pos, node)
        self.color = color

class Bishop(Piece):
    def __init__(self, number, color, node, board):
        if color == "black":
            col = BLACKP
            pos = number * 3 + 58
            board[0][7][number * 3 + 2] = self
        else:
            col = WHITEP
            pos = number * 3 + 2
            board[0][0][number * 3 + 2] = self
        super(Bishop, self).__init__(col, "models/bishop", pos, node)
        self.color = color
    
class Queen(Piece):
    def __init__(self, color, node, board, scale=1):
        if color == "black":
            col = BLACKP
            pos = 59
            board[0][7][3] = self
        else:
            col = WHITEP
            pos = 3
            board[0][0][3] = self
        super(Queen, self).__init__(col, "models/queen", pos, node, scale)
        self.color = color
    
class King(Piece):
    def __init__(self, color, node, board, scale=1):
        if color == "black":
            col = BLACKP
            pos = 60
            board[0][7][4] = self
        else:
            col = WHITEP
            pos = 4
            board[0][0][4] = self
        super(King, self).__init__(col, "models/king", pos, node, scale)
        self.color = color
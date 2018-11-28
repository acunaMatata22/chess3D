# Contains all piece classes for chess 3D
class Piece(object):
    def __init__(self, color, modelPath, pos, node, scale=1):
        # number is so different pieces arent equivalent and can be selected
        # individually
        self.model = loader.loadModel(modelPath)
        self.model.reparentTo(node)
        self.model.setColor(color)
        self.model.setPos(squarePos(pos))
        self.model.setScale(scale)
        self.position = squarePos(pos)

class Pawn(Piece):
    def __init__(self, number, color, node, board):
        if color == "black":
            col = Chess.blackP
            pos = number + 48
            board[0][6][number] = self
        else:
            col = Chess.whiteP
            pos = number + 8
            board[0][1][number] = self
        super(Pawn, self).__init__(col, "models/pawn", pos, node)

class Rook(Piece):
    def __init__(self, number, color, node, board):
        if color == "black":
            col = Chess.blackP
            pos = number * 7 + 56
            board[0][7][number * 7] = self
        else:
            col = Chess.whiteP
            pos = number * 7
            board[0][0][number * 7] = self
        super(Rook, self).__init__(col, "models/rook", pos, node)

class Knight(Piece):
    def __init__(self, number, color, node, board):
        if color == "black":
            col = Chess.blackP
            pos = number * 5 + 57
            board[0][7][number * 5 + 1] = self
        else:
            col = Chess.whiteP
            pos = number * 5 + 1
            board[0][0][number * 5 + 1] = self
        super(Knight, self).__init__(col, "models/knight", pos, node)

class Bishop(Piece):
    def __init__(self, number, color, node, board):
        if color == "black":
            col = Chess.blackP
            pos = number * 3 + 58
            board[0][7][number * 3 + 2] = self
        else:
            col = Chess.whiteP
            pos = number * 3 + 2
            board[0][0][number * 3 + 2] = self
        super(Bishop, self).__init__(col, "models/bishop", pos, node)
    
class Queen(Piece):
    def __init__(self, color, node, board, scale=1):
        if color == "black":
            col = Chess.blackP
            pos = 59
            board[0][7][3] = self
        else:
            col = Chess.whiteP
            pos = 3
            board[0][0][3] = self
        super(Queen, self).__init__(col, "models/queen", pos, node, scale)
    
class King(Piece):
    def __init__(self, color, node, board, scale=1):
        if color == "black":
            col = Chess.blackP
            pos = 60
            board[0][7][4] = self
        else:
            col = Chess.whiteP
            pos = 4
            board[0][0][4] = self
        super(King, self).__init__(col, "models/king", pos, node, scale)
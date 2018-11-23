# Author: Nicholas Acuna
# Version: 1.0

from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task

def squarePos(num):
    # returns the XY coordinates of the squares for initialization render
    return (num % 8 - 3.5, num // 8, 0)

class Chess(ShowBase):

    vanilla = (0.953, 0.898, 0.671, 1)
    whiteP = (0.941, 0.871, 0.584, 0.99)
    walnut = (.416, 0.263, .177, 1)
    blackP = (0.03, 0.03, 0.03, 1)

    def __init__(self):
        # sets the board
        ShowBase. __init__(self)
        self.loadSquares()
        self.loadPieces()

        self.disableMouse()

        camera.setPos(6, -9, 4)
        camera.setHpr(27, -15, 0)   

    def loadSquares(self):
        # loads the squares of the lower board onto the screen
        self.squares = []

        for i in range(64):
            self.squares.append(loader.loadModel("models/square"))
            self.squares[i].reparentTo(render)
            if (i // 8 + i) % 2 == 0:
                color = Chess.walnut
            else:
                color = Chess.vanilla
            self.squares[i].setColor(color)
            self.squares[i].setPos(squarePos(i))

    def loadP(self, name, color, sqaure):
        # actually adds piece node to render tree
        pass

    def loadPieces(self):
        # loads all of the pieces for the start of the game

        self.pawn = [None] * 16
        for i in range(8):
        # loads all pawns for both sides
            # Loads the vanilla pieces first
            self.pawn[i] = loader.loadModel("models/pawn")
            self.pawn[i].reparentTo(render)
            self.pawn[i].setColor(Chess.whiteP)
            self.pawn[i].setPos(squarePos(i + 8))
            # NOTE: all counting starts with vanilla pieces then walnut
            # Now loads the walnut pieces
            self.pawn[i + 8] = loader.loadModel("models/pawn")
            self.pawn[i + 8].reparentTo(render)
            self.pawn[i + 8].setColor(Chess.blackP)
            self.pawn[i + 8].setPos(squarePos(i + 48))

        self.rook = [None] * 4
        self.knight = [None] * 4
        self.bishop = [None] * 4
        for i in range(2):
        # loads Rooks, Knights, and Bishops
            # Loads vanilla first and walnut after again
            self.rook[i] = loader.loadModel("models/rook")
            self.rook[i].reparentTo(render)
            self.rook[i].setColor(Chess.whiteP)
            self.rook[i].setPos(squarePos(i * 7))
            self.knight[i] = loader.loadModel("models/knight")
            self.knight[i].reparentTo(render)
            self.knight[i].setColor(Chess.whiteP)
            self.knight[i].setPos(squarePos(1 + i * 5))
            self.bishop[i] = loader.loadModel("models/bishop")
            self.bishop[i].reparentTo(render)
            self.bishop[i].setColor(Chess.whiteP)
            self.bishop[i].setPos(squarePos(2 + i * 3))

            self.rook[i + 2] = loader.loadModel("models/rook")
            self.rook[i + 2].reparentTo(render)
            self.rook[i + 2].setColor(Chess.blackP)
            self.rook[i + 2].setPos(squarePos(56 + i * 7))
            self.knight[i + 2] = loader.loadModel("models/knight")
            self.knight[i + 2].reparentTo(render)
            self.knight[i + 2].setColor(Chess.blackP)
            self.knight[i + 2].setPos(squarePos(57 + i * 5))
            self.bishop[i + 2] = loader.loadModel("models/bishop")
            self.bishop[i + 2].reparentTo(render)
            self.bishop[i + 2].setColor(Chess.blackP)
            self.bishop[i + 2].setPos(squarePos(58 + i * 3))

        # finally load the king and queen
        self.king = [None] * 2
        self.queen = [None] * 2
        self.king[0] = loader.loadModel("models/king")
        self.king[0].reparentTo(render)
        self.king[0].setColor(Chess.whiteP)
        self.king[0].setPos(squarePos(4))
        self.king[1] = loader.loadModel("models/king")
        self.king[1].reparentTo(render)
        self.king[1].setColor(Chess.blackP)
        self.king[1].setPos(squarePos(60))
        self.queen[0] = loader.loadModel("models/queen")
        self.queen[0].reparentTo(render)
        self.queen[0].setColor(Chess.whiteP)
        self.queen[0].setPos(squarePos(3))
        self.queen[1] = loader.loadModel("models/queen")
        self.queen[1].reparentTo(render)
        self.queen[1].setColor(Chess.blackP)
        self.queen[1].setPos(squarePos(59))


game = Chess()
game.run()
# Author: Nicholas Acuna
# Version: 1.0

from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task

def squarePos(num):
    return (num % 8 - 3.5, num // 8, 0)

class CHESS3DBOOOIII(ShowBase):
    white = (1, 1, 1, 1)
    black = (0, 0, 0, 1)

    def __init__(self):
        ShowBase. __init__(self)
        self.loadPieces()
        self.loadSquares()

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
                color = black
            else:
                color = white
            self.squares[i].setColor(color)
            self.squares[i].setPos(squarePos(i))

    def loadPieces(self):
        #


        self.pawn = loader.loadModel("models/pawn")
        self.knight = loader.loadModel("models/knight")
        self.queen = loader.loadModel("models/queen")
        self.bishop = loader.loadModel("models/bishop")
        self.king = loader.loadModel("models/king")
        self.rook = loader.loadModel("models/rook")        

        self.pawn.reparentTo(render)
        self.pawn.setColor(white)
        self.pawn.setPos(squarePos(0))

        self.knight.reparentTo(render)
        self.knight.setColor(black)
        self.knight.setPos(squarePos(1))

        self.queen.reparentTo(render)
        self.queen.setColor(white)
        self.queen.setPos(squarePos(2))

        self.bishop.reparentTo(render)
        self.bishop.setColor(black)
        self.bishop.setPos(squarePos(3))

        self.king.reparentTo(render)
        self.king.setColor(white)
        self.king.setPos(squarePos(4))

        self.rook.reparentTo(render)
        self.rook.setColor(black)
        self.rook.setPos(squarePos(5))



game = CHESS3DBOOOIII()
game.run()
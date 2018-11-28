# Author: Nicholas Acuna
# Version: 1.0

from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from panda3d.core import AmbientLight, PointLight, DirectionalLight
from panda3d.core import LightAttrib, TransparencyAttrib, NodePath
from direct.task.Task import Task
from constant import *
from utils import *
from pieces import *
import copy


class Chess(ShowBase):
    # First sets up the colors used throughout the program
    
    def __init__(self):
        # sets the board
        ShowBase.__init__(self)
        # start to set up the board
        self.loadNodes() # loads nodes used for rendering tree
        
        self.squares = []
        self.loadSquares() # loads lower squares onto the render tree to be drawn
        self.loadUpperSquares("start") # loads upper squares onto render tree
        # sets up spaces on the board that keeps track of all pieces
        print(len(self.squares))
        self.selected = [0, 3, 3] # selects the first square
        self.loadSquares(tupleToIndex(self.selected), SELECT) # color starter
        self.highlighted = ([])
        self.selPiece = None
        # is a 8x8x2 3D list
        self.loadPieces() # also loads pieces onto board
        self.loadLights()
        self.disableMouse() # mouse has a janky camera controll
        camera.setPos(6, -9, 4) # sets our view into the enviornment
        camera.setHpr(27, -15, 0)
        contr = Controller(self)

    def selectSquare(self, old):
        oldSquare = tupleToIndex(old) # is now an int
        newSquare = tupleToIndex(self.selected)
        if self.selected[0] == 1:
            # new selected square is on the upper board
            self.loadSquares(newSquare, SELECT)
            if old[0] == 1:
                # make old square look normal
                self.loadSquares(oldSquare, "upper") # old was on upper
            else:
                self.loadSquares(oldSquare)
                self.loadUpperSquares("visible") # means moving to upper so
        else:
            # new selected square is on the lower board
            self.loadSquares(newSquare, SELECT)
            upperT = 0.3
            if old[0] == 1:
                self.loadSquares(oldSquare, "upper")
                self.loadUpperSquares("clear")
            else:
                self.loadSquares(oldSquare)
          
    def loadNodes(self):
        self.lBoard = NodePath("self.lBoard")
        self.lBoard.reparentTo(render)
        self.uBoard = NodePath("self.uBoard")
        self.uBoard.reparentTo(render)        
    def loadLights(self):
        # Loads the lights onto the board
        pointLight = PointLight('pointLight')
        pointLight.setColor(Vec4(.7, .7, .7, 1))
        pLight = render.attachNewNode(pointLight)
        pLight.setPos(-10, -5, 10)
        self.lBoard.setLight(pLight)
        aLight = AmbientLight('aLight')
        aLight.setColor(Vec4(0.4, 0.4, 0.4, 1))
        alnp = render.attachNewNode(aLight)
        render.setLight(alnp)
        dLight = DirectionalLight('dLight')
        dLight.setColor(Vec4(0.7, 0.7, 0.5, 1))
        dlnp = render.attachNewNode(dLight)
        dlnp.setHpr(-80, -80, 0)
        self.lBoard.setLight(dlnp)
    def loadSquares(self, square=None, newColor=None):
        # loads the squares of the lower board onto the screen
        # also can be used to change the color of any single square
        if square == None:
            for i in range(64):
                self.squares.append(loader.loadModel("models/square"))
                if (i // 8 + i) % 2 == 0:
                    color = WALNUT
                else:
                    color = VANILLA
                self.squares[i].setColor(color)
                self.squares[i].setPos(squarePos(i))
                self.squares[i].reparentTo(self.lBoard)
        else:
            if newColor == "upper": # just recoloring upper board square
                if (square // 8 + square) % 2:
                    color = DARKGREY
                else:
                    color = LIGHTGREY
            elif newColor != None:
                color = newColor # on lower board
            elif (square // 8 + square) % 2 == 0: # just recoloring lower square
                color = WALNUT
            else:
                color = VANILLA
            self.squares[square].setColor(color)
    def loadUpperSquares(self, transparency):
        # loads the squares of the lower board onto the screen
        if transparency == "start":
            for i in range(64):
                self.squares.append(loader.loadModel("models/square"))
                if (i // 8 + i) % 2 == 0:
                    color = LIGHTGREY
                else:
                    color = DARKGREY
                self.squares[i + 64].setTransparency(TransparencyAttrib.MAlpha)
                self.squares[i + 64].setColor(color)
                self.squares[i + 64].setPos(squarePos(i + 64))
                self.squares[i + 64].reparentTo(self.uBoard)
        elif transparency == "visible":
            for i in range(64):
                self.squares[i + 64].setTransparency(TransparencyAttrib.MNone)
        elif transparency == "clear":
            for i in range(64):
                self.squares[i + 64].setTransparency(TransparencyAttrib.MAlpha)
    def loadPieces(self):
        # loads all of the pieces for the start of the game

        self.pawn = [None] * 16
        for i in range(8):
        # loads all pawns for both sides
            self.pawn[i] = Pawn(i, "white", self.lBoard, board)
            self.pawn[i + 8] = Pawn(i, "black", self.lBoard, board)

        self.rook = [None] * 4
        self.knight = [None] * 4
        self.bishop = [None] * 4
        for i in range(2):
        # loads Rooks, Knights, and Bishops
            self.rook[i] = Rook(i, "white", self.lBoard, board)
            self.knight[i] = Knight(i, "white", self.lBoard, board)
            self.bishop[i] = Bishop(i, "white", self.lBoard, board)
            
            self.rook[i + 2] = Rook(i, "black", self.lBoard, board)
            self.knight[i + 2] = Knight(i, "black", self.lBoard, board)
            self.bishop[i + 2] = Bishop(i, "black", self.lBoard, board)

        # finally load the king and queen
        self.king = [King("white", self.lBoard, board, 1.19),
                     King("black", self.lBoard, board, 1.19)]
        self.queen = [Queen("white", self.lBoard, board, 1.22),
                      Queen("black", self.lBoard, board, 1.22)]

class Controller(DirectObject):
    def __init__(self, chessObj):
        self.accept('arrow_left', self.selectMove, [0, 0, -1, chessObj])
        self.accept('arrow_right', self.selectMove, [0, 0, 1, chessObj])
        self.accept('arrow_up', self.selectMove, [0, 1, 0, chessObj])
        self.accept('arrow_down', self.selectMove, [0, -1, 0, chessObj])
        self.accept('/', self.selectMove, [1, 0, 0, chessObj])
        self.accept('enter', self.selectPiece, [chessObj])

    def selectMove(self, dx, dy, dz, chessObj):
        selected = chessObj.selected
        old = copy.deepcopy(selected)
        # old so that original selected can be colored
        selected[0] += dx
        selected[1] += dy
        selected[2] += dz
        if selected[0] >= 2:
            selected[0] = 0
        elif selected[1] >= 8:
            selected[1] = 0
        elif selected[1] < 0:
            selected[1] = 7
        elif selected[2] >= 8:
            selected[2] = 0
        elif selected[2] < 0:
            selected[2] = 7
        chessObj.selectSquare(old)

    def selectPiece(self, chessObj):
        if chessObj.selPiece == None:
            height = chessObj.selected[0]
            row = chessObj.selected[1]
            col = chessObj.selected[2]
            chessObj.selPiece = board[height][row][col]
        else:
            pos = tupleToIndex(chessObj.selected)
            chessObj.selPiece.move(pos, chessObj.selected)
            chessObj.selPiece = None

# Not constants and used throughout the module
upperT = .5
DARKGREY = Vec4(0.5, 0.5, 0.5, upperT)
LIGHTGREY = Vec4(0.3, 0.3, 0.3, upperT)

game = Chess()
game.run()
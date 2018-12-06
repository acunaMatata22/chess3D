# Author: Nicholas Acuna
# Version: 1.0

from direct.showbase.ShowBase import ShowBase
from direct.showbase.DirectObject import DirectObject
from panda3d.core import AmbientLight, PointLight, DirectionalLight, TextNode
from panda3d.core import LightAttrib, TransparencyAttrib, NodePath, Point3
from panda3d.core import DynamicTextFont, Fog, TextFont
from direct.gui.OnscreenImage import OnscreenImage
from direct.task.Task import Task
from direct.interval.IntervalGlobal import *
from constant import *
from utils import *
from pieces import *

import copy
import sys
import math


class Chess(ShowBase):
    # First sets up the colors used throughout the program
    
    def __init__(self):
        # sets the board
        ShowBase.__init__(self)
        # self.base = self
        self.setup() # exists so can be reset
    def setup(self):
        # start to set up the board
        self.loadNodes() # loads nodes used for rendering tree
        self.squares = []
        # is a 8x8x2 3D list
        self.loadLights()
        self.disableMouse() # mouse has a janky camera control
        camera.setPos(6, -9, 4) # sets our view into the enviornment
        camera.setHpr(27, -15, 0)
        self.contr = Controller(self)
        self.reset()
    def reset(self):
        self.loadSquares() # loads lower squares onto the render tree to be drawn
        self.loadUpperSquares("start") # loads upper squares onto render tree
        # sets up spaces on the board that keeps track of all pieces
        self.loadPieces() # also loads pieces onto board
        self.selSqrCoor = [0, 3, 3] # coordinates of selected piece/square
        self.loadSquares(tupleToIndex(self.selSqrCoor), SELECT) # color starter
        self.pieceChoice = [0, 1] # [x, y] not [row, col]
        self.legalSquares = [] # any square legal to move onto
        self.highlighted = [] # illustrates possible moves
        self.angle = 0
        self.turn = "white"
        self.selPiece = None
        self.gameMode = "start"
        self.fontTrans = 1
        self.startScreen()
    def drawSelectSquare(self, old):
        # call to recolor the select square and to recolor the previous square
        oldSquare = tupleToIndex(old) # is now an int
        newSquare = tupleToIndex(self.selSqrCoor)
        color = SELECT
        self.loadSquares(newSquare, color)
        if self.selSqrCoor[0] == 1:
            # new selSqrCoor square is on the upper board
            if old[0] == 1:
                # make old square look normal
                self.loadSquares(oldSquare, "upper") # old was on upper
            else:
                # old was on bottom, new is on upper
                self.loadSquares(oldSquare)
                self.loadUpperSquares("visible") # means moving to upper so
        else:
            # new selSqrCoor square is on the lower board
            upperT = 0.25
            if old[0] == 1:
                self.loadSquares(oldSquare, "upper")
                self.loadUpperSquares("clear")
            else:
                self.loadSquares(oldSquare)
    def drawHighlighted(self):
        # wrapper to color blue the squares selected by the user
        for squareCoor in self.highlighted:
            if squareCoor[0] == 1:
                self.loadSquares(tupleToIndex(squareCoor), "upperHigh")
            else:
                self.loadSquares(tupleToIndex(squareCoor), HIGHLIGHT)
    def dehighlight(self):
        # returns all highlighted squares back to normal
        for squareCoor in self.highlighted:
            if squareCoor[0] == 1:
                self.loadSquares(tupleToIndex(squareCoor), "upper")
            else:
                self.loadSquares(tupleToIndex(squareCoor))
        self.highlighted = []

    def loadNodes(self):
        # loads the different parent nodes for lighting
        self.lBoard = NodePath("self.lBoard")
        self.lBoard.reparentTo(render)
        self.uBoard = NodePath("self.uBoard")
        self.uBoard.reparentTo(render)        
    def loadLights(self):
        # Loads the lights onto the board
        pointLight = PointLight('pointLight')
        pointLight.setColor(Vec4(.7, .7, .7, 1))
        self.pLight = render.attachNewNode(pointLight)
        self.pLight.setPos(-10, -5, 10)
        self.lBoard.setLight(self.pLight)
        aLight = AmbientLight('aLight')
        aLight.setColor(Vec4(0.4, 0.4, 0.4, 1))
        self.alnp = render.attachNewNode(aLight)
        render.setLight(self.alnp)
        dLight = DirectionalLight('dLight')
        dLight.setColor(Vec4(0.7, 0.7, 0.5, 1))
        self.dlnp = render.attachNewNode(dLight)
        self.dlnp.setHpr(-80, -80, 0)
        self.lBoard.setLight(self.dlnp)
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
                if (square // 8 + square) % 2 == 0:
                    color = LIGHTGREY
                else:
                    color = DARKGREY
            elif newColor == "upperHigh":
                color = HIGHLIGHT
                print(square, self.selPiece.position)
                self.squares[square].setTransparency(TransparencyAttrib.MAlpha)
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
            self.pawn[i] = Pawn(i, "white", self.lBoard)
            self.pawn[i + 8] = Pawn(i, "black", self.lBoard)

        self.rook = [None] * 4
        self.knight = [None] * 4
        self.bishop = [None] * 4
        for i in range(2):
        # loads Rooks, Knights, and Bishops
            self.rook[i] = Rook(i, "white", self.lBoard)
            self.knight[i] = Knight(i, "white", self.lBoard)
            self.bishop[i] = Bishop(i, "white", self.lBoard)
            
            self.rook[i + 2] = Rook(i, "black", self.lBoard)
            self.knight[i + 2] = Knight(i, "black", self.lBoard)
            self.bishop[i + 2] = Bishop(i, "black", self.lBoard)

        # finally load the king and queen
        self.king = [King("white", self.lBoard, 1.19),
                     King("black", self.lBoard, 1.19)]
        self.queen = [Queen(None, "white", self.lBoard, 1.22),
                      Queen(None, "black", self.lBoard, 1.22)]
        self.newPieces = []
    def checkStraight(self, origZ, origY, origX, dz, dy, dx):
        # checks in straight directions around
        if dz == 0:
            # tests if any pieces are directly north, east, etc
            dirX, dirY = dx, dy
            mult = 1
            while (0 <= origX + dirX <= 7) and (0 <= origY + dirY <= 7) and mult < 3:
                for square in self.highlighted:
                    if [origZ, origY + dirY, origX + dirX] == square:
                        return square
                mult += 1
                dirX = dx * mult
                dirY = dy * mult
        else:
            # tests vertically above/below
            for square in self.highlighted:
                if [origZ + dz, origY, origX] == square:
                    return square
        return None
        
    def checkNextClosestAbove(self, origZ, origY, origX, dz):
        # looks for literal closest square to directly above or below original
        moveX, moveY = 1, 1
        dist = 1 # the distance away from the original square
        solved = False
        while origX + moveX < 8 or origX - moveX > 0 or \
                origY + moveY < 8 or origY - moveY > 0:
            moveX, moveY = dist, dist
            # continues until all squares are checked on the respective board
            for square in self.highlighted:
                # checks the squares around original and see if any are highlighted
                for dirY in range(-dist, dist): # checks the right
                    if [origZ + dz, origY + dirY, origX + dist] == square:
                        solved = True
                for dirX in range(dist, -dist, -1): # checks above
                    if [origZ + dz, origY + dist, origX + dirX] == square:
                        solved = True
                for dirY in range(dist, -dist, -1): # checks to the left
                    if [origZ + dz, origY + dirY, origX - dist] == square:
                        solved = True
                for dirX in range(-dist, dist): # checks below
                    if [origZ + dz, origY - dist, origX + dirX] == square:
                        solved = True
                # now sees if square has been found
                if solved:
                    return square
            dist += 1
        return None
    def checkNextClosest(self, origZ, origY, origX, dy, dx):
        # checks for the closest square in the direction selected
        solved = False
        if dy == 0:
            # check left or right
            yOffset = 1 # offset is perpendicular to direction
            while 0 <= origY + yOffset < 8 or 0 <= origY - yOffset < 8:
                dirMult = 1
                dirX = dx
                while 0 <= origX + dirX < 8:
                    for square in self.highlighted:
                        if [origZ, origY + yOffset, origX + dirX] == square:
                            solved = True
                        elif [origZ, origY - yOffset, origX + dirX] == square:
                            solved = True
                        if solved:
                            return square
                    dirX = dirMult * dx
                    dirMult += 1
                yOffset += 1
        else:
            # check up or down
            xOffset = 1
            while 0 <= origX + xOffset < 8 or 0 <= origX - xOffset < 8:
                dirMult = 1
                dirY = dy
                while 0 <= origY + dirY < 8:
                    for square in self.highlighted:
                        if [origZ, origY + dirY, origX + xOffset] == square:
                            solved = True
                        elif [origZ, origY + dirY, origX - xOffset] == square:
                            solved = True
                        if solved:
                            return square
                    dirY = dirMult * dy
                    dirMult += 1
                xOffset += 1
    def showPromotion(self):
        # shows four images to select what to promote the pawn into
        imgScale = 0.111111
        self.queenImg = OnscreenImage(image = 'images/queen.jpg',
                                        pos = (-.114, 0, .114), scale = imgScale)
        self.rookImg = OnscreenImage(image = 'images/rook.jpg',
                                        pos = (.114, 0, .114), scale = imgScale)
        self.bishopImg = OnscreenImage(image = 'images/bishop.jpg',
                                        pos = (-.114, 0, -.114), scale = imgScale)
        self.knightImg = OnscreenImage(image = 'images/knight.jpg',
                                        pos = (.114, 0, -.114), scale = imgScale)
        self.outlineImg = OnscreenImage(image = 'images/outline.png',
                                        pos = (-.114, 0, .114), scale = imgScale)
        self.outlineImg.setTransparency(TransparencyAttrib.MAlpha)
        if self.selPiece.position > 63: # can't promote to queen on upper board
            self.queenPro = False
        else:
            self.queenPro = True
    def selPromote(self):
        # builds a new piece object
        exitPromo = True
        print("at selPromote, pieceChoice: " + str(self.pieceChoice))
        if self.pieceChoice == [0,0]:
            self.selNewPiece("Bishop", self.lBoard)
        elif self.pieceChoice == [0, 1]:
            if self.queenPro:
                self.selNewPiece("Queen", self.lBoard)
            else:
                self.cantSelect()
                exitPromo = False
        elif self.pieceChoice == [1, 0]:
            self.selNewPiece("Knight", self.lBoard)
        elif self.pieceChoice == [1, 1]:
            self.selNewPiece("Rook", self.lBoard)
        if exitPromo:
            self.queenImg.destroy()
            self.rookImg.destroy()
            self.bishopImg.destroy()
            self.knightImg.destroy()
            self.outlineImg.destroy()
            self.gameMode = "game"
            self.selPiece.model.removeNode()
            self.selPiece = board[self.selSqrCoor[0]][self.selSqrCoor[1]][self.selSqrCoor[2]]
            # tests for checks after the promotion
            self.selPiece.move(self.selSqrCoor, self, True)
            self.selPiece = None
            Controller.selectPiece(self.contr, self)
    def selNewPiece(self, pieceType, node):
        # adds a new piece to the board and game and removes the old
        print("PIECE CHOICE: ", pieceType)
        if pieceType == "Queen":
            self.newPieces.append(Queen(self.selPiece.position,
                self.selPiece.color, node, 1.22, False))
        elif pieceType == "Rook":
            self.newPieces.append(Rook(self.selPiece.position,
                self.selPiece.color, node, implicit=False))
        elif pieceType == "Bishop":
            self.newPieces.append(Bishop(self.selPiece.position,
                self.selPiece.color, node, implicit=False))
        else:
            self.newPieces.append(Knight(self.selPiece.position,
                self.selPiece.color, node, implicit=False))
        z, y, x = self.selSqrCoor[0], self.selSqrCoor[1], self.selSqrCoor[2]
        board[z][y][x] = self.newPieces[-1]
    def cantSelect(self):
        # states a rules so the player doesn't get confused
        cantTxt = TextNode("cantSelect")
        cantTxt.setText("Can't promote to a queen on the top board")
        cantTxt.setAlign(TextNode.ACenter)
        cantTxt.setTextColor((1, 0, 0, 1))
        self.cantPath =  aspect2d.attachNewNode(cantTxt)
        self.cantPath.setScale(0.1)
        self.cantPath.setPos((0, 0, 0))
        taskMgr.doMethodLater(2, self.removeText, "remTxt", extraArgs=[])
    def gameOver(self):
        # shows Game Over text
        gameOverTxt = TextNode("cantSelect")
        gameOverTxt.setText("Game Over")
        gameOverTxt.setAlign(TextNode.ACenter)
        gameOverTxt.setTextColor((1, 0, 0, 1))
        tFont = loader.loadFont('fonts/ariblk.ttf')
        tFont.setPixelsPerUnit(120)
        gameOverTxt.setFont(tFont)
        self.gameOverPath =  aspect2d.attachNewNode(gameOverTxt)
        self.gameOverPath.setScale(0.35)
        self.gameOverPath.setPos((0, 0, 0))
    def removeText(self):
        self.cantPath.removeNode()
    def startScreen(self):
        # load the text and the fog
        self.startText()
        self.fog = Fog('backgroundFog')
        self.setFog(0.1)
        # set up the intervals to initiate when entering the game mode
        self.camPosHprInterv = LerpPosHprInterval(camera, 2, Point3(0, -8, 7),
                                          (0, -32, 0), (6, -9, 4), (27, -15, 0),
                                          blendType='easeInOut')
        self.fogInterv = LerpFunctionInterval(self.setFog, fromData=0.1,
                                                toData=0, duration=2)
        self.txtInterv = LerpFunctionInterval(self.setStartTextColor,
                fromData=1, toData=0, duration=2, extraArgs=[self.startTxt])
        self.fontTrans=0

    def switchSides(self):
        self.switchInt = LerpFunctionInterval(self.moveCamera,
                fromData=self.angle, toData=(self.angle+math.pi), duration=1.2)
        self.switchInt.start()
        self.angle += math.pi
        if self.turn == "white":
            self.turn = "black"
        else: self.turn = "white"
    def moveCamera(self, angle):
        pos = [11.5 * math.sin(angle), 11.5 * math.cos(angle - math.pi) + 3.5, 7]
        hpr = [angle * 180 / math.pi, -32, 0]
        camera.setPosHpr(pos[0], pos[1], pos[2], hpr[0], hpr[1], hpr[2])
    def startText(self):
        # starting text displaying start intructions
        titleTxt = TextNode('introText')
        titleTxt.setText("Jump Chess")
        titleTxt.setAlign(TextNode.ACenter)
        tFont = loader.loadFont('fonts/ariblk.ttf')
        tFont.setPixelsPerUnit(120)
        titleTxt.setFont(tFont)
        titlePath = aspect2d.attachNewNode(titleTxt)
        titlePath.setScale(0.35)
        titlePath.setPos((0, 0, 0))
        authorTxt = TextNode("authorText")
        authorTxt.setText("created by: Nicholas Acuna")
        authorPath = aspect2d.attachNewNode(authorTxt)
        authorPath.setScale(0.1)
        authorPath.setPos((-.2, 0, -0.15))
        instTxt = TextNode("startInst")
        instTxt.setText("Press space to start")
        instTxt.setAlign(TextNode.ACenter)
        instPath =  aspect2d.attachNewNode(instTxt)
        instPath.setScale(0.1)
        instPath.setPos((0, 0, -0.8))
        self.startTxt = [titleTxt, authorTxt, instTxt]
        self.setStartTextColor(self.fontTrans, self.startTxt)
    def setStartTextColor(self, alpha, textNodes):
        for node in textNodes:
            node.setTextColor(1, 1, 1, alpha)
    def setFog(self, density):
        self.fog.setColor(0, 0, 0)
        self.fog.setExpDensity(density)
        self.lBoard.setFog(self.fog)
        self.uBoard.setFog(self.fog)
    def startInt(self):
        self.camPosHprInterv.start()
        self.fogInterv.start()
        self.txtInterv.start()
    def exit(self):
        sys.exit()
class Controller(DirectObject):
    # contains the methods used for acting on user input
    def __init__(self, chessObj):
        # calls a wrapper function that determines effect based on game mode
        self.accept('arrow_left', self.arrowPress, ["left", chessObj])
        self.accept('arrow_right', self.arrowPress, ["right", chessObj])
        self.accept('arrow_up', self.arrowPress, ["up", chessObj])
        self.accept('arrow_down', self.arrowPress, ["down", chessObj])
        self.accept('/', self.selectMove, [1, 0, 0, chessObj])
        self.accept('enter', self.enter, [chessObj])
        self.accept('space', self.space, [chessObj])
        self.accept('shift', self.shift, [chessObj])
        self.accept('r', self.restart, [chessObj])
        self.accept('escape', chessObj.exit)

    def arrowPress(self, dir, chessObj):
        if chessObj.gameMode == "game":
            if chessObj.turn == "white":
                if dir == "left":
                    self.selectMove(0, 0, -1, chessObj)
                elif dir == "right":
                    self.selectMove(0, 0, 1, chessObj)
                elif dir == "up":
                    self.selectMove(0, 1, 0, chessObj)
                elif dir == "down":
                    self.selectMove(0, -1, 0, chessObj)
            else:
                if dir == "left":
                    self.selectMove(0, 0, 1, chessObj)
                elif dir == "right":
                    self.selectMove(0, 0, -1, chessObj)
                elif dir == "up":
                    self.selectMove(0, -1, 0, chessObj)
                elif dir == "down":
                    self.selectMove(0, 1, 0, chessObj)
        elif chessObj.gameMode == "pieceSelection":
            self.changePromotionPiece(chessObj, dir)
    def selectMove(self, dz, dy, dx, chessObj):
        # moves selector square in a direction or selects a move
        selCoor = chessObj.selSqrCoor
        if chessObj.selPiece == None:
            # move selecter square
            old = copy.deepcopy(selCoor)
            # old so that original selSqrCoor can be colored
            selCoor[0] += dz
            selCoor[1] += dy
            selCoor[2] += dx
            if selCoor[0] >= 2: # wrap-around
                selCoor[0] = 0
            elif selCoor[1] >= 8:
                selCoor[1] = 0
            elif selCoor[1] < 0:
                selCoor[1] = 7
            elif selCoor[2] >= 8:
                selCoor[2] = 0
            elif selCoor[2] < 0:
                selCoor[2] = 7
            chessObj.drawSelectSquare(old)
        else:
            z, y, x = selCoor[0], selCoor[1], selCoor[2]
            if z == 1 and dz == 1:
                dz = -1
            # select the most appropriate highlighted square
            newSquare = chessObj.checkStraight(z, y, x, dz, dy, dx)
            if newSquare == None:
                # if reaches here, then looks for next closest square in direction
                if dz == 1 or dz == -1:
                    newSquare = chessObj.checkNextClosestAbove(z, y, x, dz)
                else:
                    newSquare = chessObj.checkNextClosest(z, y, x, dy, dx)
            if newSquare != None:
                chessObj.selSqrCoor = newSquare
                chessObj.highlighted = copy.deepcopy(chessObj.legalSquares)
                chessObj.highlighted.remove(newSquare)
                chessObj.drawSelectSquare(selCoor)
                chessObj.drawHighlighted()
            print(chessObj.selSqrCoor)
    def enter(self, chessObj):
        if chessObj.gameMode == "game":
            self.selectPiece(chessObj)
        elif chessObj.gameMode == "start":
            chessObj.gameMode = "game"
            chessObj.startInt()
        elif chessObj.gameMode == "pieceSelection":
            chessObj.selPromote()
    def space(self, chessObj):
        if chessObj.gameMode == "game":
            if chessObj.selPiece == "none":
                self.selectPiece(chessObj)
            else:
                chessObj.selPiece = None
                chessObj.dehighlight()
                if chessObj.selSqrCoor[0] == 1:
                    chessObj.loadUpperSquares("visible")
        elif chessObj.gameMode == "start":
            chessObj.gameMode = "game"
            chessObj.startInt()
    def shift(self, chessObj):
        if chessObj.gameMode == "game":
            if chessObj.selPiece != "none":
                chessObj.selPiece = None
                chessObj.dehighlight()
                if chessObj.selSqrCoor[0] == 1:
                    chessObj.loadUpperSquares("visible")
    def restart(self, chessObj):
        chessObj.reset()
    def selectPiece(self, chessObj):
        # selecting or moving a piece
        if chessObj.selPiece == None:
            # pick up a piece
            print("pick up piece")
            height = chessObj.selSqrCoor[0]
            row = chessObj.selSqrCoor[1]
            col = chessObj.selSqrCoor[2]
            chessObj.selPiece = board[height][row][col]
            print("..." + str(chessObj.selPiece))
            if chessObj.selPiece != None:
                chessObj.legalSquares = chessObj.selPiece.getSquares([height, row, col])
                chessObj.highlighted = chessObj.legalSquares
                print("Highlighted", chessObj.highlighted)
                chessObj.drawHighlighted()
        else:
            case = chessObj.selPiece.move(chessObj.selSqrCoor, chessObj)
            if case == "promotion":
                chessObj.showPromotion()
                chessObj.gameMode = "pieceSelection"
                chessObj.dehighlight()
                chessObj.switchSides()
            elif case == "success":
                print("moving piece")
                chessObj.selPiece = None
                chessObj.dehighlight()
                if chessObj.selSqrCoor[0] == 1:
                    chessObj.loadUpperSquares("visible")
                chessObj.switchSides()
            elif case == "gameOver":
                chessObj.gameOver()
    def changePromotionPiece(self, chessObj, dir):
        # controlling the popup for promotion
        if dir == "left":
            mDir = [-1, 0]
        elif dir == "right":
            mDir = [1, 0]
        elif dir == "up":
            mDir = [0, 1]
        else:
            mDir = [0, -1]
        chessObj.pieceChoice[0] += mDir[0]
        chessObj.pieceChoice[1] += mDir[1]
        if chessObj.pieceChoice[0] > 1:
            chessObj.pieceChoice[0] = 0
        elif chessObj.pieceChoice[0] < 0:
            chessObj.pieceChoice[0] = 1
        elif chessObj.pieceChoice[1] > 1:
            chessObj.pieceChoice[1] = 0
        elif chessObj.pieceChoice[1] < 0:
            chessObj.pieceChoice[1] = 1
        xMove = chessObj.pieceChoice[0] * 0.228
        yMove = chessObj.pieceChoice[1] * 0.228
        chessObj.outlineImg.setPos(-.114 + xMove, 0, -.114 + yMove)

# Not constants and used throughout the module
upperT = .5
DARKGREY = Vec4(0.5, 0.5, 0.5, upperT)
LIGHTGREY = Vec4(0.3, 0.3, 0.3, upperT)

game = Chess()
game.run()
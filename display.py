import copy
from tetromino import *
pygame.init()

class Window:

    def setDefaultDimensions(self):
        displayWidth = pygame.display.Info().current_w
        displayHeight = pygame.display.Info().current_h
        if displayHeight <= displayWidth:
            self.blockSize = displayHeight // 30
        else:
            self.blockSize = displayWidth // 30
        self.width = 20 * self.blockSize
        self.height = 20 * self.blockSize

    def __init__(self, blockSize = None):
        if (blockSize is not None):
            if isinstance(blockSize, int):
                if blockSize < 6:
                    print("blockSize minimum is 6 because of smallest window limitations")
                    self.blockSize = 6
                else:
                    self.blockSize = blockSize
                self.width = 21 * self.blockSize
                self.height = 20 * self.blockSize
            else:
                print("blockSize value provided is not an int, using default value")
        else:
            self.setDefaultDimensions()

class Draw:

    def __init__(self, window = Window()):
        self.window = window
        self.boardXOffset = 2
        self.heldXOffset = 10 + (self.boardXOffset*2)
        self.heldYOffset = 1
        self.boardWidth = 10 
        self.heldWidth = 4
        self.boardRect = pygame.Rect(self.boardXOffset*self.window.blockSize, 0, self.boardWidth*self.window.blockSize, window.height*self.window.blockSize)
        self.heldRect = pygame.Rect(self.heldXOffset*self.window.blockSize, self.heldYOffset*self.window.blockSize, self.heldWidth*self.window.blockSize, self.heldWidth*self.window.blockSize)

    def createScreen(self):
        self.screen = pygame.display.set_mode((self.window.width, self.window.height))
        pygame.display.set_caption("")

    def getScaledCoords(self, vertexCoords):
        copyCoords = copy.deepcopy(vertexCoords)
        for coord in copyCoords:
            coord[0] = (coord[0] + 2)*self.window.blockSize
            coord[1] = coord[1]*self.window.blockSize
        return copyCoords

    def drawBackground(self, board):
        pygame.draw.rect(self.screen, board.colour, self.boardRect, 3)
        pygame.draw.rect(self.screen, board.colour, self.heldRect, 3)

    def drawGrid(self, board):
        blockSize = self.window.blockSize
        for y in range(int(board.height)):
            for x in range(int(board.width)):
                if board.grid[y][x] != 0:
                    pygame.draw.rect(self.screen, board.grid[y][x], ((x+self.boardXOffset)*blockSize, y*blockSize, blockSize, blockSize))

    def drawHeldPiece(self, board):
        shape = board.heldPiece.shape
        tempPiece = Tetromino(board.heldPiece.shape, 0, board.heldPiece.colour)
        if shape in ("S","Z","I"):
            centreCorrection = 0.5
        elif shape in ("L","J","T"):
            centreCorrection = -0.5
        else:
            centreCorrection = 0
        xOffset = self.heldXOffset - tempPiece.centre[0]
        yOffset = self.heldYOffset + (self.heldWidth/2) + centreCorrection - tempPiece.centre[1]
        tempPiece.incrementCoords(xOffset, yOffset)
        pygame.draw.polygon(self.screen, tempPiece.colour, self.getScaledCoords(tempPiece.vertexCoords))
        pygame.draw.polygon(self.screen, "Black",self.getScaledCoords(tempPiece.vertexCoords), 2)
        

    def drawTetromino(self, tetromino):
        pygame.draw.polygon(self.screen, tetromino.colour, self.getScaledCoords(tetromino.vertexCoords))
        pygame.draw.polygon(self.screen, "Black", self.getScaledCoords(tetromino.vertexCoords), 2)

    def updateDisplay(self, board, tetromino):
        self.board = board
        self.tetromino = tetromino
        pygame.display.update()

    def drawScore(self, board):
        fontSize = int(1.5 * self.window.blockSize)
        awoof = pygame.font.Font("Awoof-Mono-Regular.ttf", fontSize)
        scoreNum = awoof.render(str(board.score), True, (0, 0, 0))
        scoreText = awoof.render("Score", True, (0, 0, 0))
        lineNum = awoof.render(str(board.linesCleared), True, (0, 0, 0))
        lineText = awoof.render("Lines", True, (0, 0, 0))
        scoreYPos = int(board.height*0.33)
        lineYPos = (scoreYPos + 3)
        self.screen.blit(scoreNum, (self.heldXOffset*self.window.blockSize, (scoreYPos+1)*self.window.blockSize))
        self.screen.blit(scoreText, (self.heldXOffset*self.window.blockSize, (scoreYPos)*self.window.blockSize))
        self.screen.blit(lineText, (self.heldXOffset*self.window.blockSize, lineYPos*self.window.blockSize))
        self.screen.blit(lineNum, (self.heldXOffset*self.window.blockSize, (lineYPos+1)*self.window.blockSize))
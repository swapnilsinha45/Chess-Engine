import pygame as p
from Chess import ChessEngine, ChessAI
from multiprocessing import Process, Queue

# Constants
BOARD_WIDTH = BOARD_HEIGHT = 512
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}  # Empty dictionary for images
running = True  # Global variable for game loop
gs = ChessEngine.GameState()
colors = [p.Color("white"), p.Color("gray")]


# Functions
def loadImages():
    image_folder = "C:/Users/swapn/OneDrive/Desktop/Python Chess/Chess/images"
    pieces = ['bB.png', 'bK.png', 'bN.png', 'bp.png', 'bQ.png', 'bR.png',
              'wB.png', 'wK.png', 'wN.png', 'wp.png', 'wQ.png', 'wR.png']
    for piece in pieces:
        name, extension = piece.split('.')
        image_path = f"{image_folder}/{piece}"
        IMAGES[name] = p.transform.scale(p.image.load(image_path), (SQ_SIZE, SQ_SIZE))

def drawGameState(screen, gs, validMoves, sqSelected, moveLogFont):
    drawBoard(screen)
    hightlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)
    drawMoveLog(screen, gs, moveLogFont)

def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                image = IMAGES.get(piece)
                if image is not None:
                    screen.blit(image, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawMoveLog(screen, gs, font):
    
    moveLogRect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color("black"), moveLogRect)
    moveLog = gs.moveLog
    moveTexts = []
    for i in range(0, len(moveLog), 2):
        moveString = str(i//2 + 1) + ". " + str(moveLog[i]) + " "
        if i+1 < len(moveLog):
            moveString += str(moveLog[i+1]) + "  "
        moveTexts.append(moveString)
    movesPerRow = 3
    padding = 5
    lineSpacing = 2
    textY = padding
    for i in range(0,len(moveTexts), movesPerRow):
        text = ""
        for j in range(movesPerRow):
            if i + j < len(moveTexts):
                text += moveTexts[i+j]
        textObject = font.render(text, True, p.Color("white"))
        textLocation = moveLogRect.move(padding, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + lineSpacing

def hightlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            s=p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))



    





def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10
    frameCount = (abs(dR) + abs(dC)) + framesPerSquare
    for frame in range(frameCount + 1):
        r, c = ((move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount))
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.endRow + move.endCol)%2]
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceMoved], endSquare)
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))  
        p.display.flip()
        clock.tick(60)

def drawEndGameText(screen, text):
    font = p.font.SysFont("Arial Narrow", 32, True, False)

    textObject = font.render(text, 0, p.Color('Black'))
    textLocation = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH/2 - textObject.get_width()/2, BOARD_HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)

def popUpMenu(screen, sqSelected):
    font = p.font.SysFont("Arial", 24)
    menuText1 = font.render("Press A to play against AI", True, p.Color('black'))
    menuText2 = font.render("Press H to play against Human", True, p.Color('black'))
    textRect1 = menuText1.get_rect(center=(BOARD_WIDTH // 2, BOARD_HEIGHT // 2 - 20))
    textRect2 = menuText2.get_rect(center=(BOARD_WIDTH // 2, BOARD_HEIGHT // 2 + 20))
    screen.blit(menuText1, textRect1)
    screen.blit(menuText2, textRect2)
    p.display.flip()
    while True:
        for event in p.event.get():
            if event.type == p.KEYDOWN:
                if event.key == p.K_a:  # If 'A' is pressed, play against AI
                    return False
                elif event.key == p.K_h:  # If 'H' is pressed, play against human
                    return True
            elif event.type == p.QUIT:  # Handle quit event
                return False
def main():
    global running, playerTwo
    sqSelected = ()  # Initialize sqSelected
    playerClicks = []
    # Initialize pygame and set up the screen
    try:
        p.init()
        screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
        clock = p.time.Clock()
        screen.fill(p.Color("white"))
        moveLogFont = p.font.SysFont("Arial", 18, False, False)
        gs = ChessEngine.GameState()
        validMoves = gs.getValidMoves()
        moveMade = False
        animate = False
        loadImages()
        gameOver = False
        playerOne = True  # if a human is playing white this will be true
        playerTwo = popUpMenu(screen, sqSelected)  # True if playing against human, False if playing against AI
        AIThinking = False
        moveFinderProcess = None
        moveUndone = False

        while running:
            humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
            for event in p.event.get():
                if event.type == p.QUIT:
                    running = False
                elif event.type == p.MOUSEBUTTONDOWN:
                    if not gameOver:
                        location = p.mouse.get_pos()
                        col = location[0] // SQ_SIZE
                        row = location[1] // SQ_SIZE
                        if sqSelected == (row,col) or col >= 8:  # If no square is selected yet
                            sqSelected = ()
                            playerClicks= []
                        else:  # If a square is already selected
                            sqSelected = (row, col)
                            playerClicks.append(sqSelected)
                        if len(playerClicks) == 2 and humanTurn:
                            move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                            print(move.getChessNotation())
                            for i in range(len(validMoves)):
                                if move == validMoves[i]:
                                    gs.makeMove(validMoves[i])
                                    moveMade = True
                                    animate = True
                                    sqSelected = ()  # Reset sqSelected after making a move
                                    playerClicks = []  # Reset playerClicks for the next move
                            if not moveMade:
                                playerClicks = [sqSelected]
                elif event.type == p.KEYDOWN:
                    if event.key == p.K_z:  # Press z for undo
                        gs.undoMove()
                        moveMade = True
                        animate = False
                        gameOver = False
                        if AIThinking:
                            moveFinderProcess.terminate()
                            AIThinking = False
                        moveUndone = True
                    if event.key == p.K_r: #reset the board
                        gs = ChessEngine.GameState()
                        validMoves = gs.getValidMoves()
                        sqSelected = ()
                        playerClicks = []
                        moveMade = False
                        animate = False
                        gameOver = False
                        if AIThinking:
                            moveFinderProcess.terminate()
                            AIThinking = False
                        moveUndone = True

            #AI move finder
            if not gameOver and not humanTurn and not moveUndone:
                if not AIThinking:
                    AIThinking =True
                    print("thinking...")
                    returnQueue = Queue()
                    moveFinderProcess = Process(target = ChessAI.findBestMove, args=(gs, validMoves, returnQueue))
                    moveFinderProcess.start()
                if not moveFinderProcess.is_alive():
                    print("done thinking")
                    AImove = returnQueue.get()
                    if AImove is None:
                        AImove = ChessAI.findRandomMoves(validMoves)
                    gs.makeMove(AImove)
                    moveMade = True
                    animate = True
                    AIThinking = False

            if moveMade:
                if animate:
                   animateMove(gs.moveLog[-1], screen, gs.board, clock)
                validMoves = gs.getValidMoves()
                moveMade = False
                animate = False
                moveUndone = False

            drawGameState(screen, gs, validMoves, sqSelected, moveLogFont)

            if gs.checkmate:
                gameOver = True
                drawEndGameText(screen, 'Stalemate' if gs.stalemate else 'Black wins by Checkmate' if gs.whiteToMove else 'White wins by Checkmate')
                
                

            p.display.flip()
            clock.tick(MAX_FPS)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        p.quit()


    

if __name__ == "__main__":
    main()


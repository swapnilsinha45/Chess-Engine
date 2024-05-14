# GameState class
class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.moveFunctions = {"p" : self.getPawnMoves,"R" : self.getRookMoves, "B" : self.getBishopMoves, "N" : self.getKnightMoves, "Q" : self.getQueenMoves, "K" : self.getKingMoves}
        self.moveLog = []
        self.whiteToMove = True
        
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)
        self.inCheck = False
        self.pins = []
        self.checks = []
        self.checkmate = False
        self.stalemate = False
        self.enPassantPossible = ()#here we will add coordinates where en passant is possible
        self.enPassantPossibleLog = [self.enPassantPossible]
        self.currentCastlingRights = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.wqs,self.currentCastlingRights.bks, self.currentCastlingRights.bqs)]
        

    def makeMove(self, move, aiMove=False):
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.board[move.startRow][move.startCol] = "--"
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove  # swap players
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

        

        if move.isPawnPromotion:

           promotion_piece = input("select  a piece to promote to (Q, R, B, N)").upper()
             

           self.board[move.endRow][move.endCol] = move.pieceMoved[0] + promotion_piece
        if move.isEnPassantMove:  # Corrected attribute name
            self.board[move.endRow][move.endCol] = '--'
            self.board[move.startRow][move.endCol] = move.pieceCaptured



        
        '''if self.enPassantMove:
            self.board[move.startRow][move.endRow] == "--"'''
        if move.castle:
            if move.endCol - move.startCol == 2:#king side castle
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1]
                self.board[move.endRow][move.endCol + 1] = '--'
            else: #queen side castle
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]
                self.board[move.endRow][move.endCol - 2] = '--'

        self.enPassantPossibleLog.append(self.enPassantPossible)

        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.wqs,self.currentCastlingRights.bks, self.currentCastlingRights.bqs))

       

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove 
            if move.pieceMoved == 'wK':
              self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
              self.blackKingLocation = (move.startRow, move.startCol)

            if move.isEnPassantMove:
                self.board[move.endRow][move.endCol] = '--'
                self.board[move.startRow][move.endCol] = move.pieceCaptured

            self.enPassantPossibleLog.pop()
            self.enPassantPossible = self.enPassantPossibleLog[-1]


            self.castleRightsLog.pop()
            newRights = self.castleRightsLog[-1]
            self.currentCastlingRights = CastleRights(newRights.wks, newRights.wqs, newRights.bks, newRights.bqs)

            if move.castle:
                if move.endCol - move.startCol == 2:#kingside
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
                    self.board[move.endRow][move.endCol - 1] = '--'
                else:#queenside
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = '--'
            
            self.checkmate = False
            self.stalemate = False
            

    

           
            

    def updateCastleRights(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastlingRights.wks = False
            self.currentCastlingRights.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRights.bks = False
            self.currentCastlingRights.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastlingRights.wqs = False
                elif move.startCol == 7:
                    self.currentCastlingRights.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentCastlingRights.bqs = False
                elif move.startCol == 7:
                    self.currentCastlingRights.bks = False

        if move.pieceCaptured == 'wR':
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastlingRights.wqs = False
                elif move.endCol == 7:
                    self.currentCastlingRights.wks = False
        elif move.pieceMoved == 'bR':
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentCastlingRights.bqs = False
                elif move.endCol == 7:
                    self.currentCastlingRights.bks = False
    
    def getValidMoves(self):
        moves = []
        
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        if self.inCheck:
            if len(self.checks) == 1:
                moves = self.getAllPossibleMoves()
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = []
                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1,8):
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i)
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break
                for i in range(len(moves)-1, -1, -1):
                    if moves[i].pieceMoved[1] != 'K':
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove(moves[i])
            else:
                self.getKingMoves(kingRow, kingCol, moves)
        else:
            moves = self.getAllPossibleMoves()

        if len(moves) == 0:
            if self.inCheck == True:
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False
        return moves
    
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)

                        

        return moves

    def getPawnMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
          if self.pins[i][0] == r and self.pins[i][1] == c:
              piecePinned = True
              pinDirection = (self.pins[i][2], self.pins[i][3])
              self.pins.remove(self.pins[i])
              break
        if self.whiteToMove:
            if self.board[r-1][c] == "--":
                if not piecePinned or pinDirection == (-1, 0):
                    moves.append(Move((r, c), (r-1, c), self.board))
                    if r == 6 and self.board[r-2][c] == "--":
                       moves.append(Move((r, c), (r-2, c), self.board))
            if c-1>=0: #to not go outside the board
                if self.board[r-1][c-1][0] == "b":#any black piece
                    if not piecePinned or pinDirection == (-1, -1):
                       moves.append(Move((r, c), (r-1, c-1), self.board))
                elif (r-1, c-1) == self.enPassantPossible:
                    moves.append(Move((r, c), (r-1, c-1), self.board, enPassantPossible = True))
            if c+1<=7:
                if self.board[r-1][c+1][0] == "b":
                    if not piecePinned or pinDirection == (-1, 1):
                      moves.append(Move((r, c), (r-1, c+1), self.board))
                elif (r-1, c+1) == self.enPassantPossible:
                    moves.append(Move((r, c), (r-1, c+1), self.board, enPassantPossible = True))
        else:
            if self.board[r+1][c] == "--":  # Move one square forward if empty
                if not piecePinned or pinDirection == (1, 0):
                 moves.append(Move((r, c), (r+1, c), self.board))
                 if r == 1 and self.board[r+2][c] == "--":  # Move two squares forward from starting position
                    moves.append(Move((r, c), (r+2, c), self.board))
            if c-1 >= 0:  # to not go outside the board
                if self.board[r+1][c-1][0] == "w": 
                    if not piecePinned or pinDirection == (1, -1): # Capture diagonally left
                     moves.append(Move((r, c), (r+1, c-1), self.board))
                elif (r+1, c-1) == self.enPassantPossible:
                    moves.append(Move((r, c), (r+1, c-1), self.board, enPassantPossible = True))
            if c+1 <= 7:  # to not go outside the board
                if self.board[r+1][c+1][0] == "w":  # Capture diagonally right
                    if not piecePinned or pinDirection == (1, 1):
                     moves.append(Move((r, c), (r+1, c+1), self.board))
                elif (r+1, c+1) == self.enPassantPossible:
                    moves.append(Move((r, c), (r+1, c+1), self.board, enPassantPossible = True))
     
#ANIMESH ROOK MOVE DEF
    def getRookMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
          if self.pins[i][0] == r and self.pins[i][1] == c:
              piecePinned = True
              pinDirection = (self.pins[i][2], self.pins[i][3])
              if self.board[r][c][1] == 'Q':
                  self.pins.remove(self.pins[i])
              break
        directions = ((-1,0),(0,-1),(1,0),(0,1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:#friendly piece
                            break
                else:#out of the board
                    break

    def getKnightMoves(self, r, c, moves):
      piecePinned = False
    
      for i in range(len(self.pins)-1, -1, -1):
          if self.pins[i][0] == r and self.pins[i][1] == c:
              piecePinned = True
              
              self.pins.remove(self.pins[i])
              break
      directions = ((-2,1),(-2,-1),(2,-1),(2,1),(-1,-2),(-1,2),(1,-2),(1,2))
      allyColor = 'w' if self.whiteToMove else 'b'
      for d in directions:
        endRow = r + d[0]
        endCol = c + d[1]
        if 0 <= endRow < 8 and 0 <= endCol < 8:
            endPiece = self.board[endRow][endCol]
            if not piecePinned:
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))  # Corrected line


    def getBishopMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1, -1, -1):
          if self.pins[i][0] == r and self.pins[i][1] == c:
              piecePinned = True
              pinDirection = (self.pins[i][2], self.pins[i][3])
              self.pins.remove(self.pins[i])
              break
        direction = ((-1,-1),(-1,1),(1,-1),(1,1))
        enemyColor = 'b' if self.whiteToMove else 'w'
        for d in direction:
            for i in range(1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:#friendly piece
                            break
                else:#out of the board
                    break

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    def getKingMoves(self, r, c, moves):
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
        allyColor = 'w' if self.whiteToMove else 'b'
        for i in range(8):
            endRow = r + rowMoves[i]
            endCol = c + colMoves[i]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                  if allyColor == 'w':
                      self.whiteKingLocation = (endRow, endCol)
                  else:
                      self.blackKingLocation = (endRow, endCol)
                  inCheck, pins, checks = self.checkForPinsAndChecks()
                  if not inCheck:
                     moves.append(Move((r, c), (endRow, endCol), self.board))
                  if allyColor == 'w':
                      self.whiteKingLocation = (r, c)
                  else:
                      self.blackKingLocation = (r, c)
        self.getCastleMoves(r, c, moves, allyColor)


    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        
        # Print initial conditions

        if self.whiteToMove:
            enemyColor = 'b'
            allyColor = 'w'
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = 'w'
            allyColor = 'b'
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        

        
        directions = ((-1, 0),(0, -1),(1, 0),(0, 1),(-1, -1),(-1, 1),(1, -1),(1, 1))
        
        # Print directions


        
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                

                
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    

                    
                    if endPiece[0] == allyColor and endPiece[1] != 'K':
                        if possiblePin == ():
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else:
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        if  (0 <= j <= 3 and type == 'R') or \
                            (4 <= j <= 7 and type == 'B') or \
                            (i == 1 and type == 'p' and ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and  4 <= j <= 5))) or \
                            (type == 'Q') or (i == 1 and type == 'K'):
                            if possiblePin == ():
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else:
                                pins.append(possiblePin)
                                break
                        else:
                            break
                else:
                    break
        knightMoves = ((-2, -1),(-2, 1),(-1, -2),(-1, 2),(1, -2),(1, 2),(2, -1),(2, 1))
        
        # Print knight moves


        
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N':
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))
        
        # Print final results

        
        return inCheck, pins, checks

        
    
    '''def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])'''

    def squareUnderAttack(self, r, c, allyColor):#determine if enemy can attack square r c
        enemyColor = 'w' if allyColor == 'b' else 'b'
        direction =((-1,0),(0,-1),(1,0),(0,1),(-1,-1),(-1,1),(1,-1),(1,1))
        for j in range(len(direction)):
            d = direction[j]
            for i in range(1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor:
                        break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        if  (0 <= j <= 3 and type == 'R') or \
                              (4 <= j <= 7 and type == 'B') or \
                              (i == 1 and type == 'p' and (
                                  (enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and  4 <= j <= 5))) or \
                              (type == 'Q') or (i == 1 and type == 'K'):
                            return True
                        else:
                            break
                else:
                    break
        knightMoves = ((-2,1),(2,1),(-2,-1),(2,-1),(1,2),(1,-2),(-1,2),(-1,-2))
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N':
                    return True
        return False
    

                           




    def getCastleMoves(self, r, c, moves, allyColor):
        inCheck = self.squareUnderAttack(r, c, allyColor)
        if inCheck:
            return
        if (self.whiteToMove and self.currentCastlingRights.wks) or (not self.whiteToMove and self.currentCastlingRights.bks):
            self.getKingsideCastleMoves(r, c, moves, allyColor)
        if (self.whiteToMove and self.currentCastlingRights.wks) or (not self.whiteToMove and self.currentCastlingRights.bqs):
            self.getQueensideCastleMoves(r, c, moves, allyColor)
        
    def getKingsideCastleMoves(self, r, c, moves, allyColor):
        if self.board[r][c+1] == '--' and self.board[r][c+2] == '--' and \
            not self.squareUnderAttack(r, c+1, allyColor) and not self.squareUnderAttack(r,c+2, allyColor):
                moves.append(Move((r, c), (r, c+2), self.board, castle = True))

    def getQueensideCastleMoves(self, r, c, moves, allyColor):
        if self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3] == '--' \
            and not self.squareUnderAttack(r, c-1, allyColor) and not self.squareUnderAttack(r,c-2, allyColor):
                moves.append(Move((r, c), (r, c-2), self.board, castle = True))

class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs



    


# Move class
class Move:
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}                                                                                                                                                                  

    def __init__(self, startSq, endSq, board, enPassantPossible = False, castle = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.isPawnPromotion = (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7)
        self.castle = castle   
        self.isEnPassantMove = enPassantPossible
        if self.isEnPassantMove:
            self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'
        
        self.isCapture = self.pieceCaptured != "--"

        
        
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
      


    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False


    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
    
    def __str__(self):
        if self.castle:
            return "O-O" if self.endCol == 6 else "O-O-O"
        endSquare = self.getRankFile(self.endRow, self.endCol)
        if self.pieceMoved[1] == 'p':
            if self.isCapture:
                return self.colsToFiles[self.startCol] + "x" + endSquare
            else:
                return endSquare
            
        #to do pawn promotion

        moveString = self.pieceMoved[1]
        if self.isCapture:
            moveString += "x"
        return moveString + endSquare
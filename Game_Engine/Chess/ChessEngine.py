class GameState():

    def __init__(self):
        # 2D board
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wK", "wQ", "wB", "wN", "wR"] 
        ]

        self.moveFunctions = {  'P': self.getPawnMoves, 
                                'R': self.getRookMoves, 
                                'N':self.getNightMoves, 
                                'B':self.getBishopMoves,
                                'Q':self.getQueenMoves,
                                'K':self.getKingMoves}

        self.whiteToMove = True
        self.moveLog = []
        self.whiteKing = (7, 4)
        self.blackKing = (0, 4)
        self.inCheck = False
        self.pins = []
        self.checks = []







    def makeMove(self, move):
        """ 
        Takes a move parameter and executes it 
        """
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove         # swap player



    def undoMove(self):
        """ 
        Undo last move 
        """
        if self.moveLog:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove     # switch turns back

            # undo king move
            if move.pieceMoved == "wK":
                self.whiteKing = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKing = (move.startRow, move.startCol)





    def getAllValidMoves(self):
        """ 
        All moves considering checks 
        """
        moves = []
        self.inCheck, self.pins,  self.checks =self.checkForPinsAndCheck()
        kingRow, kingCol = self.whiteKing if self.whiteToMove else self.blackKing
        if self.inCheck:
            if len(self.checks) == 1:
                moves = self.getAllPossibleMoves()
                check = self.checks[0]
                checkRow, checkCol = check[0], check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = []
                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow, checkCol)]
                
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2] * i, kingCol + check[3]*i)
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break
                
                # get rid of moves that don't block check or move king
                for i in range(len(moves)-1,-1,-1):
                    if moves[i].pieceMoved != 'K':
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove(moves[i])
            
            else:
                self.getKingMoves(kingRow, kingCol, moves)
        
        else:
            moves = self.getAllPossibleMoves()
        
        return moves






    def getAllPossibleMoves(self):
        """ 
        All moves without considering checks 
        """
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn  = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
                    
        
        return moves







    def checkForPinsAndCheck(self):
        pins, checks, incheck = [], [], False
        enemyColor, allyColor = ("b","w") if self.whiteToMove else ("w","b")
        startRow, startCol = self.whiteKing if self.whiteToMove else self.blackKing

        # All pieces except knight
        for j, dir in enumerate([(-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]):
            possiblePin = ()
            for i in range(1, 8):
                endRow, endCol = startRow + dir[0] * i, startCol + dir[1] * i 
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1] != "K":
                        if possiblePin == ():
                            possiblePin = (endRow, endCol, dir[0], dir[1])
                        else:
                            break
                    
                    elif endPiece[0] == enemyColor:
                        pieceType = endPiece[1]
                        if  (0 <= j <=3 and pieceType=='R') or (4 <= j <=7  and pieceType=='B') or (i ==1 and pieceType=='P' and ((enemyColor=='w' and 6 <= j <=7) or (enemyColor=='b' and 4<= j <=5))) or (pieceType == 'Q') or (i ==1 and pieceType =='K'):
                            if possiblePin == ():
                                incheck = True
                                checks.append((endRow, endCol, dir[0], dir[1]))
                                break
                            else:
                                pins.append(possiblePin)
                                break
                        else:
                            break
                else:
                    break
        
        # Only knight
        for dir in  [(-2,-1),(-2,1),(2,-1),(2,1),(-1,-2),(-1,2),(1,-2),(1,2)]:
            endRow, endCol = startRow + dir[0], startCol + dir[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == "N":
                    incheck = True
                    checks.append((endRow, endCol, dir[0], dir[1]))
            
        return incheck, pins, checks





        
    def getPawnMoves(self, r, c, moves):
        piecesPinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecesPinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break 

        enemyColor = "b" if self.whiteToMove else "w"
        dir, start = (-1,6 ) if self.whiteToMove else (1,1) 

        if (not piecesPinned or pinDirection == (dir,0)) and r+dir >= 0 and r+dir < len(self.board) and self.board[r+dir][c] == "--":
            moves.append(Move((r,c), (r+dir,c), self.board))

            if r==start and self.board[r+dir*2][c] == "--":
                moves.append(Move((r,c), (r+dir*2,c), self.board))

        for i in [-1,1]:k
            if r+dir >= 0 and r+dir < len(self.board) and c+i >= 0 and c+i < len(self.board[0]):
                if (not piecesPinned or pinDirection == (dir,i)) and self.board[r+dir][c+i][0] == enemyColor:
                    moves.append(Move((r,c), (r+dir,c+i), self.board))

        return moves



    def getRookMoves(self, r, c, moves):
        enemyColor = "b" if self.whiteToMove else "w"
        for dir in [(-1,0),(0,-1),(1,0),(0,1)]:
            for i in range(1, 8):
                endRow, endCol = r + dir[0] * i, c + dir[1] * i
                if 0 <= endRow < 8 and  0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break



    def getNightMoves(self, r, c, moves):
        allyColor = "w" if self.whiteToMove else "b"
        for dir in [(-2,-1),(-2,1),(2,-1),(2,1),(-1,-2),(-1,2),(1,-2),(1,2)]:
            endRow, endCol = r + dir[0], c + dir[1]
            if 0 <= endRow < 8 and  0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r,c), (endRow, endCol), self.board))



    def getBishopMoves(self, r, c, moves):
        enemyColor = "b" if self.whiteToMove else "w"
        for dir in [(-1,-1),(-1,1),(1,1),(1,-1)]:
            for i in range(1, 8):
                endRow, endCol = r + dir[0] * i, c + dir[1] * i
                if 0 <= endRow < 8 and  0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break
    
    
    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r,c, moves)


    def getKingMoves(self, r, c, moves):
        allyColor = "w" if self.whiteToMove else "b"
        for dir in [(-1,-1),(-1,1),(1,1),(1,-1),(-1,0),(0,-1),(1,0),(0,1)]:
            endRow, endCol = r + dir[0], c + dir[1]
            if 0 <= endRow < 8 and  0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r,c), (endRow, endCol), self.board))

            










class Move():

    # map keys to vallues
    rankToRows = { str(x) : 8 - x  for x in range(1,9) }
    rowsToRankds = { v : k for k, v in rankToRows.items() }

    filesToCols = { chr(97+x) : x  for x in range(8)}
    colsToFiles = { v : k for k, v in filesToCols.items() }



    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol] 
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol


    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
            

    
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)



    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRankds[r]
    


    
    
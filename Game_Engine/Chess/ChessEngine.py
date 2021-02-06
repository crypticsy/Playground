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




    """ 
    Takes a move parameter and executes it 
    """
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove         # swap player



    """ 
    Undo last move 
    """
    def undoMove(self):
        if self.moveLog:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove     # switch turns back



    """ 
    All moves considering checks 
    """
    def getAllValidMoves(self):
        return self.getAllPossibleMoves()



    """ 
    All moves without considering checks 
    """
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn  = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
                    
        
        return moves




    def getPawnMoves(self, r, c, moves):
        valid = "b" if self.whiteToMove else "w"
        dir, start = (-1,6 ) if self.whiteToMove else (1,1) 

        if r+dir >= 0 and r+dir < len(self.board) and self.board[r+dir][c] == "--":
            moves.append(Move((r,c), (r+dir,c), self.board))

            if r==start and self.board[r+dir*2][c] == "--":
                moves.append(Move((r,c), (r+dir*2,c), self.board))

        for i in [-1,1]:
            if r+dir >= 0 and r+dir < len(self.board) and c+i >= 0 and c+i < len(self.board[0]):
                if self.board[r+dir][c+i][0] == valid:
                    moves.append(Move((r,c), (r+dir,c+i), self.board))

        return moves


    def getRookMoves(self, r, c, moves):
        pass


    def getNightMoves(self, r, c, moves):
        pass


    def getBishopMoves(self, r, c, moves):
        pass
    
    
    def getQueenMoves(self, r, c, moves):
        pass


    def getKingMoves(self, r, c, moves):
        pass






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
    


    
    
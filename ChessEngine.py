"""
"""

class Chess:
    def __init__(self, _board=None):
        """Initializes the starting conditions of a chess game."""
        self.check = False
        self.whiteTurn = True
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--","--","--","--","--","--"],
            ["--", "--", "--","--","--","--","--","--"],
            ["--", "--", "--","--","--","--","--","--"],
            ["--", "--", "--","--","--","--","--","--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.moveLog = []
        self.moveFunctions = {
            'P': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves, 
            'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves
        }
        self.wK_location = (7, 4)
        self.bK_location = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.enpassantCoords = () # this updates whenever a pawn advances 2 squares in one move
        self.castlingRights = Castle(True, True, True, True) # game starts off with castle available on all sides
        self.castleRightsLog = [Castle(self.castlingRights.wKside, self.castlingRights.wQside, self.castlingRights.bKside, self.castlingRights.bQside)]



    def make_move(self, move):
        """Moves a piece."""
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.startPiece
        self.moveLog.append(move)
        self.whiteTurn = not self.whiteTurn

        # track king's location
        if move.startPiece == 'wK':
            self.wK_location = (move.endRow, move.endCol)
        elif move.startPiece == 'bK':
            self.bK_location = (move.endRow, move.endCol)
        
        # check for pawn promotion
        if move.pawnPromotion:
            self.board[move.endRow][move.endCol] = move.startPiece[0] + 'Q'

        # enpassant move, pawn is captured
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = "--" 
        
        # update enpassant coords if last pawn move was 2 square advance
        if move.startPiece[1] == "P" and abs(move.startRow - move.endRow) == 2:
            self.enpassantCoords = ((move.startRow + move.endRow)//2, move.startCol)
        # any other move resets en passant possibility
        else:
            self.enpassantCoords = ()

        # castle move
        if move.isCastle:
            # kingside castle, king moves to the right
            if move.endCol - move.startCol == 2:
                # place rook to king's left, remove rook from original position
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1]
                self.board[move.endRow][move.endCol+1] = "--"
            # queenside castle, king moves to the left
            else:
                # place rook to king's right, remove rook from original position
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2]
                self.board[move.endRow][move.endCol-2] = "--"

        # update castle rights if a king or rook piece moves
        self.updateCastleRights(move)
        self.castleRightsLog.append(Castle(self.castlingRights.wKside, self.castlingRights.wQside, self.castlingRights.bKside, self.castlingRights.bQside))

    def updateCastleRights(self, move):
        """Updates castling rights after a move."""
        if move.startPiece == 'wK':
            self.castlingRights.wKside = False
            self.castlingRights.wQside = False
        elif move.startPiece == 'bK':
            self.castlingRights.bKside = False
            self.castlingRights.bQside = False
        elif move.startPiece == 'wR':
            if move.startRow == 7:
                # left white rook
                if move.startCol == 0:
                    self.castlingRights.wQside = False
                # right white rook
                elif move.startCol == 7:
                    self.castlingRights.wKside = False
        elif move.startPiece == 'bR':
            if move.startRow == 0:
                # left black rook
                if move.startCol == 0:
                    self.castlingRights.bQside = False
                # right black rook
                elif move.startCol == 7:
                    self.castlingRights.bKside = False

    def undo_move(self):
        """A 'takeback' similar to Lichess."""

        # moveLog must be populated for a move to be undone
        if self.moveLog:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.startPiece
            self.board[move.endRow][move.endCol] = move.endPiece
            self.whiteTurn = not self.whiteTurn
            if move.startPiece == 'wK':
                self.wK_location = (move.startRow, move.startCol)
            elif move.startPiece == 'bK':
                self.bK_location = (move.startRow, move.startCol)

            # undo enpassant
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = "--"
                self.board[move.startRow][move.endCol] = move.endPiece
                self.enpassantCoords = (move.endRow, move.endCol)
            
            # undo 2 square pawn advance
            if move.startPiece[1] == "P" and abs(move.startRow - move.endRow) == 2:
                self.enpassantCoords = ()

            # undo castle rights
            self.castleRightsLog.pop()
            # revert castle rights to most recent one
            self.castlingRights.wKside = self.castleRightsLog[-1].wKside
            self.castlingRights.wQside = self.castleRightsLog[-1].wQside
            self.castlingRights.bKside = self.castleRightsLog[-1].bKside
            self.castlingRights.bQside = self.castleRightsLog[-1].bQside
            
            # undo castle move
            if move.isCastle:
                # kingside castle
                if move.endCol - move.startCol == 2:
                    # place the rook and king back in original position
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol-1] = "--"
                # queenside castle
                else:
                    self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1] = "--"
                    
    def validMoves(self):
        """All moves possible when taking opposing 'check' into consideration."""
        temp = self.enpassantCoords
        tempCastle = Castle(self.castlingRights.wKside, self.castlingRights.wQside, self.castlingRights.bKside, self.castlingRights.bQside)
        # 1. generate all possible moves
        tryMoves = self.possibleMoves()
        if self.whiteTurn:
            self.getCastleMoves(self.wK_location[0], self.wK_location[1], tryMoves)
        else:
            self.getCastleMoves(self.bK_location[0], self.bK_location[1], tryMoves)

        # 2. try each move
        for i in range(len(tryMoves)-1, -1, -1):
            self.make_move(tryMoves[i])
    
        # 3. generate opponent's moves
        # 4. if any of opponent's moves attack the king,
        # 5. the move tried in step 2 is invalid
            self.whiteTurn = not self.whiteTurn
            if self.inCheck():
                    tryMoves.remove(tryMoves[i])

            self.whiteTurn = not self.whiteTurn
            self.undo_move()

        # check for checkmate / stalemate conditions
        # if there are no valid moves, a stalemate or checkmate has occurred
        if len(tryMoves) == 0:
            if self.inCheck():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False

        self.enpassantCoords = temp
        self.castlingRights = tempCastle
        return tryMoves

    def possibleMoves(self):
        """All moves possible for a side without considering opposing 'check'."""
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]
                piece = self.board[row][col][1]

                # empty squares do not have turn/color character
                # if white's turn, look at all white's pieces
                # if black's turn, look at all black's pieces
                if (turn == 'w' and self.whiteTurn) or (turn == 'b' and not self.whiteTurn):
                    self.moveFunctions[piece](row, col, moves)
        return moves

    def inCheck(self):
        """Return if a side is in check."""

        # if it's white's turn and the white king is under attack, returns True
        if self.whiteTurn:
            return self.squareUnderAtk(self.wK_location[0], self.wK_location[1])
        # same for black
        else:
            return self.squareUnderAtk(self.bK_location[0], self.bK_location[1])

    def squareUnderAtk(self, row, col):
        # visit opponent's moves
        self.whiteTurn = not self.whiteTurn
        oppMoves = self.possibleMoves()

        # switch back to proper turn
        self.whiteTurn = not self.whiteTurn

        # check if opponent's moves attack the input piece
        for move in oppMoves:
            if move.endRow == row and move.endCol == col:
                return True
        

    def getPawnMoves(self, row, col, moves):
        # generate white pawn moves
        # white pawns start on row 6, moves up the board (decrease rows)
        if self.whiteTurn:
            # white pawn can move directly one square ahead
            if self.board[row-1][col] == "--":
                moves.append(Move((row, col), (row-1, col), self.board))

                # determined one square ahead is clear, check if pawn can advance two squares
                # only valid for starting position of white pawn (row 6)
                if row == 6 and self.board[row-2][col] == "--":
                    moves.append(Move((row, col), (row-2, col), self.board))

            # white pawn can capture diagonally
            if col < 7:
                if self.board[row-1][col+1][0] == "b":
                    moves.append(Move((row, col), (row-1, col+1), self.board))
                # en passant capture
                elif (row-1, col+1) == self.enpassantCoords:
                    moves.append(Move((row, col), (row-1, col+1), self.board, isEnpassantMove=True))

            if col > 0:
                if self.board[row-1][col-1][0] == "b":
                    moves.append(Move((row, col), (row-1, col-1), self.board))
                # en passant capture
                elif (row-1, col-1) == self.enpassantCoords:
                    moves.append(Move((row, col), (row-1, col-1), self.board, isEnpassantMove=True))

        # generate black pawn moves
        # black pawns start on row 1, moves down the board (increase rows)
        else:
            # black pawn can move directly one square ahead
            if self.board[row+1][col] == "--":
                moves.append(Move((row, col), (row+1, col), self.board))

                # determined one square ahead is clear, check if pawn can advance two squares
                # only valid for starting position of black pawn (row 1)
                if row == 1 and self.board[row+2][col] == "--":
                    moves.append(Move((row, col), (row+2, col), self.board))
            
            # black pawn can capture diagonally
            if col < 7:
                if self.board[row+1][col+1][0] == "w":
                    moves.append(Move((row, col), (row+1, col+1), self.board))
                # en passant capture
                elif (row+1, col+1) == self.enpassantCoords:
                    moves.append(Move((row, col), (row+1, col+1), self.board, isEnpassantMove=True))

            if col > 0:
                if self.board[row+1][col-1][0] == "w":
                    moves.append(Move((row, col), (row+1, col-1), self.board))
                # en passant capture
                elif (row+1, col-1) == self.enpassantCoords:
                    moves.append(Move((row, col), (row+1, col-1), self.board, isEnpassantMove=True))
            
        return moves


    def getRookMoves(self, row, col, moves):
        rookColor = self.board[row][col][0]

        # up, down, left, and right moves
        rookMoves = ((-1, 0), (1, 0), (0, -1), (0, 1))
        for move in rookMoves:
            endRow = row + move[0]
            endCol = col + move[1]

            while 0 <= endRow <= 7 and 0 <= endCol <= 7:
                endPiece = self.board[endRow][endCol]
                # rook stops traversing in a direction if it encounters an ally piece
                if rookColor == endPiece[0]:
                    break
                
                elif rookColor != endPiece[0]:
                    # rook can continue traversing if it encounters empty squares
                    if endPiece[0] == "-":
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                    else:
                        # rook encounters an enemy piece, that is the last stop in its traversal
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                        break

                endRow += move[0]
                endCol += move[1]
        
        return moves


    def getKnightMoves(self, row, col, moves):
        knightColor = self.board[row][col][0]

        # horizontal L-move: 1 row change & 2 column changes
        # vertical L-move: 2 row changes & 1 column change
        knightMoves = ((-1, -2), (-1, 2), (1, -2), (1, 2), (2, 1), (2, -1), (-2, 1), (-2, -1))
        for move in knightMoves:
            endRow = row + move[0]
            endCol = col + move[1]

            # if move is within bounds,
            if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                endPiece = self.board[endRow][endCol]

                # move is valid if end piece is empty or not same color as knight
                if knightColor != endPiece[0]:
                    moves.append(Move((row, col), (endRow, endCol), self.board))

        return moves

    def getBishopMoves(self, row, col, moves):
        bishopColor = self.board[row][col][0]

        # up-left, up-right, down-left, down-right (diagonal moves)
        bishopMoves = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        for move in bishopMoves:
            endRow = row + move[0]
            endCol = col + move[1]

            while 0 <= endRow <= 7 and 0 <= endCol <= 7:
                endPiece = self.board[endRow][endCol]
                # bishop stops traversing in a direction if it encounters an ally piece
                if bishopColor == endPiece[0]:
                    break

                elif bishopColor != endPiece[0]:
                    # bishop can continue traversing if it encounters empty squares
                    if endPiece[0] == "-":
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                    else:
                        # bishop encounters an enemy piece, that is the last stop in its traversal
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                        break

                endRow += move[0]
                endCol += move[1]


    def getQueenMoves(self, row, col, moves):
        # queen has combined moves of bishop moves and rook moves
        self.getBishopMoves(row, col, moves)
        self.getRookMoves(row, col, moves)

    def getKingMoves(self, row, col, moves):
        kingColor = self.board[row][col][0]

        kingMoves = ((-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1))
        for move in kingMoves:
            endRow = row + move[0]
            endCol = col + move[1]

            # if move is within bounds,
            if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                endPiece = self.board[endRow][endCol]

                # move is valid if end piece is empty or not same color as king
                if kingColor != endPiece[0]:
                    moves.append(Move((row, col), (endRow, endCol), self.board))

        return moves

    def kingsideCastle(self, row, col, moves):
        """Generate kingside castle move."""

        # king -> rook path must be empty
        if self.board[row][col+1] == "--" and self.board[row][col+2] == "--":
            # squares in that path cannot be under attack
            if not self.squareUnderAtk(row, col+1) and not self.squareUnderAtk(row, col+2):
                moves.append(Move((row, col), (row, col+2), self.board, isCastle=True))

    def queensideCastle(self, row, col, moves):
        """Generate queenside castle move."""

        # king -> rook path must be empty, extra square for queenside castle
        if self.board[row][col-1] == "--" and self.board[row][col-2] == "--" and self.board[row][col-3] == "--":
            # squares in that path cannot be under attack
            if not self.squareUnderAtk(row, col-1) and not self.squareUnderAtk(row, col-2):
                moves.append(Move((row, col), (row, col-2), self.board, isCastle=True))

    def getCastleMoves(self, row, col, moves):
        # can't castle if in check
        if self.squareUnderAtk(row, col):
            return

        # determine if kingside castle is available
        if (self.whiteTurn and self.castlingRights.wKside) or (not self.whiteTurn and self.castlingRights.bKside):
            self.kingsideCastle(row, col, moves)
        
        # determine if queenside castle is available
        if (self.whiteTurn and self.castlingRights.wQside) or (not self.whiteTurn and self.castlingRights.bQside):
            self.queensideCastle(row, col, moves)

    


class Move:
    rowsToRanks = {k:str(abs(8-k)) for k in range(8)}
    colsToFiles = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

    ranksToRows = {v:k for k,v in rowsToRanks.items()}
    filesToCols = {v:k for k,v in colsToFiles.items()}

    def __init__(self, startSq, endSq, board, isEnpassantMove=False, isCastle=False):
        self.startRow = startSq[0]
        self.startCol= startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.startPiece = board[self.startRow][self.startCol]
        self.endPiece = board[self.endRow][self.endCol]
        self.moveID = self.chessNotation(startSq, endSq)
        self.pawnPromotion = (self.startPiece == 'wP' and self.endRow == 0) or (self.startPiece == 'bP' and self.endRow == 7)
        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.endPiece = 'wP' if self.startPiece == 'bP' else 'bP'

        self.isCastle = isCastle

    def chessNotation(self, start, end):
        """Converts index location to chess notation."""
        startRow, startCol = start[0], start[1]
        endRow, endCol = end[0], end[1]
        return self.colsToFiles[startCol] + self.rowsToRanks[startRow] + " -> " + self.colsToFiles[endCol] + self.rowsToRanks[endRow]

    def __eq__(self, other):
        """
        Overrides equalizer for instance of Move object.
        Used to check if Move in validMoves.
        """
        if isinstance(other, Move):
            return other.moveID == self.moveID
        else:
            return False

class Castle:
    """Tracks whether each side can castle or not."""
    def __init__(self, wKside, wQside, bKside, bQside):
        self.wKside = wKside
        self.wQside = wQside
        self.bKside = bKside
        self.bQside = bQside
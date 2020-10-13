import ChessEngine

class Piece:
    """Represents various attributes of a gamepiece."""

    def __init__(self, color, location):
        """Initializes the default attributes of a piece."""
        self.color = color # 'w' or 'b'
        self.location = location # tuple (row, col)

class Pawn(Piece):
    """Represents a pawn piece."""

    def __repr__(self):
        """Displays a pawn piece as its board representation."""
        if self.color == 'w':
            return 'wP'
        else:
            return 'bP'

class Rook(Piece):
    """Represents a rook piece."""

    # def __repr__(self):
    #     """Displays a rook piece as its board representation."""
    #     if self.color == 'w':
    #         return 'wR'
    #     else:
    #         return 'bR'

class Knight(Piece):
    """Represents a knight piece."""

    def __repr__(self):
        """Displays a knight piece as its board representation."""
        if self.color == 'w':
            return 'wN'
        else:
            return 'bN'



class Bishop(Piece):
    """Represents a bishop piece."""

    def __repr__(self):
        """Displays a bishop piece as its board representation."""
        if self.color == 'w':
            return 'wB'
        else:
            return 'bB'


class Queen(Piece):
    """Represents a queen piece."""

    def __repr__(self):
        """Displays a queen piece as its board representation."""
        if self.color == 'w':
            return 'wQ'
        else:
            return 'bQ'

class King(Piece):
    """Represents a king piece."""

    def __repr__(self):
        """Displays a king piece as its board representation."""
        if self.color == 'w':
            return 'wK'
        else:
            return 'bK'




r = Rook('b', (0,0))
print(r)
# game = ChessEngine.Chess()
# p = Pawn('w', (0, 2))
# p.get_moves(game.board) # this will look different each time the board is updated (after a move)
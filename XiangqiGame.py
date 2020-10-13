# Author: Jack Tang
# Date: 3/7/2020
# Description: This program contains a simulation of a Xiangqi game.
#              However, chasing and perpetual checks are not accounted for.


class XiangqiGame:
    """Represents the underlying components of a Xiangqi game."""

    def __init__(self, board=None):
        """Initializes the starting conditions of a Xiangqi game."""
        self._game_state = "UNFINISHED"
        self._turn = "red"
        self._board = [["" for i in range(9)] for j in range(10)]

        # default red pieces
        self._board[0] = [Chariot('red', 'a1'), Horse('red', 'b1'), Elephant('red', 'c1'),
                          Advisor('red', 'd1'), General('red', 'e1'), Advisor('red', 'f1'),
                          Elephant('red', 'g1'), Horse('red', 'h1'), Chariot('red', 'i1')]

        # red soldiers
        self._board[3][0] = Soldier('red', 'a4')
        self._board[3][2] = Soldier('red', 'c4')
        self._board[3][4] = Soldier('red', 'e4')
        self._board[3][6] = Soldier('red', 'g4')
        self._board[3][8] = Soldier('red', 'i4')

        # red cannons
        self._board[2][1] = Cannon('red', 'b3')
        self._board[2][7] = Cannon('red', 'h3')

        # default black pieces
        self._board[9] = [Chariot('black', 'a10'), Horse('black', 'b10'), Elephant('black', 'c10'),
                          Advisor('black', 'd10'), General('black', 'e10'), Advisor('black', 'f10'),
                          Elephant('black', 'g10'), Horse('black', 'h10'), Chariot('black', 'i10')]
        # black soldiers
        self._board[6][0] = Soldier('black', 'a7')
        self._board[6][2] = Soldier('black', 'c7')
        self._board[6][4] = Soldier('black', 'e7')
        self._board[6][6] = Soldier('black', 'g7')
        self._board[6][8] = Soldier('black', 'i7')

        # black cannons
        self._board[7][1] = Cannon('black', 'b8')
        self._board[7][7] = Cannon('black', 'h8')

        # this dictionary will only store locations with pieces,
        # whereas the board will have an empty string for empty positions
        self._locations = {
            # red pieces
            'a1': self._board[0][0],
            'b1': self._board[0][1],
            'c1': self._board[0][2],
            'd1': self._board[0][3],
            'e1': self._board[0][4],
            'f1': self._board[0][5],
            'g1': self._board[0][6],
            'h1': self._board[0][7],
            'i1': self._board[0][8],
            'a4': self._board[3][0],
            'c4': self._board[3][2],
            'e4': self._board[3][4],
            'g4': self._board[3][6],
            'i4': self._board[3][8],
            'b3': self._board[2][1],
            'h3': self._board[2][7],
            # black pieces
            'a10': self._board[9][0],
            'b10': self._board[9][1],
            'c10': self._board[9][2],
            'd10': self._board[9][3],
            'e10': self._board[9][4],
            'f10': self._board[9][5],
            'g10': self._board[9][6],
            'h10': self._board[9][7],
            'i10': self._board[9][8],
            'a7': self._board[6][0],
            'c7': self._board[6][2],
            'e7': self._board[6][4],
            'g7': self._board[6][6],
            'i7': self._board[6][8],
            'b8': self._board[7][1],
            'h8': self._board[7][7],
        }

    def get_game_state(self):
        """Returns state of game."""
        return self._game_state

    def set_game_state(self, color):
        """Updates state of game."""
        self._game_state = color.upper() + "_WON"

    def color_moves(self, color):
        """Returns a list of all possible moves for a team/color."""
        # dict to store piece: [legal moves]
        possible_moves = {}

        # Determine all the legal moves for each piece (value) in self._locations
        for piece in self._locations.values():
            if piece.get_color() == color:
                piece_moves = piece.get_moves(self)
                possible_moves[piece] = piece_moves

        return possible_moves

    def flying_general(self, red_loc, blk_loc):
        """Determines if a flying general scenario exists."""
        same_column = False
        col = ""

        # Flying generals occur in the same column
        if red_loc[1] == blk_loc[1]:
            same_column = True
            col = red_loc[1]
        else:
            return False

        # check each row between the generals' column
        # if any of the rows contain a piece, flying general can't occur
        if same_column is True:
            for i in range(red_loc[0]+1, blk_loc[0]):       # start of range is +1 since we don't need to check
                if self._board[i][col] != "":               # the red general's row
                    return False

        return True

    def is_in_check(self, team_color):
        """Determines if a player is in check."""

        def index_converter(loc):
            """Converts alphanumeric location into row-col indexing format."""
            column_to_index = {
                "a": 0,
                "b": 1,
                "c": 2,
                "d": 3,
                "e": 4,
                "f": 5,
                "g": 6,
                "h": 7,
                "i": 8
            }
            col_letter = loc[0]
            row_num = int(loc[1:])
            row_index = int(row_num) - 1
            col_index = column_to_index[col_letter]
            index_location = [row_index, col_index]
            return index_location

        red_loc = ""
        blk_loc = ""

        # find locations of generals
        # since generals can't be captured, they'll always be in self._locations
        for location, piece in self._locations.items():
            if piece.__repr__() == "General":
                if piece.get_color() == "red":
                    red_loc = location
                else:
                    blk_loc = location

        # convert locations to indexing format
        red_loc = index_converter(red_loc)
        blk_loc = index_converter(blk_loc)

        # determine all possible moves of each team
        red_moves = self.color_moves('red')
        blk_moves = self.color_moves('black')

        # checking if the general is in check
        # if any of the opposite team's moves can target the general,
        # general is in check and return True
        if team_color == 'black':
            for location in red_moves.values():
                if blk_loc in location:
                    return True

        if team_color == 'red':
            for location in blk_moves.values():
                if red_loc in location:
                    return True

        # pass row-col coordinates of both generals to flying_general method
        if self.flying_general(red_loc, blk_loc) is True:
            return True
        
        return False

    def mate(self, color):
        """Determines if team/color has been checkmated or stalemated."""

        def alphanumeric_converter(loc):
            """Converts index location into row-col alphanumeric format."""
            column_to_alphanumeric = {
                0: 'a',
                1: 'b',
                2: 'c',
                3: 'd',
                4: 'e',
                5: 'f',
                6: 'g',
                7: 'h',
                8: 'i'
            }
            row_index = loc[0]
            col_index = loc[1]

            col_alphanum = column_to_alphanumeric[col_index]
            row_alphanum = str(row_index + 1)
            alphanum = col_alphanum + row_alphanum
            return alphanum

        def index_converter(loc):
            """Converts alphanumeric location into row-col indexing format."""
            column_to_index = {
                "a": 0,
                "b": 1,
                "c": 2,
                "d": 3,
                "e": 4,
                "f": 5,
                "g": 6,
                "h": 7,
                "i": 8
            }
            col_letter = loc[0]
            row_num = int(loc[1:])
            row_index = int(row_num) - 1
            col_index = column_to_index[col_letter]
            index_location = [row_index, col_index]
            return index_location

        # get all the team moves for the team to be checked
        escape_moves = self.color_moves(color)

        # convert moves to alphanumeric format
        for piece, moves in escape_moves.items():
            temp = []
            for move in moves:
                temp.append(alphanumeric_converter(move))
            escape_moves[piece] = temp

        # convert escape_moves to {alphanum format: [alphanum moves]}
        new_moves = {self.get_piece_location(k): v for k, v in escape_moves.items()}

        # test the escape moves to see if they can be executed without resulting in check
        legal_moves = []
        for piece, moves in new_moves.items():
            for move in moves:
                old_loc = index_converter(piece)            # convert piece location to row-col index
                old_bd_piece = self.get_piece(old_loc)      # get piece at row-col index
                old_loc_piece = self._locations[piece]      # get piece from self._locations

                new_loc = index_converter(move)             # convert new location to row-col index
                new_bd_piece = self.get_piece(new_loc)      # get new piece, this could be "" or Piece object

                # if the new move is not a key in self._locations (ie. position doesn't contain a piece)
                if move not in self._locations:
                    new_loc_piece = None
                else:
                    # if new move is a key in self._locations,
                    # retrieve the piece
                    new_loc_piece = self._locations[move]

                # try the move
                del self._locations[piece]                          # delete the original key-value pair
                old_bd_piece.change_location(move)                  # change location attribute of piece
                self._locations[move] = old_loc_piece               # add key-value to self._locations
                self._board[old_loc[0]][old_loc[1]] = ""            # remove piece from board
                self._board[new_loc[0]][new_loc[1]] = old_bd_piece  # place piece on new board position

                # check if that move can be executed without resulting in check
                # reverse move regardless of result
                if self.is_in_check(color) is True:
                    self._locations[piece] = old_loc_piece          # placing piece back to its old location
                    if new_loc_piece is not None:                   # if the move captured another piece,
                        self._locations[move] = new_loc_piece       # place that piece back to its original position
                    else:
                        del self._locations[move]                   # otherwise, just delete the key

                    old_bd_piece.change_location(piece)             # change piece's location back to original
                    if new_bd_piece != "":                          # if a piece was captured,
                        new_bd_piece.change_location(move)          # change that piece's location too
                    self._board[old_loc[0]][old_loc[1]] = old_bd_piece
                    self._board[new_loc[0]][new_loc[1]] = new_bd_piece
                else:
                    # found a move that can execute without resulting in check
                    self._locations[piece] = old_loc_piece
                    if new_loc_piece is not None:
                        self._locations[move] = new_loc_piece
                    else:
                        del self._locations[move]

                    old_bd_piece.change_location(piece)
                    if new_bd_piece != "":
                        new_bd_piece.change_location(move)
                    self._board[old_loc[0]][old_loc[1]] = old_bd_piece
                    self._board[new_loc[0]][new_loc[1]] = new_bd_piece

                    # the move escaped check, its not checkmate
                    legal_moves.append(move)

                # if legal_moves contains at least 1 move, game can continue
                if legal_moves:
                    # print("there are still valid moves at play.")
                    return False

        return True

    def get_piece(self, location):
        """Returns piece at location, if location is within boundaries of grid."""
        # returns either the piece object or "" (empty string)
        if 0 <= location[0] <= 9 and 0 <= location[1] <= 8:
            return self._board[location[0]][location[1]]
        else:
            # if location is out of bounds, returns None
            return None

    def get_piece_location(self, piece):
        """Returns alphanumeric location of item."""
        for location, loc_piece in self._locations.items():
            if loc_piece == piece:
                return location

    def reverse_move(self, new, old, new_loc_piece, old_loc_piece, new_bd_piece, old_bd_piece):
        """Reverses a move if move causes same-side check."""

        def index_converter(loc):
            """Converts alphanumeric location into row-col indexing format."""
            column_to_index = {
                "a": 0,
                "b": 1,
                "c": 2,
                "d": 3,
                "e": 4,
                "f": 5,
                "g": 6,
                "h": 7,
                "i": 8
            }
            col_letter = loc[0]
            row_num = int(loc[1:])
            row_index = int(row_num) - 1
            col_index = column_to_index[col_letter]
            index_location = [row_index, col_index]
            return index_location

        old_loc = index_converter(old)
        new_loc = index_converter(new)

        self._locations[old] = old_loc_piece
        if new_loc_piece is not None:
            self._locations[new] = new_loc_piece
        else:
            del self._locations[new]

        if new_bd_piece != "":
            new_bd_piece.change_location(new)

        self._board[old_loc[0]][old_loc[1]] = old_bd_piece
        self._board[new_loc[0]][new_loc[1]] = new_bd_piece

    def make_move(self, old, new):
        """Moves a piece, updates player's turn, and game status."""

        def index_converter(loc):
            """Converts alphanumeric location into row-col indexing format."""
            column_to_index = {
                "a": 0,
                "b": 1,
                "c": 2,
                "d": 3,
                "e": 4,
                "f": 5,
                "g": 6,
                "h": 7,
                "i": 8
            }
            col_letter = loc[0]
            row_num = int(loc[1:])
            row_index = int(row_num) - 1
            col_index = column_to_index[col_letter]
            index_location = [row_index, col_index]
            return index_location

        old_loc = index_converter(old)
        new_loc = index_converter(new)

        if self._game_state != "UNFINISHED":        # game already finished
            # print("game already finished")
            return False
        elif self.get_piece(old_loc) is None or self.get_piece(new_loc) is None:       # position is out of bounds
            # print("position(s) out of bounds")
            return False
        elif self.get_piece(old_loc) == "":         # empty position
            # print("original position doesn't have a piece")
            return False
        elif self._locations[old] is None:          # no piece on old position
            # print("original position doesn't have a piece")
            return False

        # previous conditionals reveal a piece on position
        piece = self.get_piece(old_loc)             # must be a piece object
        new_piece = self.get_piece(new_loc)         # this could be "" or a piece object

        if piece.get_color() != self._turn:         # piece color doesn't match player turn
            # print("piece color doesn't match player's color")
            # print("it's", self._turn, "turn", "but the piece is", piece.get_color())
            return False
        elif new_piece.__repr__() == "General":     # can't capture generals
            # print('cant capture generals')
            return False
        else:
            moves = piece.get_moves(self)       # get the piece's valid moves

        if new_loc not in moves:                # new position not in piece's valid moves
            # print('cant move there')
            return False
        else:
            # remove piece from old position
            # place piece in new position
            old_loc_piece = self._locations[old]    # store the old piece
            if new not in self._locations:          # new position is empty, not a capture
                new_loc_piece = None
            else:
                new_loc_piece = self._locations[new]    # store the new piece if it's being captured

            del self._locations[old]                    # delete piece from locations
            piece.change_location(new)                  # change the piece's location
            self._locations[new] = old_loc_piece        # place piece on new location
            self._board[old_loc[0]][old_loc[1]] = ""    # old board position will always be ""
            self._board[new_loc[0]][new_loc[1]] = piece

        # if move caused same-side check, void move
        if self.is_in_check(self._turn) is True:
            # print('move denied.', self._turn, "still in check")
            self.reverse_move(new, old, new_loc_piece, old_loc_piece, new_piece, piece)
            piece.change_location(old)
            if new_piece != "":
                new_piece.change_location(new)
            return False

        # move is registered, check for endgame conditions
        if self._turn == 'red':
            # print('moved red', piece, 'to', new)

            # check if red's move caused check
            if self.is_in_check('black') is True:
                # print('Black is in check')

                # check if checkmate occurred
                if self.mate('black') is True:
                    # print('Red checkmates black')
                    self.set_game_state('red')
            else:
                # no check occurred, but check for stalemate
                if self.mate('black') is True:
                    # print('Red stalemates black')
                    self.set_game_state('red')

            # game continues, update player turn
            self._turn = 'black'

        else:
            # print('moved black', piece, 'to', new)
            # check if black's move caused check
            if self.is_in_check('red') is True:
                # print('red is in check')

                # check if checkmate occurred
                if self.mate('red') is True:
                    # print('Black checkmates red')
                    self.set_game_state('black')
            else:
                # no check occurred, bu check for stalemate
                if self.mate('red') is True:
                    # print('Black stalemates red')
                    self.set_game_state('black')

            # game continues, update player turn
            self._turn = 'red'

        # end turn
        return True


class Piece:
    """Represents various attributes of a gamepiece."""

    # used to convert alphanumeric notation
    column_to_index = {
        "a": 0,
        "b": 1,
        "c": 2,
        "d": 3,
        "e": 4,
        "f": 5,
        "g": 6,
        "h": 7,
        "i": 8
    }

    def __init__(self, color, location):
        """Initializes the default attributes of a piece."""
        self._color = color
        self._location = location

    def col_to_index(self, loc):
        """Converts column of alphanumeric location to indexing format."""
        column_letter = loc[0]
        column_index = Piece.column_to_index[column_letter]
        return column_index

    def row_to_index(self, loc):
        """Converts column of alphanumeric location to indexing format."""
        row_number = int(loc[1:])
        row_index = int(row_number) - 1
        return row_index

    def get_color(self):
        """Returns team/color of a piece."""
        return self._color

    def change_location(self, new_loc):
        """Updates location of piece after move."""
        self._location = new_loc

    def left(self):
        """Move generator for left-moves. Used with chariot and cannon pieces."""
        row = self.row_to_index(self._location)
        col = self.col_to_index(self._location)
        while col >= 0:
            col -= 1
            yield [row, col]

    def right(self):
        """Move generator for right-moves. Used with chariot and cannon pieces."""
        row = self.row_to_index(self._location)
        col = self.col_to_index(self._location)
        while col <= 8:
            col += 1
            yield [row, col]

    def up(self):
        """Move generator for up-moves. Used with chariot and cannon pieces."""
        row = self.row_to_index(self._location)
        col = self.col_to_index(self._location)
        while row <= 9:
            row += 1
            yield [row, col]

    def down(self):
        """Move generator for down-moves. Used with chariot and cannon pieces."""
        row = self.row_to_index(self._location)
        col = self.col_to_index(self._location)
        while row >= 0:
            row -= 1
            yield [row, col]


class Soldier(Piece):
    """Represents a soldier piece."""

    def __repr__(self):
        """Displays a soldier piece as its Chinese character."""
        if self._color == 'red':
            return '兵'
        else:
            return '卒'

    def get_moves(self, board):
        """Returns a list of valid move based on current location."""
        row = self.row_to_index(self._location)
        col = self.col_to_index(self._location)

        if self._color == 'red':
            temp_moves = [[row + 1, col]]  # default move
            if row > 4:  # soldier crossed river
                temp_moves.append([row, col + 1])  # add horizontal moves
                temp_moves.append([row, col - 1])

        elif self._color == 'black':
            temp_moves = [[row - 1, col]]
            if row < 5:
                temp_moves.append([row, col + 1])
                temp_moves.append([row, col - 1])

        # eliminate out-of-bound moves
        inbound_moves = [move for move in temp_moves if 0 <= move[0] <= 9 and 0 <= move[1] <= 8]

        # eliminate moves that contain friendly pieces
        valid_moves = [move for move in inbound_moves if
                       board.get_piece(move) == "" or
                       board.get_piece(move).get_color() != self._color]

        return valid_moves


class Cannon(Piece):
    """Represents a cannon piece."""

    def __repr__(self):
        """Displays a cannon piece as its Chinese character."""
        if self._color == 'red':
            return '炮'
        else:
            return '砲'

    def get_moves(self, board):
        """Returns a list of valid move based on current location."""

        def cannon_test(left_right_up_down):
            """
            Tests a move from the move generator
            and determine if it's valid.
            Accounts for jumping capture of cannon.
            """
            jumped_over = False
            temp_moves = []

            # generator traverses along column or row
            for generated_move in left_right_up_down:
                current_piece = board.get_piece(generated_move)     # this could be a Piece object, "", or None
                                                                    # if the generated move is out of bounds,
                                                                    # current_piece = None

                # this will be skipped if generator yields empty positions
                # code runs through block if cannon has jumped over a piece
                if jumped_over is True:

                    # skip empty positions behind jumped over piece
                    if current_piece != "" and current_piece is not None:
                        current_piece_color = current_piece.get_color()

                        # detected a piece behind jump
                        # first piece behind jump will end the path
                        if current_piece_color != self._color:
                            temp_moves.append(generated_move)

                        # if it's a friendly piece, end path
                        # if it's an enemy piece, add it to potential moves & end path
                        break
                else:
                    # generator detected piece, cannon must jump over it
                    # check if any pieces behind it are available for capture
                    if current_piece != "" and current_piece is not None:
                        jumped_over = True

                    # execute this for consecutive empty positions
                    else:
                        temp_moves.append(generated_move)
            return temp_moves

        # try each direction for cannon
        valid_moves = []
        for move in cannon_test(self.up()):
            valid_moves.append(move)
        for move in cannon_test(self.down()):
            valid_moves.append(move)
        for move in cannon_test(self.left()):
            valid_moves.append(move)
        for move in cannon_test(self.right()):
            valid_moves.append(move)

        # eliminate out-of-bound moves
        inbound_moves = [move for move in valid_moves if 0 <= move[0] <= 9 and 0 <= move[1] <= 8]

        return inbound_moves


class Chariot(Piece):
    """Represents a chariot piece."""

    def __repr__(self):
        """Displays a chariot piece as its Chinese character."""
        if self._color == 'red':
            return '俥'
        else:
            return '車'

    def get_moves(self, board):
        """Returns a list of valid move based on current location."""

        def chariot_test(left_right_up_down):
            """
            Tests a move from the move generator
            and determine if it's valid.
            """
            temp_moves = []

            # generator traverses along column or row
            for generated_move in left_right_up_down:
                current_piece = board.get_piece(generated_move)

                # generator detected a piece
                if current_piece != "" and current_piece is not None:
                    current_piece_color = current_piece.get_color()

                    # detected piece is friendly,
                    # chariot path ends.
                    if current_piece_color == self._color:
                        break

                    # detected piece is enemy,
                    # add position to potential moves,
                    # chariot path ends.
                    else:
                        temp_moves.append(generated_move)
                        break

                # execute this for consecutive empty positions
                else:
                    temp_moves.append(generated_move)

            return temp_moves

        # try each direction for chariot
        valid_moves = []
        for move in chariot_test(self.up()):
            valid_moves.append(move)
        for move in chariot_test(self.down()):
            valid_moves.append(move)
        for move in chariot_test(self.left()):
            valid_moves.append(move)
        for move in chariot_test(self.right()):
            valid_moves.append(move)

        # eliminate out-of-bound moves
        inbound_moves = [move for move in valid_moves if 0 <= move[0] <= 9 and 0 <= move[1] <= 8]

        return inbound_moves


class Horse(Piece):
    """Represents a horse piece."""

    def __repr__(self):
        """Displays a horse piece as its Chinese character."""
        if self._color == 'red':
            return '傌'
        else:
            return '馬'

    def get_moves(self, board):
        """Returns a list of valid move based on current location."""
        temp_moves = []
        row = self.row_to_index(self._location)
        col = self.col_to_index(self._location)

        # check the position below horse
        if board.get_piece([row - 1, col]) == "":
            temp_moves.append([row - 2, col - 1])
            temp_moves.append([row - 2, col + 1])

        # check the position above horse
        if board.get_piece([row + 1, col]) == "":
            temp_moves.append([row + 2, col - 1])
            temp_moves.append([row + 2, col + 1])

        # check the position to the left of horse
        if board.get_piece([row, col - 1]) == "":
            temp_moves.append([row + 1, col - 2])
            temp_moves.append([row - 1, col - 2])

        # check the position to the right of horse
        if board.get_piece([row, col + 1]) == "":
            temp_moves.append([row + 1, col + 2])
            temp_moves.append([row - 1, col + 2])

        # eliminate out-of-bound moves
        inbound_moves = [move for move in temp_moves if 0 <= move[0] <= 9 and 0 <= move[1] <= 8]

        # eliminate moves that contain friendly pieces
        valid_moves = [move for move in inbound_moves if
                       board.get_piece(move) == "" or
                       board.get_piece(move).get_color() != self._color]

        return valid_moves


class Elephant(Piece):
    """Represents an elephant piece."""

    def __repr__(self):
        """Displays a elephant piece as its Chinese character."""
        if self._color == 'red':
            return '相'
        else:
            return '象'

    def get_moves(self, board):
        """Returns a list of valid move based on current location."""
        row = self.row_to_index(self._location)
        col = self.col_to_index(self._location)
        temp_moves = {
            (row + 2, col + 2): (row + 1, col + 1),
            (row + 2, col - 2): (row + 1, col - 1),
            (row - 2, col - 2): (row - 1, col - 1),
            (row - 2, col + 2): (row - 1, col + 1)
        }

        # eliminate out of bound elephant moves
        out_of_bound_keys = [move for move in temp_moves if move[0] < 0 or move[0] > 9 or move[1] < 0 or move[1] > 8]
        for key in out_of_bound_keys:
            del temp_moves[key]

        # eliminate occupied diagonally adjacent positions
        valid_moves = [[move[0], move[1]] for move, diag_adj in temp_moves.items() if board.get_piece(diag_adj) == ""]

        # eliminate moves that extend beyond river
        red_inb_moves = [move for move in valid_moves if 0 <= move[0] <= 4 and 0 <= move[1] <= 8]
        blk_inb_moves = [move for move in valid_moves if 5 <= move[0] <= 9 and 0 <= move[1] <= 8]

        # eliminate moves that contain friendly pieces
        red_moves = [move for move in red_inb_moves if
                     board.get_piece(move) == "" or
                     board.get_piece(move).get_color() != self._color]

        blk_moves = [move for move in blk_inb_moves if
                     board.get_piece(move) == "" or
                     board.get_piece(move).get_color() != self._color]

        if self._color == 'red':
            return red_moves
        else:
            return blk_moves


class Advisor(Piece):
    """Represents an advisor piece."""

    def __repr__(self):
        """Displays an advisor piece as its Chinese character."""
        if self._color == 'red':
            return '仕'
        else:
            return '士'

    def get_moves(self, board):
        """Returns a list of valid move based on current location."""
        row = self.row_to_index(self._location)
        col = self.col_to_index(self._location)
        temp_moves = [[row + 1, col + 1],
                      [row + 1, col - 1],
                      [row - 1, col + 1],
                      [row - 1, col - 1]]

        # restrict movement to red palace
        if self._color == 'red':
            inbound_moves = [move for move in temp_moves if (0 <= move[0] <= 2) and (3 <= move[1] <= 5)]
            valid_moves = [move for move in inbound_moves if
                           board.get_piece(move) == "" or
                           board.get_piece(move).get_color() != self._color]
            return valid_moves

        # restrict movement to black palace
        elif self._color == 'black':
            inbound_moves = [move for move in temp_moves if (7 <= move[0] <= 9) and (3 <= move[1] <= 5)]
            valid_moves = [move for move in inbound_moves if
                           board.get_piece(move) == "" or
                           board.get_piece(move).get_color() != self._color]
            return valid_moves


class General(Piece):
    """Represents a General piece."""

    def __repr__(self):
        """Displays a general piece as its Chinese character."""
        return "General"

    def get_moves(self, board):
        """Returns a list of valid move based on current location."""
        row = self.row_to_index(self._location)
        col = self.col_to_index(self._location)
        temp_moves = [[row + 1, col],
                      [row - 1, col],
                      [row, col + 1],
                      [row, col - 1]]

        # restrict movement to red palace
        if self._color == 'red':
            inbound_moves = [move for move in temp_moves if (0 <= move[0] <= 2) and (3 <= move[1] <= 5)]
            valid_moves = [move for move in inbound_moves if
                           board.get_piece(move) == "" or
                           board.get_piece(move).get_color() != self._color]
            return valid_moves

        # restrict movement to black palace
        elif self._color == 'black':
            inbound_moves = [move for move in temp_moves if (7 <= move[0] <= 9) and (3 <= move[1] <= 5)]
            valid_moves = [move for move in inbound_moves if
                           board.get_piece(move) == "" or
                           board.get_piece(move).get_color() != self._color]
            return valid_moves


# g = XiangqiGame()
#
# g.make_move('i1','i2')
# g.make_move('h10','g8')
# g.make_move('i2','f2')
# g.make_move('g8','e9')
# g.make_move('f2','f7')
# g.make_move('h8','h7')
# g.make_move('a4','a5')
# g.make_move('i10','h10')
# g.make_move('h3','h10')
# g.make_move('b8','b6')
# g.make_move('c4','c5')
# g.make_move('a7','a6')
# g.make_move('b3','b10')
# g.make_move('a6','a5')
# g.make_move('a1','a5')
# g.make_move('c7','c6')
# g.make_move('a5','a10')
# g.make_move('e7','e6')
# g.make_move('f7','g7')
# g.make_move('e6','e5')
# g.make_move('g7','h7')
# g.make_move('e5','e4')
# g.make_move('h7','i7')
# g.make_move('b6','b7')
# g.make_move('a10','a4')
# g.make_move('b7','c7')
# g.make_move('a4','e4')
# g.make_move('c7','a7')
# g.make_move('c5','c6')
# g.make_move('a7','b7')
# g.make_move('i7','b7')
# print(g.get_game_state())
# for row in reversed(g._board):
#     print(row)
#
# print("")
# print("")
# print("")
# print("")
# print("")
# print("")
# print("")
# print("")
# print("")
# print("")




# game = XiangqiGame()
#
# game.make_move('e4', 'e5')
# game.make_move('e7', 'e6')
# game.make_move('c1', 'a3')
# game.make_move('e5', 'e6') # not right turn
# game.make_move('e6', 'e5')
# game.make_move('g1', 'i3')
# game.make_move('e5', 'e4')
# game.make_move('b3', 'b4')
# game.make_move('b8', 'd8')
# game.make_move('c4', 'c5')
# game.make_move('h8', 'f8')
# game.make_move('c5', 'c6')
# game.make_move('e4', 'e3')
# game.make_move('h3', 'f3')
# game.make_move('e3', 'e2') # puts red general in check
# game.make_move('d1', 'e2')
# game.make_move('f8', 'e8')
# game.make_move('e1','d1')
# game.make_move('a10', 'a9')
# game.make_move('d1', 'd2')
# game.make_move('a9', 'e9')
# game.make_move('g4', 'g5')
# game.make_move('d8', 'd7')
# game.make_move('g5', 'g6')
# game.make_move('e8', 'd8')
# print(game.get_game_state())
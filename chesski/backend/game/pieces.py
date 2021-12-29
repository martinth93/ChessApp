class Piece():
    """
    A parent class of all chesspieces.
    """

    def __init__(self, position, color, chessboard):

        self.position = position # position on chessboard (int:row, int:col)
        self.color = color  # color of piece (which player it belongs to)
        self.Abbrevation = None
        self.chessboard = chessboard
        self.chessboard.place_piece_on_board(self) # place it on board

    def is_white(self):
        """Methods that returns true if piece belongs to the white player"""
        return self.color=='w'

    def get_position(self):
        """
        Returns the current position of the chess piece in common chess notation.
        col 0, row 0 = a1
        col 4, row 2 = e3
        """
        row = self.position[0]
        col = self.position[1]
        alphabet = "abcdefgh"
        return alphabet[col] + str(row+1)

    def display(self):
        """
        displays the Piece with color, Abbrevation, id and
        position in chess notation.
        """
        return f"{self.color}-{self.Abbrevation}-{self.get_position()}"

    def move(self, new_pos):
        """
        Updates position if move is legal.
        """

        if self.move_is_legal(new_pos):
        # if move is legal according to general and piece-specific rules -
        # move piece and eventually remove opponents piece
            self.chessboard.remove_piece_from_board(new_pos)
            self.chessboard.remove_piece_from_board(self.position)
            self.position = new_pos
            self.chessboard.place_piece_on_board(self)
            return True
        else:
            raise ValueError('Move not possible.')

    def general_illegal_move(self, new_pos):
        """
        Checking if a move is illegal, according to general rules that are equal
        to all pieces.
        Move to the field it is already on.
        Move to a field out of board.
        Move to a field where if there is already one of your
        pieces (Except castling).
        """
        if new_pos == self.position:
            return True
            # didn't move! new_position was old position

        if (new_pos[1] < 0 or new_pos[1] > 7 or
            new_pos[0] < 0 or new_pos[0] > 7):
            return True
            # If out of board

        piece_to_remove = self.chessboard.return_piece_on_field(new_pos)
        # Checking if there is a piece on new_pos

        if piece_to_remove != None:
            if piece_to_remove.color == self.color:
                return True
                # if trying to move on field with own piece on it
                # Castling?

        return False # no rulebreak found


# ----------------------------- Classes of Chess Pieces -----------------------


class Pawn(Piece):
    """
    A Class representing the Pawn Chesspiece.
    """

    def __init__(self, position, color, chessboard):
        super().__init__(position, color, chessboard)
        self.Abbrevation = "P"

    def move_is_legal(self, new_pos):
        """
        Returning True if moving pawn in specified way is allowed.
        Wether endfield is already occupied with own piece is checked in
        Piece Class.

        Parameters:
                    new_pos: (int:row, int:col)   new position of piece
                    chessboard: ChessBoard        current chessboard of piece
        """
        if self.general_illegal_move(new_pos):
            return False

        one_field = 1
        if not self.is_white():         # white pawns can only go up
            one_field = -1              # black pawns can only go down

        direction = tuple(map(lambda i, j: i - j, new_pos, self.position))
        # how many fields up/down left/rigth

        if self.chessboard.return_piece_on_field(new_pos) == None:
        # if new field does not have a piece on it

            if direction == (one_field, 0):
                return True
                # if moved one field up (if white) / down (if black)
                # in same column

            elif (direction == (2 * one_field, 0) and
                self.position[0] == ((7 + one_field) % 7) and
                self.chessboard.return_piece_on_field(piece_pos =
                (self.position[0] + one_field, self.position[1])) == None):
                 return True
                 # if moved two fields up/down from starting position (legal)
                 # and no piece is inbetween old and new position

        else:
        # if new field does have a piece on it
            if (direction == (one_field, one_field) or
                    direction == (one_field, -one_field)):
               return True
               # if moved one to the site
               # and 1 up (if white) / 1 down (if black) (diagonal, legal)


        return False   # if no legal move was matched


class Rook(Piece):
    """
    A Class representing the Rook Chesspiece.
    """

    def __init__(self, position, color, chessboard):
        super().__init__(position, color, chessboard)
        self.Abbrevation = "R"

    def move_is_legal(self, new_pos):
        """
        Returning True if moving rook in specified way is allowed.
        Wether endfield is already occupied with own piece is checked in
        Piece Class.

        Parameters:
                    new_pos: (int:row, int:col)   new position of piece
        """
        if self.general_illegal_move(new_pos):
            return False

        direction = tuple(map(lambda i, j: i - j, new_pos, self.position))
        # how many fields up/down left/rigth

        if direction[0] == 0 or direction[1] == 0:  # only along row or column
            return self.chessboard.no_pieces_between(start_pos=self.position,
                                                     end_pos = new_pos)
            # returns True if no pieces between start and end, otherwise False

        else: # not moved diagonally
            return False


class Knight(Piece):
    """
    A Class representing the Knight Chesspiece.
    """

    def __init__(self, position, color, chessboard):
        super().__init__(position, color, chessboard)
        self.Abbrevation = "N"

    def move_is_legal(self, new_pos):
        """
        Returning True if moving knight in specified way is allowed.
        Wether endfield is already occupied with own piece is checked in
        Piece Class.

        Parameters:
                    new_pos: (int:row, int:col)   new position of piece
        """
        if self.general_illegal_move(new_pos):
            return False

        direction = tuple(map(lambda i, j: i - j, new_pos, self.position))
        # how many fields up/down left/rigth

        possible_directions_set = {1, 2}

        if set([abs(direction[0]), abs(direction[1])]) == possible_directions_set:
        # knight can move in all possible directions that are combinations
        # of moving one field vertical and two fields horizontal or
        # one field horizontal and two fields vertical (L-Shaped)
            return True

        else: # no legal move found
            return False


class Bishop(Piece):
    """
    A Class representing the Bishop Chesspiece.
    """

    def __init__(self, position, color, chessboard):
        super().__init__(position, color, chessboard)
        self.Abbrevation = "B"

    def move_is_legal(self, new_pos):
        """
        Returning True if moving a Bishop in specified way is allowed.
        Wether endfield is already occupied with own piece is checked in
        Piece Class.

        Parameters:
                    new_pos: (int:row, int:col)   new position of piece
        """
        if self.general_illegal_move(new_pos):
            return False

        direction = tuple(map(lambda i, j: i - j, new_pos, self.position))
        # how many fields up/down left/rigth

        if abs(direction[0]) == abs(direction[1]):
        # only diagonal moves allowed
            return self.chessboard.no_pieces_between(start_pos=self.position,
                                                     end_pos = new_pos)
            # returns True if no pieces between start and end, otherwise False

        else: # not moved diagonally
            return False


class Queen(Piece):
    """
    A Class representing the Queen Chesspiece.
    """

    def __init__(self, position, color, chessboard):
        super().__init__(position, color, chessboard)
        self.Abbrevation = "Q"

    def move_is_legal(self, new_pos):
        """
        Returning True if moving Queen in specified way is allowed.
        Wether endfield is already occupied with own piece is checked in
        Piece Class.

        Parameters:
                    new_pos: (int:row, int:col)   new position of piece
        """
        if self.general_illegal_move(new_pos):
            return False

        direction = tuple(map(lambda i, j: i - j, new_pos, self.position))
        # how many fields up/down left/rigth

        if (abs(direction[0]) == abs(direction[1]) or
            direction[0] == 0 or direction[1] == 0):
        # only diagonal/vertical and horizontal moves allowed
            return self.chessboard.no_pieces_between(start_pos=self.position,
                                                     end_pos = new_pos)
            # returns True if no pieces between start and endposition

        else: # not moved diagonally
            return False

class King(Piece):
    """
    A Class representing the King Chesspiece.
    """

    def __init__(self, position, color, chessboard):
        super().__init__(position, color, chessboard)
        self.Abbrevation = "K"

    def move_is_legal(self, new_pos):
        """
        Returning True if moving the King in specified way is allowed.
        Wether endfield is already occupied with own piece is checked in
        Piece Class.

        Parameters:
                    new_pos: (int:row, int:col)   new position of piece
        """
        if self.general_illegal_move(new_pos):
            return False

        direction = tuple(map(lambda i, j: i - j, new_pos, self.position))
        # how many fields up/down left/rigth

        if abs(direction[0]) < 2 and abs(direction[1]) < 2:
            return True
            # king can move in any of the 8 squares surrounding him

        else: # moved to far
            return False

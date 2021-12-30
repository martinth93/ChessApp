class Piece():
    """
    A parent class of all chesspieces.
    """

    def __init__(self, position, color, chessboard):

        self.position = position # position on chessboard (int:row, int:col)
        self.color = color  # color of piece (which player it belongs to)
        self.Abbrevation = None
        self.chessboard = chessboard
        self.chessboard.place_on_board(self) # place it on board

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

    def move(self, end_pos):
        """
        Updates position and place piece on chessbaord.
        """
        # if move is legal according to general and piece-specific rules -
        # move piece
        self.chessboard.remove_from_board(self)
        self.position = end_pos
        self.chessboard.place_on_board(self)

    def move_is_legal(self, end_pos):
        """
        Checks if move is legal according to general piece-unspecific and
        piece-specific rules like moving restictions.
        """
        try:
            self.check_general_illegal_move(end_pos)
            self.check_piece_rules(end_pos)
            return True
        except ValueError as e:
            print(e)
            return False


    def check_general_illegal_move(self, end_pos):
        """
        Checking if a move is illegal, according to general rules that are equal
        to all pieces.
        Move to the field it is already on.
        Move to a field out of board.
        Move to a field where if there is already one of your
        pieces (Except castling).
        """
        if end_pos == self.position:
            raise ValueError('Move failed: Piece already on new position.')
            # didn't move! end_position was old position

        if (end_pos[1] < 0 or end_pos[1] > 7 or
            end_pos[0] < 0 or end_pos[0] > 7):
            raise ValueError('Move failed: New position out of board.')
            # If out of board

        piece_to_remove = self.chessboard.return_piece_on_field(end_pos)
        # Checking if there is a piece on end_pos

        if piece_to_remove != None:
            if piece_to_remove.color == self.color:
                raise ValueError('Move failed: Field blocked by another same-colored piece.')
                # if trying to move on field with own piece on it
                # Castling?


# ----------------------------- Classes of Chess Pieces -----------------------


class Pawn(Piece):
    """
    A Class representing the Pawn Chesspiece.
    """

    def __init__(self, position, color, chessboard):
        super().__init__(position, color, chessboard)
        self.Abbrevation = "P"

    def check_piece_rules(self, end_pos):
        """
        Returning True if moving pawn in specified way is allowed.
        Wether endfield is already occupied with own piece is checked in
        Piece Class.
        """
        one_field = 1
        if not self.is_white():         # white pawns can only go up
            one_field = -1              # black pawns can only go down

        start_pos = self.position
        on_starting_row = start_pos[0] == ((7 + one_field) % 7)
        # boolean if pawn on starting row (1 for white/6 for black)

        direction = tuple(map(lambda i, j: i - j, end_pos, start_pos))
        # how many fields up/down left/rigth

        if self.chessboard.return_piece_on_field(end_pos) == None:
        # if new field does not have a piece on it

            if direction == (one_field, 0):
                return True
                # if moved one field up (if white) or down (if black)

            # if moved two fields up from startrow
            elif direction[0] == 2 * one_field and on_starting_row:
                if direction[1] == 0:
                    if self.chessboard.no_pieces_between(start_pos, end_pos):
                        return True
                        # returns True if no pieces between start and endposition

        else: # if new field does have a piece on it
            if (direction == (one_field, one_field) or
                    direction == (one_field, -one_field)):
               return True
               # if moved one field diagonal and up

            # en passant
            elif (direction[0] == 2*one_field and on_starting_row and
                  abs(direction[1]) == 1):
                inter_pos = (start_pos[0]+2*one_field, start_pos[1])
                if self.chessboard.no_pieces_between(start_pos, inter_pos):
                    if self.chessboard.return_piece_on_field(end_pos):
                        return True

        # no legal move found
        raise ValueError('Move failed: Cannot move pawn like that.')


class Rook(Piece):
    """
    A Class representing the Rook Chesspiece.
    """

    def __init__(self, position, color, chessboard):
        super().__init__(position, color, chessboard)
        self.Abbrevation = "R"

    def check_piece_rules(self, end_pos):
        """
        Returning True if moving rook in specified way is allowed.
        Wether endfield is already occupied with own piece is checked in
        Piece Class.
        """
        direction = tuple(map(lambda i, j: i - j, end_pos, self.position))
        # how many fields up/down left/rigth

        if direction[0] == 0 or direction[1] == 0:  # only along row or column
            if self.chessboard.no_pieces_between(self.position, end_pos):
                return True
                # returns True if no pieces between start and endposition
            else:
                raise ValueError('Move failed: Cannot move rook like that.')

        else: # not moved vetical/horizontal
            raise ValueError('Move failed: Cannot move rook like that.')


class Knight(Piece):
    """
    A Class representing the Knight Chesspiece.
    """

    def __init__(self, position, color, chessboard):
        super().__init__(position, color, chessboard)
        self.Abbrevation = "N"

    def check_piece_rules(self, end_pos):
        """
        Returning True if moving knight in specified way is allowed.
        Wether endfield is already occupied with own piece is checked in
        Piece Class.
        """
        direction = tuple(map(lambda i, j: i - j, end_pos, self.position))
        # how many fields up/down left/rigth

        possible_directions_set = {1, 2}

        if set([abs(direction[0]), abs(direction[1])]) == possible_directions_set:
        # knight can move in all possible directions that are combinations
        # of moving one field vertical and two fields horizontal or
        # one field horizontal and two fields vertical (L-Shaped)
            return True

        else: # no legal move found
            raise ValueError('Move failed: Cannot move knight like that.')


class Bishop(Piece):
    """
    A Class representing the Bishop Chesspiece.
    """

    def __init__(self, position, color, chessboard):
        super().__init__(position, color, chessboard)
        self.Abbrevation = "B"

    def check_piece_rules(self, end_pos):
        """
        Returning True if moving a Bishop in specified way is allowed.
        Wether endfield is already occupied with own piece is checked in
        Piece Class.
        """
        direction = tuple(map(lambda i, j: i - j, end_pos, self.position))
        # how many fields up/down left/rigth

        if abs(direction[0]) == abs(direction[1]):
        # only diagonal moves allowed
            if self.chessboard.no_pieces_between(self.position, end_pos):
                return True
                # returns True if no pieces between start and endposition
            else:
                raise ValueError('Move failed: Cannot move bishop like that.')

        else: # not moved diagonally
            raise ValueError('Move failed: Cannot move bishop like that.')


class Queen(Piece):
    """
    A Class representing the Queen Chesspiece.
    """

    def __init__(self, position, color, chessboard):
        super().__init__(position, color, chessboard)
        self.Abbrevation = "Q"

    def check_piece_rules(self, end_pos):
        """
        Returning True if moving Queen in specified way is allowed.
        Wether endfield is already occupied with own piece is checked in
        Piece Class.
        """
        direction = tuple(map(lambda i, j: i - j, end_pos, self.position))
        # how many fields up/down left/rigth

        if (abs(direction[0]) == abs(direction[1]) or
            direction[0] == 0 or direction[1] == 0):
        # only diagonal/vertical and horizontal moves allowed
            if self.chessboard.no_pieces_between(self.position, end_pos):
                return True
                # returns True if no pieces between start and endposition
            else:
                raise ValueError('Move failed: Cannot move queen like that.')

        else: # not moved diagonally
            raise ValueError('Move failed: Cannot move queen like that.')

class King(Piece):
    """
    A Class representing the King Chesspiece.
    """

    def __init__(self, position, color, chessboard):
        super().__init__(position, color, chessboard)
        self.Abbrevation = "K"

    def check_piece_rules(self, end_pos):
        """
        Returning True if moving the King in specified way is allowed.
        Wether endfield is already occupied with own piece is checked in
        Piece Class.
        """
        direction = tuple(map(lambda i, j: i - j, end_pos, self.position))
        # how many fields up/down left/rigth

        if abs(direction[0]) < 2 and abs(direction[1]) < 2:
            return True
            # king can move in any of the 8 squares surrounding him

        else: # moved to far
            raise ValueError('Move failed: Cannot move king like that.')

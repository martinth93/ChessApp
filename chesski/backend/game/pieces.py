class Piece():
    """Parent Class of all ChessPiece Classes"""

    def __init__(self, position, color, chessboard):
        self.position = position
        self.color = color
        self.type_code = ''
        self.chessboard = chessboard
        self.move_count = 0
        self.value = 0
        self.en_passantable = False

        self.chessboard.place_on_board(self)

    def is_white(self):return self.color=='w'

    def increase_move_count(self):
        """Function to set flags for special rules, like castling or en passant"""
        self.move_count += 1

    def get_position(self):
        """Returns the current position of the chess piece in chess notation."""
        row = self.position[0]
        col = self.position[1]
        alphabet = "abcdefgh"
        return alphabet[col] + str(row+1)

    def display(self):
        """Returng String with color-type_code-position (in chess notation)."""
        return f"{self.color}-{self.type_code}-{self.get_position()}"

    def move(self, move, reverse=False):
        """Updates position, removes from chessboard and place on new field.

        Parameters:
        -------------
        move.end_pos: tuple of int
            New Position of chesspiece (row, col).
        """
        self.chessboard.remove_from_board(self)
        if reverse:
            self.position = move.start_pos
        else:
            self.position = move.end_pos

        self.chessboard.place_on_board(self)

    def move_is_pseudo_legal(self, move):
        """Checks if move is legal except for following rules:
        -player move puts himself in check
        -castling through check
        """
        try:
            move.taking_piece = self.chessboard.return_piece_on_field(move.end_pos)
            self.check_moving_off_board(move)
            self.check_moving_on_place(move)
            self.check_taking_piece(move)
            self.check_piece_rules(move)
            return True
        except ValueError as e:
            # print(e)
            return False

    def check_moving_off_board(self, move):
        if (move.end_pos[1] < 0 or move.end_pos[1] > 7 or
            move.end_pos[0] < 0 or move.end_pos[0] > 7):
            raise ValueError('Move failed: New position out of board.')

    def check_moving_on_place(self, move):
        if move.end_pos == move.start_pos:
            raise ValueError('Move failed: Piece already on new position.')
            # didn't move! move.end_position was old position

    def check_taking_piece(self, move):
        """Has to be called before """
        if move.taking_piece:
            if move.taking_piece.color == self.color:
                if self.type_code == 'K':
                    if self.check_for_castle(move):
                        return # don't raise error if castling
                raise ValueError('Move failed: Field blocked by another same-colored piece.')


# ----------------------------- Classes of Chess Pieces -----------------------


class Pawn(Piece):
    """A Class representing the Pawn Chesspiece."""

    def __init__(self, position, color, chessboard):
        super().__init__(position, color, chessboard)
        self.type_code = "P"
        self.value = 1

    def check_piece_rules(self, move):
        """Returning True if moving pawn in specified way is allowed according
        to piece-specific movement rules."""

        one_field = 1
        if not self.is_white():         # white pawns can only go up
            one_field = -1              # black pawns can only go down

        on_starting_row = move.start_pos[0] == ((7 + one_field) % 7)
        # boolean if pawn on starting row (1 for white/6 for black)

        on_enpassant_row = move.start_pos[0] == ((7 + one_field)/2)
        # print(on_enpassant_row)
        # boolean if pawn on en passant row (5 for white/4 for black)

        direction = tuple(map(lambda i, j: i - j, move.end_pos, move.start_pos))
        # how many fields up/down left/rigth

        if move.taking_piece == None:
        # if new field does not have a piece on it

            if direction == (one_field, 0):
                return True
                # if moved one field up (if white) or down (if black)

            # if moved two fields up from startrow
            elif on_starting_row and direction[0] == 2 * one_field:
                if direction[1] == 0:
                    if self.chessboard.no_pieces_between(move.start_pos, move.end_pos):
                        return True
                        # returns True if no pieces between start and endposition

            # en passant
            elif on_enpassant_row:
                if (direction == (one_field, one_field) or
                    direction == (one_field, -one_field)):
                    inter_pos = (move.start_pos[0], move.start_pos[1] + direction[1])
                    piece = self.chessboard.return_piece_on_field(inter_pos)
                    if piece != None and piece.color != self.color and piece.en_passantable:
                        move.taking_piece = piece
                        self.chessboard.remove_from_board(piece)
                        move.en_passant = True
                        return True


        else: # if new field does have a piece on it
            if (direction == (one_field, one_field) or
                    direction == (one_field, -one_field)):
               return True
               # if moved one field diagonal and up



        # no legal move found
        raise ValueError('Move failed: Cannot move pawn like that.')


class Rook(Piece):
    """
    A Class representing the Rook Chesspiece.
    """

    def __init__(self, position, color, chessboard):
        super().__init__(position, color, chessboard)
        self.type_code = "R"
        self.value = 5

    def check_piece_rules(self, move):
        """
        Returning True if moving rook in specified way is allowed.
        Wether endfield is already occupied with own piece is checked in
        Piece Class.
        """
        direction = tuple(map(lambda i, j: i - j, move.end_pos, move.start_pos))
        # how many fields up/down left/rigth

        if direction[0] == 0 or direction[1] == 0:  # only along row or column
            if self.chessboard.no_pieces_between(move.start_pos, move.end_pos):
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
        self.type_code = "N"
        self.value = 3

    def check_piece_rules(self, move):
        """
        Returning True if moving knight in specified way is allowed.
        Wether endfield is already occupied with own piece is checked in
        Piece Class.
        """
        direction = tuple(map(lambda i, j: i - j, move.end_pos, move.start_pos))
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
        self.type_code = "B"
        self.value = 3

    def check_piece_rules(self, move):
        """
        Returning True if moving a Bishop in specified way is allowed.
        Wether endfield is already occupied with own piece is checked in
        Piece Class.
        """
        direction = tuple(map(lambda i, j: i - j, move.end_pos, move.start_pos))
        # how many fields up/down left/rigth

        if abs(direction[0]) == abs(direction[1]):
        # only diagonal moves allowed
            if self.chessboard.no_pieces_between(move.start_pos, move.end_pos):
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
        self.type_code = "Q"
        self.value = 9

    def check_piece_rules(self, move):
        """
        Returning True if moving Queen in specified way is allowed.
        Wether endfield is already occupied with own piece is checked in
        Piece Class.
        """
        direction = tuple(map(lambda i, j: i - j, move.end_pos, move.start_pos))
        # how many fields up/down left/rigth

        if (abs(direction[0]) == abs(direction[1]) or
            direction[0] == 0 or direction[1] == 0):
        # only diagonal/vertical and horizontal moves allowed
            if self.chessboard.no_pieces_between(move.start_pos, move.end_pos):
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
        self.type_code = "K"
        self.value = 0

    def check_piece_rules(self, move):
        """
        Returning True if moving the King in specified way is allowed.
        Wether endfield is already occupied with own piece is checked in
        Piece Class.
        """
        direction = tuple(map(lambda i, j: i - j, move.end_pos, move.start_pos))
        # how many fields up/down left/rigth

        if move.castling:
            return True

        if abs(direction[0]) < 2 and abs(direction[1]) < 2:
            return True
            # king can move in any of the 8 squares surrounding him

        else: # moved to far
            raise ValueError('Move failed: Cannot move king like that.')

    def check_for_castle(self, move):
        direction = tuple(map(lambda i, j: i - j, move.end_pos, move.start_pos))

        if direction == (0, 3) or direction == (0, -4):
            if move.taking_piece and self.move_count == 0:
                if move.taking_piece.color==self.color and move.taking_piece.type_code == 'R':
                    if move.taking_piece.move_count == 0:
                        if self.chessboard.no_pieces_between(self.position, move.end_pos):
                            if direction == (0, 3):
                                move.castling = 'short'
                                return True
                            else:
                                move.castling = 'long'
                                return True
        return False

class Piece():
    """
    A parent class of all chesspieces.
    """

    def __init__(self, position, color, chessboard):

        self.position = position # position on chessboard (int:row, int:col)
        self.color = color  # color of piece (which player it belongs to)
        self.Abbrevation = None
        self.chessboard = chessboard
        self.chessboard.place_piece_in_state(self) # place it on board

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

    def move_is_legal(self, new_pos, chessboard):
        """
        Returns True if the move is legal.
        Defined in the Subclasses for each Chesspiece.
        """
        pass

    def move(self, new_pos):
        """
        Updates position if move is legal.
        """
        new_row = new_pos[0]
        new_col = new_pos[1]

        if (new_col < 0 or new_col > 7 or
            new_row < 0 or new_row > 7):
            # If out of board
            return

        elif self.move_is_legal(new_pos):
            piece_to_remove = self.chessboard.piece_on_field(new_pos)
            if piece_to_remove != None:
                self.chessboard.remove_piece_from_state(new_pos)
                # maybe do something with removed pieces (display somewhere)
            self.chessboard.remove_piece_from_state(self.position)
            self.position = new_pos
            self.chessboard.place_piece_in_state(self)


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

        Parameters:
                    new_pos: (int:row, int:col)   new position of piece
                    chessboard: ChessBoard        current chessboard of piece
        """
        one_field = 1
        if not self.is_white():         # if its a pawn of the black player
            one_field = -1              # going up/right in opposite direction

        direction = tuple(map(lambda i, j: i - j, new_pos, self.position))
        # how many fields up/down left/rigth

        if self.chessboard.piece_on_field(new_pos) == None:
        # if new field does not have a piece on it

            if direction == (one_field, 0):
                return True
                # if moved one field up (if white) / down (if black)
                # in same column

            elif (direction == (2 * one_field, 0) and
                self.position[0] == ((7 + one_field) % 7) and
                self.chessboard.piece_on_field(piece_pos =
                (self.position[0] + one_field, self.position[1])) == None):
                 return True
                 # if moved two fields up/down from starting position (legal)
                 # and no piece is inbetween old and new position

        elif self.chessboard.piece_on_field(new_pos).color != self.color:
        # if new field does have a piece of different color on it
            if (direction == (one_field, one_field) or
                    direction == (one_field, -one_field)):
               return True
               # if moved one to the site
               # and 1 up (if white) / 1 down (if black) (diagonal, legal)


        return False   # if no legal move was matched

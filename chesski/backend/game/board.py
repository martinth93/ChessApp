class ChessBoard():
    """
    A class to represent a chessboard.
    """

    def __init__(self, state=None):
        if state == None:                # if state is not provided
            self.initialize_state()
        else:
            self.state = state

        self.size = (8, 8)

    def initialize_state(self):
        """
        Initializes the state as an empty ChessBoard. Empty = None.
        """

        self.state = []
        for _ in range(8):
            row = [None,]*8
            self.state.append(row)
            # create 8x8 None Board (list([row0], [row1], ...))

    def remove_piece_from_state(self, piece_pos):
        """
        Replaces field at piece_pos (int:col, int:row) of the chessboard with "None"
        """
        row = piece_pos[0]
        col = piece_pos[1]
        self.state[row][col] = None

    def place_piece_in_state(self, piece):
        """
        Places piece (instance of Piece or a Subclass like Pawn)
        on field piece_pos (int:col, int:row) on the chessboard.
        """
        row = piece.position[0]
        col = piece.position[1]
        self.state[row][col] = piece

    def piece_on_field(self, piece_pos):
        """
        Checks if a Piece is on a field.
        If True returns the piece, if False returns None.
        """
        row = piece_pos[0]
        col = piece_pos[1]
        return self.state[row][col]

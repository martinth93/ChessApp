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

    def remove_piece_from_board(self, piece_pos):
        """
        Replaces field at piece_pos (int:col, int:row) of the chessboard with "None"
        """
        row = piece_pos[0]
        col = piece_pos[1]
        self.state[row][col] = None

    def place_piece_on_board(self, piece):
        """
        Places piece (instance of Piece or a Subclass like Pawn)
        on field piece_pos (int:col, int:row) on the chessboard.
        """
        row = piece.position[0]
        col = piece.position[1]
        self.state[row][col] = piece

    def return_piece_on_field(self, piece_pos):
        """
        Checks if a Piece is on a field.
        If True returns the piece, if False returns None.
        """
        row = piece_pos[0]
        col = piece_pos[1]
        return self.state[row][col]

    def no_pieces_between(self, start_pos, end_pos):
        """
        Checks if fields between start and end position are empty.
        Only for horizontal, vertical or diagonal moves.
        """

        distance = ( end_pos[0] - start_pos[0],  end_pos[1] - start_pos[1])

        if abs(distance[0]) == abs(distance[1]): # if diagonal
            num_fields_between = abs(distance[0])
        elif distance[0] == 0 or distance[1] == 0: # if vertical/horizontal
            num_fields_between = abs(sum(distance))
        else:
            raise ValueError("Function only works with diagonal or"
                             "horizontal/vertical moves")

        increment = (distance[0]//num_fields_between,
                     distance[1]//num_fields_between)

        for i in range(1, num_fields_between):
        # checking every field between start and endposition
            next_pos = (start_pos[0] + i * increment[0],
                        start_pos[1] + i * increment[1])
            if self.return_piece_on_field(next_pos):
                return False
                # illegal if there is a piece between start and endposition
        return True
        # no rulebreak found!

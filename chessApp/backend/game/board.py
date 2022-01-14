import numpy as np

class ChessBoard():
    """A class to represent a chessboard."""

    def __init__(self, state=None):
        if state == None:
            self.initialize_state()
        else:
            self.state = state

        self.size = (8, 8)

    def initialize_state(self):
        """Initializes the state as an empty ChessBoard. Empty = None."""
        self.state = []
        for _ in range(8):
            row = [None,]*8
            self.state.append(row)
            # creates 8x8 None-filled Board

    def remove_from_board(self, piece):
        """Replaces field at piece.position of the chessboard with None"""
        row = piece.position[0]
        col = piece.position[1]
        self.state[row][col] = None

    def place_on_board(self, piece):
        """Places piece on piece.position on the chessboard."""
        row = piece.position[0]
        col = piece.position[1]
        self.state[row][col] = piece

    def return_piece_on_field(self, piece_pos):
        """If field is empty returns None."""
        row = piece_pos[0]
        col = piece_pos[1]
        return self.state[row][col]

    def no_pieces_between(self, start_pos, end_pos):
        """Checks if fields between start and end position are empty.
        Only for horizontal, vertical or diagonal moves."""

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

        return True

    def display_board(self):
        """
        Displays the chessboard with pieces on it as numpy array in terminal.

        "O" for empty white field
        "X" for empty black field
        "P-w" for white Pawn
        "P-b" for black Pawn
        "R-w" for white Rook
        "R-b" for black Rook
        "N-w" for white Knight
        "N-b" for black Knight
        "B-w" for white Bishop
        "B-b" for black Bishop
        "Q-w" for white Queen
        "Q-b" for black Queen
        "K-w" for white King
        "K-b" for black King
        """
        full_board = []

        for row in range(8):
            displayed_row = []

            for col in range(8):
                displayed_as = ""
                piece = self.state[row][col]  # get piece or None

                if piece == None:
                    if (row + col) % 2 == 0:
                        displayed = " X "
                    else:
                        displayed = " O "
                else:
                    displayed = f"{piece.type_code}-{piece.color}"
                displayed_row.append(displayed)
            full_board.append(displayed_row)
        full_board.reverse()

        # print(np.array(full_board))
        return np.array(full_board)

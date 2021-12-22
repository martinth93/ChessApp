import numpy as np

from chesski.backend.game.board import ChessBoard
from chesski.backend.game.pieces import Pawn


class GameManager():
    """
    A class handling all gameobjects and mechanics.
    """

    def __init__(self, chessboard=None, pieces=None):

        if chessboard is None:
            self.chessboard = ChessBoard()  # create a new chessboard

        if pieces is None:
            self.pieces = []
            self.initialize_pieces()  # create all necessary pieces

    def initialize_pieces(self):
        """
        Creates Instances of all necessary Chesspieces and places them on
        the right starting spot.

        Current status: Only Pawns
        """
        self
        if self.chessboard.size != (8, 8):  # Custom piece placement for
            raise NotImplementedError       # unusual board sizes
        else:
            for i in range(8):
                pawn_white = Pawn(position=(1, i), color="w",
                                    chessboard=self.chessboard)
                pawn_black = Pawn(position=(6, i), color="b",
                                    chessboard=self.chessboard)
                self.chessboard.place_piece_in_state(pawn_white)
                self.chessboard.place_piece_in_state(pawn_black)

    def display_board(self):
        """
        Displays the chessboard with pieces on it as numpy array.
        "O" for empty white field
        "X" for empty black field
        "P-w" for white Pawn
        "P-b" for black Pawn
        """
        full_board = []

        for row in range(8):
            displayed_row = []

            for col in range(8):
                displayed_as = ""
                piece = self.chessboard.state[row][col]  # get piece or None

                if piece == None:
                    if (row + col) % 2 == 0:
                        displayed = "X"
                    else:
                        displayed = "O"
                else:
                    displayed = f"{piece.Abbrevation}-{piece.color}"

                displayed_row.append(displayed)

            full_board.append(displayed_row)

        return np.array(full_board)

import unittest

from chesski.backend.game.board import ChessBoard
from chesski.backend.game.pieces import Pawn, Rook, Knight, Bishop, Queen, King
from chesski.backend.game.match import Match

class TestMatchBasics(unittest.TestCase):

    def test_initiliaze_pieces(self):
        all_pieces_correct = ""
        match = Match()
        start_board = [
        [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook],
        [Pawn, Pawn, Pawn, Pawn, Pawn, Pawn, Pawn, Pawn],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [Pawn, Pawn, Pawn, Pawn, Pawn, Pawn, Pawn, Pawn],
        [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        ]

        for row in range(8):
            for col in range(8):
                # compare each entry in chessboard state with start board
                piece = match.chessboard.return_piece_on_field(piece_pos=(row, col))
                correct_piece_type = start_board[row][col]

                # if no Piece in state check wether there should be one
                if piece==None:
                    if correct_piece_type != None:
                        all_pieces_correct += f"No piece on {row}, {col} - "

                # if there is a piece in the state check Type and color
                elif not isinstance(piece, correct_piece_type):
                    all_pieces_correct += f"Wrong piece ({piece.Abbrevation}) " \
                            	        + f"on {row}, {col} - "
                elif ((row in [0, 1] and piece.color != 'w') or
                     (row in [6, 7] and piece.color != 'b')):
                     all_pieces_correct += f"Wrong piece-color on {row}, {col} - "

        self.assertEqual("", all_pieces_correct)

    def test_display_board(self):
        match = Match()
        start_board_displayed = [
        ["R-b", "N-b", "B-b", "Q-b", "K-b", "B-b", "N-b", "R-b"],
        ["P-b", "P-b", "P-b", "P-b", "P-b", "P-b", "P-b", "P-b"],
        [" O ", " X ", " O ", " X ", " O ", " X ", " O ", " X "],
        [" X ", " O ", " X ", " O ", " X ", " O ", " X ", " O "],
        [" O ", " X ", " O ", " X ", " O ", " X ", " O ", " X "],
        [" X ", " O ", " X ", " O ", " X ", " O ", " X ", " O "],
        ["P-w", "P-w", "P-w", "P-w", "P-w", "P-w", "P-w", "P-w"],
        ["R-w", "N-w", "B-w", "Q-w", "K-w", "B-w", "N-w", "R-w"]
        ]
        generated_display = match.chessboard.display_board().tolist()
        self.assertEqual(generated_display, start_board_displayed)

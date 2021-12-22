import unittest

from chesski.backend.game.board import ChessBoard
from chesski.backend.game.pieces import Pawn
from chesski.backend.game.gamemanager import GameManager

class TestGameManagerBasics(unittest.TestCase):
    def test_initiliaze_pieces(self):
        """
        Testing if all 8 white and all 8 black pawns are placed correctly.
        """
        manager = GameManager()
        all_pawns_correct = ""
        for row in range(8):
            for col in range(8):
                piece = manager.chessboard.piece_on_field(piece_pos=(row, col))
                if row == 1 or row == 6:
                    if not isinstance(piece, Pawn):
                        all_pawns_correct += f"Not A Pawn on ({row}, {col}) - "
                    elif row == 1 and piece.color != 'w':
                        all_pawns_correct += f"Pawn not white on ({row}, {col}) - "
                    elif row == 6 and piece.color != 'b':
                        all_pawns_correct += f"Pawn not black on ({row}, {col}) - "
                else:
                    if piece is not None:
                        all_pawns_correct += f"Pawn worngfully on ({row}, {col}) - "

        self.assertEqual("", all_pawns_correct)

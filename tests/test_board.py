import unittest

from chesski.backend.game.board import ChessBoard


class TestBoardSize(unittest.TestCase):
    def test_board_size(self):
        """
        Chessboard-Size with odd numbers should raise an Exception
        """

        with self.assertRaises(Exception):
            chessboard = ChessBoard(size=(8, 8))

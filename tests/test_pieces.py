import unittest

from chesski.backend.game.board import ChessBoard


class TestPiece(unittest.TestCase):
    def _test_move(self, piece_type, piece_pos, piece_color, piece_output,
                         piece_move=None,
                         piece2_type=None, piece2_pos=None, piece2_color=None,
                         expected_error=None, expected_msg=None):
        """
        Testing legal and illegal moves that are supposed to raise an Error.
        Possible Spawns of an extra Pawn with specified color and position.
        Can move first Pawn to given position.
        """
        chessboard = ChessBoard()
        piece = piece_type(position=piece_pos,
                         color=piece_color,
                        chessboard=chessboard)
        if piece2_pos:
            piece2 = piece2_type(position=piece2_pos,
                                 color=piece2_color,
                                 chessboard=chessboard)

        if piece_move:
            if expected_error:     # check error
                with self.assertRaises(expected_error) as e:
                    piece.move(end_pos=piece_move)

                expected_msg = expected_msg
                self.assertEqual(str(e.exception), expected_msg)
            else:
                piece.move(end_pos=piece_move)

        generated_output = piece.display()
        self.assertEqual(piece_output, generated_output)

import unittest

from chesski.backend.game.board import ChessBoard


class TestPiece(unittest.TestCase):
    def _test_move(self, piece_type, piece_pos, piece_color, piece_output,
                         piece_move=None,
                         piece2_type=None, piece2_pos=None, piece2_color=None):
        # Testing legal and illegal moves of chess pieces.
        # Possible placing an extra piece with specified type, color and position.
        chessboard = ChessBoard()
        piece = piece_type(position=piece_pos,
                         color=piece_color,
                        chessboard=chessboard)
        if piece2_pos:
            piece2 = piece2_type(position=piece2_pos,
                                 color=piece2_color,
                                 chessboard=chessboard)

        if piece_move:
            if piece.move_is_legal(piece_move):
                piece.move(new_pos=piece_move)

        generated_output = piece.display()
        self.assertEqual(piece_output, generated_output)

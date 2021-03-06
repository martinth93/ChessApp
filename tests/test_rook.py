import unittest

from chesski.backend.game.pieces import Pawn, Rook, Knight, Bishop, Queen, King
from chesski.backend.game.board import ChessBoard

from tests.test_pieces import TestPiece

class TestRook(TestPiece):

    def test_display(self):
        self._test_move(piece_type=Rook, piece_pos=(0, 0), piece_color='w',
                        piece_output='w-R-a1')
        self._test_move(piece_type=Rook, piece_pos=(4, 4), piece_color='b',
                        piece_output='b-R-e5')

###############################################################################
#                                Legal Moves
###############################################################################

    def test_move_is_legal_1up(self):
        self._test_move(piece_type=Rook, piece_pos=(0, 0), piece_color='w',
                        piece_move=(1, 0), piece_output='w-R-a2')
        self._test_move(piece_type=Rook, piece_pos=(4, 4), piece_color='b',
                        piece_move=(3, 4), piece_output='b-R-e4')


    def test_move_is_legal_1right(self):
        self._test_move(piece_type=Rook, piece_pos=(0, 0), piece_color='w',
                        piece_move=(0, 1), piece_output='w-R-b1')
        self._test_move(piece_type=Rook, piece_pos=(4, 4), piece_color='b',
                        piece_move=(4, 3), piece_output='b-R-d5')


    def test_move_is_legal_long_up(self):
        self._test_move(piece_type=Rook, piece_pos=(0, 0), piece_color='w',
                        piece_move=(7, 0), piece_output='w-R-a8')
        self._test_move(piece_type=Rook, piece_pos=(4, 4), piece_color='b',
                        piece_move=(0, 4), piece_output='b-R-e1')

    def test_move_is_legal_4down(self):
        self._test_move(piece_type=Rook, piece_pos=(7, 2), piece_color='w',
                        piece_move=(3, 2), piece_output='w-R-c4')
        self._test_move(piece_type=Rook, piece_pos=(3, 4), piece_color='b',
                        piece_move=(7, 4), piece_output='b-R-e8')


    def test_move_is_legal_1left(self):
        self._test_move(piece_type=Rook, piece_pos=(4, 4), piece_color='w',
                        piece_move=(4, 3), piece_output='w-R-d5')
        self._test_move(piece_type=Rook, piece_pos=(5, 5), piece_color='b',
                        piece_move=(5, 6), piece_output='b-R-g6')

    def test_move_is_legal_4left(self):
        self._test_move(piece_type=Rook, piece_pos=(2, 6), piece_color='w',
                        piece_move=(2, 2), piece_output='w-R-c3')
        self._test_move(piece_type=Rook, piece_pos=(5, 1), piece_color='b',
                        piece_move=(5, 5), piece_output='b-R-f6')

    def test_move_is_legal_taking_pawn(self):
        self._test_move(piece_type=Rook, piece_pos=(4, 4), piece_color='w',
                        piece_move=(4, 6), piece_output='w-R-g5',
                        piece2_type=Pawn, piece2_pos=(4, 6), piece2_color='b')
        self._test_move(piece_type=Rook, piece_pos=(4, 4), piece_color='b',
                        piece_move=(4, 2), piece_output='b-R-c5',
                        piece2_type=Pawn, piece2_pos=(4, 2), piece2_color='w')

    def test_move_is_legal_taking_opponents_pawn(self):
        self._test_move(piece_type=Rook, piece_pos=(4, 4), piece_color='w',
                        piece_move=(6, 4), piece_output='w-R-e7',
                        piece2_type=Pawn, piece2_pos=(6, 4), piece2_color='b')
        self._test_move(piece_type=Rook, piece_pos=(4, 4), piece_color='b',
                        piece_move=(2, 4), piece_output='b-R-e3',
                        piece2_type=Pawn, piece2_pos=(2, 4), piece2_color='w')

###############################################################################
#                               Illegal Moves
###############################################################################

    def test_move_is_illegal_out_of_board(self):
        self._test_move(piece_type=Rook, piece_pos=(0, 7), piece_color='w',
                        piece_move=(0, 8), piece_output='w-R-h1')
        self._test_move(piece_type=Rook, piece_pos=(0, 0), piece_color='b',
                        piece_move=(-1, 0), piece_output='b-R-a1')

    def test_move_is_illegal_diagonal(self):
        self._test_move(piece_type=Rook, piece_pos=(4, 4), piece_color='w',
                        piece_move=(5, 5), piece_output='w-R-e5')
        self._test_move(piece_type=Rook, piece_pos=(4, 4), piece_color='b',
                        piece_move=(3, 3), piece_output='b-R-e5')

    def test_move_is_illegal_taking_own_pawn(self):
        self._test_move(piece_type=Rook, piece_pos=(4, 4), piece_color='w',
                        piece_move=(4, 2), piece_output='w-R-e5',
                        piece2_type=Pawn, piece2_pos=(4, 2), piece2_color='w')
        self._test_move(piece_type=Rook, piece_pos=(4, 3), piece_color='b',
                        piece_move=(3, 3), piece_output='b-R-d5',
                        piece2_type=Pawn, piece2_pos=(3, 3), piece2_color='b')

    def test_move_is_illegal_piece_inbetween_vertical(self):
        self._test_move(piece_type=Rook, piece_pos=(4, 4), piece_color='w',
                        piece_move=(4, 2), piece_output='w-R-e5',
                        piece2_type=Pawn, piece2_pos=(4, 3), piece2_color='b')
        self._test_move(piece_type=Rook, piece_pos=(4, 3), piece_color='b',
                        piece_move=(1, 3), piece_output='b-R-d5',
                        piece2_type=Pawn, piece2_pos=(3, 3), piece2_color='w')

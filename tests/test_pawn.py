import unittest

from chesski.backend.game.pieces import Pawn, Rook, Knight, Bishop, Queen, King
from chesski.backend.game.board import ChessBoard

from tests.test_pieces import TestPiece


class TestPawn(TestPiece):

    def test_display(self):
        self._test_move(piece_type=Pawn, piece_pos=(1, 2), piece_color='w',
                        piece_output='w-P-c2')
        self._test_move(piece_type=Pawn, piece_pos=(6, 2), piece_color='b',
                        piece_output='b-P-c7')

###############################################################################
#                                Legal Moves
###############################################################################

    def test_move_is_legal_1up(self):
        self._test_move(piece_type=Pawn, piece_pos=(1, 2), piece_color='w',
                        piece_move=(2, 2), piece_output='w-P-c3')
        self._test_move(piece_type=Pawn, piece_pos=(6, 2), piece_color='b',
                        piece_move=(5, 2), piece_output='b-P-c6')

    def test_move_is_legal_2up(self):
        self._test_move(piece_type=Pawn, piece_pos=(1, 2), piece_color='w',
                        piece_move=(3, 2), piece_output='w-P-c4')
        self._test_move(piece_type=Pawn, piece_pos=(6, 2), piece_color='b',
                        piece_move=(4, 2), piece_output='b-P-c5')

    def test_move_is_legal_diagonal_left(self):
        self._test_move(piece_type=Pawn, piece_pos=(1, 2), piece_color='w',
                        piece_move=(2, 1), piece_output='w-P-b3',
                        piece2_type=Pawn, piece2_pos=(2, 1), piece2_color='b')
        self._test_move(piece_type=Pawn, piece_pos=(6, 2), piece_color='b',
                        piece_move=(5, 3), piece_output='b-P-d6',
                        piece2_type=Pawn, piece2_pos=(5, 3), piece2_color='w')

    def test_move_is_legal_diagonal_right(self):
        self._test_move(piece_type=Pawn, piece_pos=(1, 2), piece_color='w',
                        piece_move=(2, 3), piece_output='w-P-d3',
                        piece2_type=Pawn, piece2_pos=(2, 3), piece2_color='b')
        self._test_move(piece_type=Pawn, piece_pos=(6, 2), piece_color='b',
                        piece_move=(5, 1), piece_output='b-P-b6',
                        piece2_type=Pawn, piece2_pos=(5, 1), piece2_color='w')

###############################################################################
#                               Illegal Moves
################################################################################

    def test_move_is_illegal_1down(self):
        self._test_move(piece_type=Pawn, piece_pos=(1, 2), piece_color='w',
                        piece_move=(0, 2), piece_output='w-P-c2')
        self._test_move(piece_type=Pawn, piece_pos=(6, 2), piece_color='b',
                        piece_move=(7, 2), piece_output='b-P-c7')

    def test_move_is_illegal_2up_not_at_startrow(self):
        self._test_move(piece_type=Pawn, piece_pos=(3, 2), piece_color='w',
                        piece_move=(5, 2), piece_output='w-P-c4')
        self._test_move(piece_type=Pawn, piece_pos=(5, 2), piece_color='b',
                        piece_move=(3, 2), piece_output='b-P-c6')

    def test_move_is_illegal_2up_notempty_at_end(self):
        self._test_move(piece_type=Pawn, piece_pos=(1, 2), piece_color='w',
                        piece_move=(3, 2), piece_output='w-P-c2',
                        piece2_type=Pawn, piece2_pos=(3, 2), piece2_color='b')
        self._test_move(piece_type=Pawn, piece_pos=(6, 2), piece_color='b',
                        piece_move=(4, 2), piece_output='b-P-c7',
                        piece2_type=Pawn, piece2_pos=(4, 2), piece2_color='w')

    def test_move_is_illegal_2up_notempty_inbetween(self):
        self._test_move(piece_type=Pawn, piece_pos=(1, 2), piece_color='w',
                        piece_move=(3, 2), piece_output='w-P-c2',
                        piece2_type=Pawn, piece2_pos=(2, 2), piece2_color='b')
        self._test_move(piece_type=Pawn, piece_pos=(6, 2), piece_color='b',
                        piece_move=(4, 2), piece_output='b-P-c7',
                        piece2_type=Pawn, piece2_pos=(5, 2), piece2_color='b')

    def test_move_is_illegal_diagonal(self):
        self._test_move(piece_type=Pawn, piece_pos=(1, 2), piece_color='w',
                        piece_move=(0, 1), piece_output='w-P-c2',
                        piece2_type=Pawn, piece2_pos=(0, 1), piece2_color='b')
        self._test_move(piece_type=Pawn, piece_pos=(6, 2), piece_color='b',
                        piece_move=(7, 3), piece_output='b-P-c7',
                        piece2_type=Pawn, piece2_pos=(7, 3), piece2_color='b')

import unittest

from chesski.backend.game.pieces import Pawn, Rook, Knight, Bishop, Queen, King
from chesski.backend.game.board import ChessBoard

from tests.test_pieces import TestPiece


class TestKnight(TestPiece):

    def test_display(self):
        # Testing Knight display
        self._test_move(piece_type=Knight, piece_pos=(0, 0), piece_color='w',
                        piece_output='w-N-a1')
        self._test_move(piece_type=Knight, piece_pos=(4, 4), piece_color='b',
                        piece_output='b-N-e5')

###############################################################################
#                               Legal Moves
###############################################################################

    def test_move_is_legal_up_right(self):
        self._test_move(piece_type=Knight, piece_pos=(0, 0), piece_color='w',
                        piece_move=(2, 1), piece_output='w-N-b3')
        self._test_move(piece_type=Knight, piece_pos=(4, 4), piece_color='b',
                        piece_move=(2, 3), piece_output='b-N-d3')

    def test_move_is_legal_down_left(self):
        self._test_move(piece_type=Knight, piece_pos=(0, 6), piece_color='w',
                        piece_move=(2, 5), piece_output='w-N-f3')
        self._test_move(piece_type=Knight, piece_pos=(4, 4), piece_color='b',
                        piece_move=(6, 5), piece_output='b-N-f7')

    def test_move_is_legal_take_rook(self):
        self._test_move(piece_type=Knight, piece_pos=(0, 6), piece_color='w',
                        piece_move=(2, 5), piece_output='w-N-f3',
                        piece2_type=Rook, piece2_pos=(2, 5), piece2_color='b')
        self._test_move(piece_type=Knight, piece_pos=(4, 4), piece_color='b',
                        piece_move=(6, 5), piece_output='b-N-f7',
                        piece2_type=Rook, piece2_pos=(6, 5), piece2_color='w')

###############################################################################
#                               Illegal Moves
###############################################################################

    def test_move_is_illegal_2up(self):
        self._test_move(piece_type=Knight, piece_pos=(4, 4), piece_color='w',
                        piece_move=(6, 4), piece_output='w-N-e5')
        self._test_move(piece_type=Knight, piece_pos=(4, 3), piece_color='b',
                        piece_move=(2, 3), piece_output='b-N-d5')

    def test_move_is_illegal_diagonal(self):
        self._test_move(piece_type=Knight, piece_pos=(4, 4), piece_color='w',
                        piece_move=(5, 5), piece_output='w-N-e5')
        self._test_move(piece_type=Knight, piece_pos=(4, 3), piece_color='b',
                        piece_move=(3, 2), piece_output='b-N-d5')

    def test_move_is_illegal_take_own_rook(self):
        self._test_move(piece_type=Knight, piece_pos=(0, 6), piece_color='w',
                        piece_move=(2, 5), piece_output='w-N-g1',
                        piece2_type=Rook, piece2_pos=(2, 5), piece2_color='w')
        self._test_move(piece_type=Knight, piece_pos=(4, 4), piece_color='b',
                        piece_move=(6, 5), piece_output='b-N-e5',
                        piece2_type=Rook, piece2_pos=(6, 5), piece2_color='b')

import unittest

from chesski.backend.game.pieces import Pawn, Rook, Knight, Bishop, Queen, King
from chesski.backend.game.board import ChessBoard

from tests.test_pieces import TestPiece


class TestQueen(TestPiece):

    def test_display(self):
        self._test_move(piece_type=Queen, piece_pos=(0, 0), piece_color='w',
                        piece_output='w-Q-a1')
        self._test_move(piece_type=Queen, piece_pos=(4, 4), piece_color='b',
                        piece_output='b-Q-e5')

###############################################################################
#                               Legal Moves
###############################################################################

    def test_move_is_legal_diagonal(self):
        self._test_move(piece_type=Queen, piece_pos=(0, 0), piece_color='w',
                        piece_move=(6, 6), piece_output='w-Q-g7')
        self._test_move(piece_type=Queen, piece_pos=(4, 4), piece_color='b',
                        piece_move=(2, 2), piece_output='b-Q-c3')

    def test_move_is_legal_straight(self):
        self._test_move(piece_type=Queen, piece_pos=(6, 6), piece_color='w',
                        piece_move=(6, 1), piece_output='w-Q-b7')
        self._test_move(piece_type=Queen, piece_pos=(1, 1), piece_color='b',
                        piece_move=(1, 6), piece_output='b-Q-g2')

    def test_move_is_take_knight(self):
        self._test_move(piece_type=Queen, piece_pos=(6, 6), piece_color='w',
                        piece_move=(1, 1), piece_output='w-Q-b2',
                        piece2_type=Knight, piece2_pos=(1, 1), piece2_color='b')
        self._test_move(piece_type=Queen, piece_pos=(1, 1), piece_color='b',
                        piece_move=(3, 3), piece_output='b-Q-d4',
                        piece2_type=Knight, piece2_pos=(3, 3), piece2_color='w')

###############################################################################
#                              Illegal Moves
###############################################################################

    def test_move_is_illegal_knight_movement(self):
        self._test_move(piece_type=Queen, piece_pos=(1, 2), piece_color='w',
                        piece_move=(3, 3), piece_output='w-Q-c2')
        self._test_move(piece_type=Queen, piece_pos=(5, 5), piece_color='b',
                        piece_move=(3, 4), piece_output='b-Q-f6')

    def test_move_is_illegal_diagonal_pawn_between(self):
        self._test_move(piece_type=Queen, piece_pos=(1, 1), piece_color='w',
                        piece_move=(5, 5), piece_output='w-Q-b2',
                        piece2_type=Pawn, piece2_pos=(2, 2), piece2_color='b')
        self._test_move(piece_type=Queen, piece_pos=(5, 5), piece_color='b',
                        piece_move=(1, 1), piece_output='b-Q-f6',
                        piece2_type=Pawn, piece2_pos=(3, 3), piece2_color='w')

    def test_move_is_illegal_straight_pawn_between(self):
        self._test_move(piece_type=Queen, piece_pos=(1, 1), piece_color='w',
                        piece_move=(5, 1), piece_output='w-Q-b2',
                        piece2_type=Pawn, piece2_pos=(2, 1), piece2_color='b')
        self._test_move(piece_type=Queen, piece_pos=(5, 5), piece_color='b',
                        piece_move=(5, 1), piece_output='b-Q-f6',
                        piece2_type=Pawn, piece2_pos=(5, 3), piece2_color='w')

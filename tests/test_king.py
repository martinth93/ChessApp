import unittest

from chesski.backend.game.pieces import Pawn, Rook, Knight, Bishop, Queen, King
from chesski.backend.game.board import ChessBoard

from tests.test_pieces import TestPiece


class TestKing(TestPiece):

    def test_display(self):
        """
        Testing to display a king with color and position.
        """
        self._test_move(piece_type=King, piece_pos=(0, 0), piece_color='w',
                        piece_output='w-K-a1')
        self._test_move(piece_type=King, piece_pos=(4, 4), piece_color='b',
                        piece_output='b-K-e5')

###############################################################################
#                              Legal Moves
###############################################################################

    def test_move_is_legal_diagonal(self):
        """
        King moving one field diagonal should update position.
        """
        self._test_move(piece_type=King, piece_pos=(0, 0), piece_color='w',
                        piece_move=(1, 1), piece_output='w-K-b2')
        self._test_move(piece_type=King, piece_pos=(4, 4), piece_color='b',
                        piece_move=(5, 5), piece_output='b-K-f6')

    def test_move_is_legal_straight(self):
        """
        King moving one field horizontal/vertical should update position.
        """
        self._test_move(piece_type=King, piece_pos=(0, 0), piece_color='w',
                        piece_move=(1, 0), piece_output='w-K-a2')
        self._test_move(piece_type=King, piece_pos=(4, 4), piece_color='b',
                        piece_move=(4, 5), piece_output='b-K-f5')

    def test_move_is_take_knight(self):
        """
        King taking knight should update position.
        """
        self._test_move(piece_type=King, piece_pos=(0, 0), piece_color='w',
                        piece_move=(1, 0), piece_output='w-K-a2',
                        piece2_type=Knight, piece2_pos=(1, 0), piece2_color='b')
        self._test_move(piece_type=King, piece_pos=(4, 4), piece_color='b',
                        piece_move=(4, 5), piece_output='b-K-f5',
                        piece2_type=Knight, piece2_pos=(4, 5), piece2_color='w')

###############################################################################
#                              Illegal Moves
###############################################################################

    def test_move_is_illegal_2up(self):
        """
        King moving two fields vertical/horizontal
        shouldn't update position and raise Error.
        """
        self._test_move(piece_type=King, piece_pos=(0, 0), piece_color='w',
                        piece_move=(2, 0), piece_output='w-K-a1')
        self._test_move(piece_type=King, piece_pos=(4, 4), piece_color='b',
                        piece_move=(4, 2), piece_output='b-K-e5')

    def test_move_is_illegal_diagonal_far(self):
        """
        King moving three fields diagonal shouldn't update position
        and raise Error.
        """
        self._test_move(piece_type=King, piece_pos=(0, 0), piece_color='w',
                        piece_move=(3, 3), piece_output='w-K-a1')
        self._test_move(piece_type=King, piece_pos=(4, 4), piece_color='b',
                        piece_move=(1, 1), piece_output='b-K-e5')

    def test_move_is_illegal_taking_own_pawn(self):
        """
        King moving to field with same-colored Pawn shouldn't update position
        and raise Error.
        """
        self._test_move(piece_type=King, piece_pos=(0, 0), piece_color='w',
                        piece_move=(1, 0), piece_output='w-K-a1',
                        piece2_type=Pawn, piece2_pos=(1, 0), piece2_color='w')
        self._test_move(piece_type=King, piece_pos=(4, 4), piece_color='b',
                        piece_move=(4, 5), piece_output='b-K-e5',
                        piece2_type=Pawn, piece2_pos=(4, 5), piece2_color='b')

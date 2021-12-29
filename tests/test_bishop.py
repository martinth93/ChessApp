import unittest

from chesski.backend.game.pieces import Pawn, Rook, Knight, Bishop, Queen, King
from chesski.backend.game.board import ChessBoard

from tests.test_pieces import TestPiece


class TestBishop(TestPiece):

    def test_display(self):
        """
        Testing to display a Bishop with color and position.
        """
        self._test_move(piece_type=Bishop, piece_pos=(0, 0), piece_color='w',
                        piece_output='w-B-a1')
        self._test_move(piece_type=Bishop, piece_pos=(4, 4), piece_color='b',
                        piece_output='b-B-e5')

###############################################################################
#                               Legal Moves
###############################################################################

    def test_move_is_legal_up_right(self):
        """
        Bishop moving one field up and one to the right should update position.
        """
        self._test_move(piece_type=Bishop, piece_pos=(0, 0), piece_color='w',
                        piece_move=(1, 1), piece_output='w-B-b2')
        self._test_move(piece_type=Bishop, piece_pos=(4, 4), piece_color='b',
                        piece_move=(3, 3), piece_output='b-B-d4')

    def test_move_is_legal_down_left(self):
        """
        Bishop moving diagonal several fields down-left should update position.
        """
        self._test_move(piece_type=Bishop, piece_pos=(7, 7), piece_color='w',
                        piece_move=(1, 1), piece_output='w-B-b2')
        self._test_move(piece_type=Bishop, piece_pos=(0, 0), piece_color='b',
                        piece_move=(3, 3), piece_output='b-B-d4')

    def test_move_is_legal_take_knight(self):
        """
        Bishop taking knight should update position.
        """
        self._test_move(piece_type=Bishop, piece_pos=(7, 7), piece_color='w',
                        piece_move=(1, 1), piece_output='w-B-b2',
                        piece2_type=Knight, piece2_pos=(1, 1), piece2_color='b')
        self._test_move(piece_type=Bishop, piece_pos=(0, 0), piece_color='b',
                        piece_move=(3, 3), piece_output='b-B-d4',
                        piece2_type=Knight, piece2_pos=(3, 3), piece2_color='w')

###############################################################################
#                               Illegal Moves
###############################################################################

    def test_move_is_illegal_1up(self):
        """
        Bishop moving one field up shouldn't update position and raise Error.
        """
        self._test_move(piece_type=Bishop, piece_pos=(1, 1), piece_color='w',
                        piece_move=(2, 1), piece_output='w-B-b2',
                        expected_error=ValueError,
                        expected_msg='Move failed: Cannot move bishop like that.')
        self._test_move(piece_type=Bishop, piece_pos=(0, 0), piece_color='b',
                        piece_move=(1, 0), piece_output='b-B-a1',
                        expected_error=ValueError,
                        expected_msg='Move failed: Cannot move bishop like that.')

    def test_move_is_illegal_diagonal_pawn_between(self):
        """
        Bishop moving several fields diagonal through black pawn
        shouldn't update position and raise Error.
        """
        self._test_move(piece_type=Bishop, piece_pos=(7, 7), piece_color='w',
                        piece_move=(1, 1), piece_output='w-B-h8',
                        piece2_type=Pawn, piece2_pos=(2, 2), piece2_color='b',
                        expected_error=ValueError,
                        expected_msg='Move failed: Cannot move bishop like that.')
        self._test_move(piece_type=Bishop, piece_pos=(0, 0), piece_color='b',
                        piece_move=(5, 5), piece_output='b-B-a1',
                        piece2_type=Pawn, piece2_pos=(3, 3), piece2_color='w',
                        expected_error=ValueError,
                        expected_msg='Move failed: Cannot move bishop like that.')

    def test_move_is_illegal_take_own_knight(self):
        """
        Bishop taking same-colored knight should not update position and
        raise Error.
        """
        self._test_move(piece_type=Bishop, piece_pos=(7, 7), piece_color='w',
                        piece_move=(1, 1), piece_output='w-B-h8',
                        piece2_type=Knight, piece2_pos=(1, 1), piece2_color='w',
                        expected_error=ValueError,
                        expected_msg='Move failed: Field blocked by another same-colored piece.')
        self._test_move(piece_type=Bishop, piece_pos=(0, 0), piece_color='b',
                        piece_move=(3, 3), piece_output='b-B-a1',
                        piece2_type=Knight, piece2_pos=(3, 3), piece2_color='b',
                        expected_error=ValueError,
                        expected_msg='Move failed: Field blocked by another same-colored piece.')

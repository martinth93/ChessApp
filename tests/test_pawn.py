import unittest

from chesski.backend.game.pieces import Pawn, Rook, Knight, Bishop, Queen, King
from chesski.backend.game.board import ChessBoard

from tests.test_pieces import TestPiece


class TestPawn(TestPiece):
    """
    Testing of legal and illegal move.
    Each test contains two subtests whith the same game-scenario:
        One where a white Pawn makes a legal/illegal move
        One where a black Pawn makes a legal/illegal move
    """

    def test_display(self):
        """
        Testing to display a Pawn with color and position.
        """
        self._test_move(piece_type=Pawn, piece_pos=(1, 2), piece_color='w',
                        piece_output='w-P-c2')
        self._test_move(piece_type=Pawn, piece_pos=(6, 2), piece_color='b',
                        piece_output='b-P-c7')

###############################################################################
#                                Legal Moves
###############################################################################

    def test_move_is_legal_1up(self):
        """
        Pawn moving one field up to an empty field should update postion
        from c2 to c3.
        """
        self._test_move(piece_type=Pawn, piece_pos=(1, 2), piece_color='w',
                        piece_move=(2, 2), piece_output='w-P-c3')
        self._test_move(piece_type=Pawn, piece_pos=(6, 2), piece_color='b',
                        piece_move=(5, 2), piece_output='b-P-c6')

    def test_move_is_legal_2up(self):
        """
        Pawn moving two field up to an empty field should update postion
        if pawn is on starting row 1.
        """
        self._test_move(piece_type=Pawn, piece_pos=(1, 2), piece_color='w',
                        piece_move=(3, 2), piece_output='w-P-c4')
        self._test_move(piece_type=Pawn, piece_pos=(6, 2), piece_color='b',
                        piece_move=(4, 2), piece_output='b-P-c5')

    def test_move_is_legal_diagonal_left(self):
        """
        Pawn moving one left and one up to a field with a piece (not empty)
        should update postion.
        """
        self._test_move(piece_type=Pawn, piece_pos=(1, 2), piece_color='w',
                        piece_move=(2, 1), piece_output='w-P-b3',
                        piece2_type=Pawn, piece2_pos=(2, 1), piece2_color='b')
        self._test_move(piece_type=Pawn, piece_pos=(6, 2), piece_color='b',
                        piece_move=(5, 3), piece_output='b-P-d6',
                        piece2_type=Pawn, piece2_pos=(5, 3), piece2_color='w')

    def test_move_is_legal_diagonal_right(self):
        """
        Pawn moving one right and one up to a field with a piece (not empty)
        should update postion.
        """
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
        """
        Pawn moving one down to an empty field should raise ValueError and
        not update postion.
        """
        self._test_move(piece_type=Pawn, piece_pos=(1, 2), piece_color='w',
                        piece_move=(0, 2), piece_output='w-P-c2',
                        expected_error=ValueError,
                        expected_msg='Move failed: Cannot move pawn like that.')
        self._test_move(piece_type=Pawn, piece_pos=(6, 2), piece_color='b',
                        piece_move=(7, 2), piece_output='b-P-c7',
                        expected_error=ValueError,
                        expected_msg='Move failed: Cannot move pawn like that.')

    def test_move_is_illegal_2up_not_at_startrow(self):
        """
        Pawn moving two up to an empty field while not being at starting
        position should raise ValueError and not update postion.
        """
        self._test_move(piece_type=Pawn, piece_pos=(3, 2), piece_color='w',
                        piece_move=(5, 2), piece_output='w-P-c4',
                        expected_error=ValueError,
                        expected_msg='Move failed: Cannot move pawn like that.')
        self._test_move(piece_type=Pawn, piece_pos=(5, 2), piece_color='b',
                        piece_move=(3, 2), piece_output='b-P-c6',
                        expected_error=ValueError,
                        expected_msg='Move failed: Cannot move pawn like that.')

    def test_move_is_illegal_2up_notempty_at_end(self):
        """
        Pawn moving two up to an non-empty field while being at starting
        position should raise ValueError and not update postion.
        """
        self._test_move(piece_type=Pawn, piece_pos=(1, 2), piece_color='w',
                        piece_move=(3, 2), piece_output='w-P-c2',
                        piece2_type=Pawn, piece2_pos=(3, 2), piece2_color='b',
                        expected_error=ValueError,
                        expected_msg='Move failed: Cannot move pawn like that.')
        self._test_move(piece_type=Pawn, piece_pos=(6, 2), piece_color='b',
                        piece_move=(4, 2), piece_output='b-P-c7',
                        piece2_type=Pawn, piece2_pos=(4, 2), piece2_color='w',
                        expected_error=ValueError,
                        expected_msg='Move failed: Cannot move pawn like that.')

    def test_move_is_illegal_2up_notempty_inbetween(self):
        """
        Pawn moving two up to an non-empty field inbetween
        while being at starting position should raise ValueError and
        not change position.
        """
        self._test_move(piece_type=Pawn, piece_pos=(1, 2), piece_color='w',
                        piece_move=(3, 2), piece_output='w-P-c2',
                        piece2_type=Pawn, piece2_pos=(2, 2), piece2_color='b',
                        expected_error=ValueError,
                        expected_msg='Move failed: Cannot move pawn like that.')
        self._test_move(piece_type=Pawn, piece_pos=(6, 2), piece_color='b',
                        piece_move=(4, 2), piece_output='b-P-c7',
                        piece2_type=Pawn, piece2_pos=(5, 2), piece2_color='b',
                        expected_error=ValueError,
                        expected_msg='Move failed: Cannot move pawn like that.')

    def test_move_is_illegal_diagonal(self):
        """
        Pawn moving diagonal down left to an non-empty field
        should raise ValueError and not change position.
        """
        self._test_move(piece_type=Pawn, piece_pos=(1, 2), piece_color='w',
                        piece_move=(0, 1), piece_output='w-P-c2',
                        piece2_type=Pawn, piece2_pos=(0, 1), piece2_color='b',
                        expected_error=ValueError,
                        expected_msg='Move failed: Cannot move pawn like that.')
        self._test_move(piece_type=Pawn, piece_pos=(6, 2), piece_color='b',
                        piece_move=(7, 3), piece_output='b-P-c7',
                        piece2_type=Pawn, piece2_pos=(7, 3), piece2_color='b',
                        expected_error=ValueError,
                        expected_msg='Move failed: Field blocked by another same-colored piece.')

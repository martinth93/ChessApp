import unittest

from chesski.backend.game.pieces import Pawn
from chesski.backend.game.board import ChessBoard


#########################################################
#                      Testing
#                       Pawns
########################################################

class TestWhitePawn(unittest.TestCase):

    def setUp(self):
        self.chessboard = ChessBoard()
        self.pawn = Pawn(position=(1, 2), color='w',
                                chessboard=self.chessboard)

    def test_display(self):
        """
        Testing to display a Pawn with id and position.
        """
        correct_output = "w-P-c2"
        generated_output = self.pawn.display()
        self.assertEqual(correct_output, generated_output)

    def test_move_is_legal_1up(self):
        """
        White Pawn moving one field up to an empty field should update postion
        from c2 to c3.
        """
        self.pawn.move(new_pos=(2, 2))
        generated_output = self.pawn.display()
        correct_output = "w-P-c3"
        self.assertEqual(correct_output, generated_output)

    def test_move_is_legal_2up(self):
        """
        White Pawn moving two field up to an empty field should update postion
        if pawn is on starting row 1.
        Position should update from c2 to c4
        """
        self.pawn.move(new_pos=(3, 2))
        generated_output = self.pawn.display()
        correct_output = "w-P-c4"
        self.assertEqual(correct_output, generated_output)

    def test_move_is_legal_diagonal_left(self):
        """
        White Pawn moving one left and one up to a field with a piece (not empty)
        should update postion from c2 to b3.
        """
        Pawn(position=(2, 1), color='b', chessboard=self.chessboard)
        self.pawn.move(new_pos=(2, 1))
        generated_output = self.pawn.display()
        correct_output = "w-P-b3"
        self.assertEqual(correct_output, generated_output)

    def test_move_is_legal_diagonal_right(self):
        """
        White Pawn moving one right and one up to a field with a piece (not empty)
        should update postion from c2 to d3.
        """
        Pawn(position=(2, 3), color='b', chessboard=self.chessboard)
        self.pawn.move(new_pos=(2, 3))
        generated_output = self.pawn.display()
        correct_output = "w-P-d3"
        self.assertEqual(correct_output, generated_output)

    # ------------------testing illegal moves ------------------------------

    def test_move_is_illegal_1down(self):
        """
        White Pawn moving one down to an empty field
        should not update postion from c2.
        """
        self.pawn.move(new_pos=(0, 2))
        generated_output = self.pawn.display()
        correct_output = "w-P-c2"
        self.assertEqual(correct_output, generated_output)

    def test_move_is_illegal_2up_not_at_startrow(self):
        """
        White Pawn moving two up to an empty field
        while not being at starting position should not update postion from c2.
        """
        pawn_2 = Pawn(position=(3, 2), color='w', chessboard=self.chessboard)
        pawn_2.move(new_pos=(5, 2))
        generated_output = pawn_2.display()
        correct_output = "w-P-c4"
        self.assertEqual(correct_output, generated_output)

    def test_move_is_illegal_2up_notempty_at_end(self):
        """
        White Pawn moving two up to an non-empty field
        while being at starting position should not update postion from c2.
        """
        pawn_2 = Pawn(position=(3, 2), color='w', chessboard=self.chessboard)
        self.pawn.move(new_pos=(3, 2))
        generated_output = self.pawn.display()
        correct_output = "w-P-c2"
        self.assertEqual(correct_output, generated_output)

    def test_move_is_illegal_2up_notempty_inbetween(self):
        """
        White Pawn moving two up to an non-empty field inbetween
        while being at starting position should not update postion from c2.
        """
        pawn_2 = Pawn(position=(2, 2), color='w', chessboard=self.chessboard)
        self.pawn.move(new_pos=(3, 2))
        generated_output = self.pawn.display()
        correct_output = "w-P-c2"
        self.assertEqual(correct_output, generated_output)

    def test_move_is_illegal_diagonal(self):
        """
        White Pawn moving diagonal down left to an non-empty field
        should not change position from c2.
        """
        pawn_2 = Pawn(position=(0, 1), color='w', chessboard=self.chessboard)
        self.pawn.move(new_pos=(0, 1))
        generated_output = self.pawn.display()
        correct_output = "w-P-c2"
        self.assertEqual(correct_output, generated_output)

# ---------------------------- Test Black Pawn ---------------------------------

class TestBlackPawn(unittest.TestCase):

    def setUp(self):
        self.chessboard = ChessBoard()
        self.pawn = Pawn(position=(6, 2), color='b', chessboard=self.chessboard)

    def test_display(self):
        """
        Testing to display a Pawn with position.
        """
        correct_output = "b-P-c7"
        generated_output = self.pawn.display()
        self.assertEqual(correct_output, generated_output)

    def test_move_is_legal_1down(self):
        """
        Black Pawn moving one field down to an empty field should update postion
        from c7 to c6.
        """
        self.pawn.move(new_pos=(5, 2))
        generated_output = self.pawn.display()
        correct_output = "b-P-c6"
        self.assertEqual(correct_output, generated_output)

    def test_move_is_legal_2down(self):
        """
        Black Pawn moving two field down to an empty field should update postion
        if pawn is on starting row 6.
        Position should update from c7 to c5
        """
        self.pawn.move(new_pos=(4, 2))
        generated_output = self.pawn.display()
        correct_output = "b-P-c5"
        self.assertEqual(correct_output, generated_output)

    def test_move_is_legal_diagonal_left(self):
        """
        Black Pawn moving one left and one down to a field with a piece (not empty)
        should update postion from c7 to b6.
        """
        Pawn(position=(5, 1), color='w', chessboard=self.chessboard)
        self.pawn.move(new_pos=(5, 1))
        generated_output = self.pawn.display()
        correct_output = "b-P-b6"
        self.assertEqual(correct_output, generated_output)

    def test_move_is_legal_diagonal_right(self):
        """
        Black Pawn moving one right and one down to a field with a piece (not empty)
        should update postion from c7 to d6.
        """
        Pawn(position=(5, 3), color='w', chessboard=self.chessboard)
        self.pawn.move(new_pos=(5, 3))
        generated_output = self.pawn.display()
        correct_output = "b-P-d6"
        self.assertEqual(correct_output, generated_output)

    # ------------------testing illegal moves ------------------------------

    def test_move_is_illegal_1up(self):
        """
        Black Pawn moving one up to an empty field
        should not update postion from c7.
        """
        self.pawn.move(new_pos=(7, 2))
        generated_output = self.pawn.display()
        correct_output = "b-P-c7"
        self.assertEqual(correct_output, generated_output)

    def test_move_is_illegal_2down_not_at_startrow(self):
        """
        Black Pawn moving two down to an empty field
        while not being at starting position should not update postion from c5.
        """
        pawn_2 = Pawn(position=(4, 2), color='b', chessboard=self.chessboard)
        pawn_2.move(new_pos=(2, 2))
        generated_output = pawn_2.display()
        correct_output = "b-P-c5"
        self.assertEqual(correct_output, generated_output)

    def test_move_is_illegal_2down_notempty_at_end(self):
        """
        Black Pawn moving two down to an non-empty field
        while being at starting position should not update postion from c7.
        """
        pawn_2 = Pawn(position=(4, 2), color='w', chessboard=self.chessboard)
        self.pawn.move(new_pos=(4, 2))
        generated_output = self.pawn.display()
        correct_output = "b-P-c7"
        self.assertEqual(correct_output, generated_output)

    def test_move_is_illegal_2down_notempty_inbetween(self):
        """
        Black Pawn moving two down to an non-empty field inbetween
        while being at starting position should not update postion from c7.
        """
        pawn_2 = Pawn(position=(5, 2), color='b', chessboard=self.chessboard)
        self.pawn.move(new_pos=(4, 2))
        generated_output = self.pawn.display()
        correct_output = "b-P-c7"
        self.assertEqual(correct_output, generated_output)

    def test_move_is_illegal_diagonal(self):
        """
        Black Pawn moving diagonal up left to an non-empty field
        should not change position from c7.
        """
        pawn_2 = Pawn(position=(7, 1), color='w', chessboard=self.chessboard)
        self.pawn.move(new_pos=(7, 1))
        generated_output = self.pawn.display()
        correct_output = "b-P-c7"
        self.assertEqual(correct_output, generated_output)

import unittest

from chesski.backend.game.pieces import Pawn, Rook, Knight, Bishop, Queen, King
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
        Testing to display a Pawn with color and position.
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

#########################################################
#                      Testing
#                       Rook
########################################################

class TestRook(unittest.TestCase):

    def setUp(self):
        self.chessboard = ChessBoard()
        self.rook1 = Rook(position=(0, 0), color='w',
                                chessboard=self.chessboard)
        self.rook2 = Rook(position=(4, 4), color='b',
                                chessboard=self.chessboard)

    def test_display(self):
        """
        Testing to display a Rook with color and position.
        """
        correct_output = "w-R-a1"
        generated_output = self.rook1.display()
        self.assertEqual(correct_output, generated_output)


    def test_move_is_legal_1up(self):
        """
        White Rook moving one field up to an empty field should update position
        from a1 to a2.
        """
        self.rook1.move(new_pos=(1, 0))
        generated_output = self.rook1.display()
        correct_output = "w-R-a2"
        self.assertEqual(correct_output, generated_output)

    def test_move_is_legal_1down(self):
        """
        Black Rook moving one field down to an empty field should update position
        from e5 to e4.
        """
        self.rook2.move(new_pos=(3, 4))
        generated_output = self.rook2.display()
        correct_output = "b-R-e4"
        self.assertEqual(correct_output, generated_output)

    def test_move_is_legal_7up(self):
        """
        White Rook moving seven fields up to an empty field should update position
        from a1 to a8.
        """
        self.rook1.move(new_pos=(7, 0))
        generated_output = self.rook1.display()
        correct_output = "w-R-a8"
        self.assertEqual(correct_output, generated_output)

    def test_move_is_legal_4down(self):
        """
        Black Rook moving four fields down to an empty field should update position
        from e5 to e1.
        """
        self.rook2.move(new_pos=(0, 4))
        generated_output = self.rook2.display()
        correct_output = "b-R-e1"
        self.assertEqual(correct_output, generated_output)

    def test_move_is_legal_1right(self):
        """
        White Rook moving one field right to an empty field should update postion
        from a1 to b1.
        """
        self.rook1.move(new_pos=(0, 1))
        generated_output = self.rook1.display()
        correct_output = "w-R-b1"
        self.assertEqual(correct_output, generated_output)

    def test_move_is_legal_1left(self):
        """
        Black Rook moving one field left to an empty field should update postion
        from e5 to d5.
        """
        self.rook2.move(new_pos=(4, 3))
        generated_output = self.rook2.display()
        correct_output = "b-R-d5"
        self.assertEqual(correct_output, generated_output)

    def test_move_is_legal_4left(self):
        """
        Black Rook moving four fields left to an empty field should update
        postion from e5 to a5.
        """
        self.rook2.move(new_pos=(4, 0))
        generated_output = self.rook2.display()
        correct_output = "b-R-a5"
        self.assertEqual(correct_output, generated_output)

    def test_move_is_legal_taking_rook(self):
        """
        Black Rook moving four fields left, and white Rook moving four fields up
        should result in white rook taking black rook and update
        postion from a1 to a5.
        """
        self.rook1.move(new_pos=(4, 0))
        self.rook2.move(new_pos=(4, 0))
        generated_output = self.rook1.display()
        correct_output = "w-R-a5"
        self.assertEqual(correct_output, generated_output)

    def test_move_is_legal_taking_opponents_pawn(self):
        """
        White Rook moving two fields up to a field whith a black pawn on it
        should update position from a1 to a3.
        """
        Pawn(position=(2, 0), color='b', chessboard=self.chessboard)
        self.rook1.move(new_pos=(2, 0))
        generated_output = self.rook1.display()
        correct_output = "w-R-a3"
        self.assertEqual(correct_output, generated_output)

 # ------------------testing illegal moves ------------------------------

    def test_move_is_illegal_out_of_board(self):
        """
        White Rook moving one field down to a field  out of the board
        shouldn't update position from a1.
        """
        self.rook1.move(new_pos=(-1, 0))
        generated_output = self.rook1.display()
        correct_output = "w-R-a1"
        self.assertEqual(correct_output, generated_output)

    def test_move_is_illegal_diagonal(self):
        """
        White Rook moving one field up and one field right
        shouldn't update position from a1.
        """
        self.rook1.move(new_pos=(1, 1))
        generated_output = self.rook1.display()
        correct_output = "w-R-a1"
        self.assertEqual(correct_output, generated_output)

    def test_move_is_illegal_taking_own_pawn(self):
        """
        White Rook moving two fields up to a field whith a white pawn on it
        should't update position from a1.
        """
        Pawn(position=(2, 0), color='w', chessboard=self.chessboard)
        self.rook1.move(new_pos=(2, 0))
        generated_output = self.rook1.display()
        correct_output = "w-R-a1"
        self.assertEqual(correct_output, generated_output)

    def test_move_is_illegal_piece_inbetween_vertical(self):
        """
        White Rook moving two fields up but field inbetween has pawn on it
        should't update position from a1.
        """
        Pawn(position=(1, 0), color='w', chessboard=self.chessboard)
        self.rook1.move(new_pos=(2, 0))
        generated_output = self.rook1.display()
        correct_output = "w-R-a1"
        self.assertEqual(correct_output, generated_output)

    def test_move_is_illegal_piece_inbetween_horizontal(self):
        """
        White Rook moving six fields right but field inbetween has pawn on it
        should't update position from a1.
        """
        Pawn(position=(0, 3), color='b', chessboard=self.chessboard)
        self.rook1.move(new_pos=(0, 6))
        generated_output = self.rook1.display()
        correct_output = "w-R-a1"
        self.assertEqual(correct_output, generated_output)


#########################################################
#                      Testing
#                       Knight
########################################################

class TestKnight(unittest.TestCase):

    def setUp(self):
        self.chessboard = ChessBoard()
        self.knight1 = Knight(position=(0, 1), color='w',
                                chessboard=self.chessboard)
        self.knight2 = Knight(position=(4, 4), color='b',
                                chessboard=self.chessboard)

    def test_display(self):
        """
        Testing to display a Knight with color and position.
        """
        correct_output = "w-N-b1"
        generated_output = self.knight1.display()
        self.assertEqual(correct_output, generated_output)


    def test_move_is_legal_up_right(self):
        """
        White Knight moving two fields up and one to the right should update
        position from b1 to c3.
        """
        self.knight1.move(new_pos=(2, 2))
        generated_output = self.knight1.display()
        correct_output = "w-N-c3"
        self.assertEqual(correct_output, generated_output)

    def test_move_is_legal_down_left(self):
        """
        Black Knight moving two fields down and one to the left should update
        position from e5 to d3.
        """
        self.knight2.move(new_pos=(2, 3))
        generated_output = self.knight2.display()
        correct_output = "b-N-d3"
        self.assertEqual(correct_output, generated_output)

    def test_move_is_legal_down_right(self):
        """
        Black Knight moving two fields down and one to the left should update
        position from e5 to f3.
        """
        self.knight2.move(new_pos=(2, 5))
        generated_output = self.knight2.display()
        correct_output = "b-N-f3"
        self.assertEqual(correct_output, generated_output)


 # ------------------testing illegal moves ------------------------------

    def test_move_is_illegal_2up(self):
        """
        White Knight moving two fields up shouldn't update position from b1.
        """
        self.knight1.move(new_pos=(2, 1))
        generated_output = self.knight1.display()
        correct_output = "w-N-b1"
        self.assertEqual(correct_output, generated_output)

    def test_move_is_illegal_diagonal_1(self):
        """
        White Knight moving one field up and to the right
        shouldn't update position from b1.
        """
        self.knight1.move(new_pos=(1, 2))
        generated_output = self.knight1.display()
        correct_output = "w-N-b1"
        self.assertEqual(correct_output, generated_output)


#########################################################
#                      Testing
#                       Bishop
########################################################

class TestBishop(unittest.TestCase):

    def setUp(self):
        self.chessboard = ChessBoard()
        self.bishop1 = Bishop(position=(0, 2), color='w',
                                chessboard=self.chessboard)
        self.bishop2 = Bishop(position=(4, 4), color='b',
                                chessboard=self.chessboard)

    def test_display(self):
        """
        Testing to display a Bishop with color and position.
        """
        correct_output = "w-B-c1"
        generated_output = self.bishop1.display()
        self.assertEqual(correct_output, generated_output)


    def test_move_is_legal_up_right(self):
        """
        White Bishop moving one field up and one to the right should update
        position from c1 to d2.
        """
        self.bishop1.move(new_pos=(1, 3))
        generated_output = self.bishop1.display()
        correct_output = "w-B-d2"
        self.assertEqual(correct_output, generated_output)

    def test_move_is_legal_down_left(self):
        """
        Black Bishop moving four fields down and four to the left should update
        position from e5 to a1.
        """
        self.bishop2.move(new_pos=(0, 0))
        generated_output = self.bishop2.display()
        correct_output = "b-B-a1"
        self.assertEqual(correct_output, generated_output)

    def test_move_is_take_knight(self):
        """
        Black Bishop taking knight should update position
        from c1 to h6.
        """
        Knight(position=(5, 7), color='b', chessboard=self.chessboard)
        self.bishop1.move(new_pos=(5, 7))
        generated_output = self.bishop1.display()
        correct_output = "w-B-h6"
        self.assertEqual(correct_output, generated_output)


 # ------------------testing illegal moves ------------------------------

    def test_move_is_illegal_1up(self):
        """
        White Bishop moving one field up shouldn't update position from c1.
        """
        self.bishop1.move(new_pos=(1, 2))
        generated_output = self.bishop1.display()
        correct_output = "w-B-c1"
        self.assertEqual(correct_output, generated_output)

    def test_move_is_illegal_diagonal_pawn_between(self):
        """
        White Bishop moving four fields up and four to the right
        through black pawn on shouldn't update position from b1.
        """
        Pawn(position=(3, 5), color='b', chessboard=self.chessboard)
        self.bishop1.move(new_pos=(5, 7))
        generated_output = self.bishop1.display()
        correct_output = "w-B-c1"
        self.assertEqual(correct_output, generated_output)


#########################################################
#                      Testing
#                       Queen
########################################################

class TestQueen(unittest.TestCase):

    def setUp(self):
        self.chessboard = ChessBoard()
        self.queen1 = Queen(position=(0, 3), color='w',
                                chessboard=self.chessboard)
        self.queen2 = Queen(position=(4, 4), color='b',
                                chessboard=self.chessboard)

    def test_display(self):
        """
        Testing to display a Queen with color and position.
        """
        correct_output = "w-Q-d1"
        generated_output = self.queen1.display()
        self.assertEqual(correct_output, generated_output)


    def test_move_is_legal_up_right(self):
        """
        White Queen moving one field up and one to the right should update
        position from d1 to e2.
        """
        self.queen1.move(new_pos=(1, 4))
        generated_output = self.queen1.display()
        correct_output = "w-Q-e2"
        self.assertEqual(correct_output, generated_output)

    def test_move_is_legal_down_left_4(self):
        """
        Black Queen moving four fields down and four to the left should update
        position from e5 to a1.
        """
        self.queen2.move(new_pos=(0, 0))
        generated_output = self.queen2.display()
        correct_output = "b-Q-a1"
        self.assertEqual(correct_output, generated_output)

    def test_move_is_take_knight(self):
        """
        White Queen taking knight should update position
        from d1 to h5.
        """
        Knight(position=(4, 7), color='b', chessboard=self.chessboard)
        self.queen1.move(new_pos=(4, 7))
        generated_output = self.queen1.display()
        correct_output = "w-Q-h5"
        self.assertEqual(correct_output, generated_output)


 # ------------------testing illegal moves ------------------------------

    def test_move_is_illegal_1up(self):
        """
        White Queen moving two fields up and one right (knight pattern)
        shouldn't update position from d1.
        """
        self.queen1.move(new_pos=(2, 4))
        generated_output = self.queen1.display()
        correct_output = "w-Q-d1"
        self.assertEqual(correct_output, generated_output)

    def test_move_is_illegal_diagonal_pawn_between(self):
        """
        White Queen moving four fields up and four to the right
        through black pawn shouldn't update position from b1.
        """
        Pawn(position=(3, 6), color='b', chessboard=self.chessboard)
        self.queen1.move(new_pos=(4, 7))
        generated_output = self.queen1.display()
        correct_output = "w-Q-d1"
        self.assertEqual(correct_output, generated_output)

    def test_move_is_illegal_straight_backwards_pawn_between(self):
        """
        Black Queen moving three fields down through black pawn
        shouldn't update position from b1.
        """
        Pawn(position=(3, 4), color='b', chessboard=self.chessboard)
        self.queen2.move(new_pos=(1, 4))
        generated_output = self.queen2.display()
        correct_output = "b-Q-e5"
        self.assertEqual(correct_output, generated_output)


#########################################################
#                      Testing
#                       King
########################################################

class TestKing(unittest.TestCase):

    def setUp(self):
        self.chessboard = ChessBoard()
        self.king1 = King(position=(0, 4), color='w',
                                chessboard=self.chessboard)
        self.king2 = King(position=(4, 4), color='b',
                                chessboard=self.chessboard)

    def test_display(self):
        """
        Testing to display a king with color and position.
        """
        correct_output = "w-K-e1"
        generated_output = self.king1.display()
        self.assertEqual(correct_output, generated_output)


    def test_move_is_legal_up_right(self):
        """
        White king moving one field up and one to the right should update
        position from e1 to f2.
        """
        self.king1.move(new_pos=(1, 5))
        generated_output = self.king1.display()
        correct_output = "w-K-f2"
        self.assertEqual(correct_output, generated_output)

    def test_move_is_legal_down_left(self):
        """
        Black king moving on fields down and one to the left should update
        position from e5 to d4.
        """
        self.king2.move(new_pos=(3, 3))
        generated_output = self.king2.display()
        correct_output = "b-K-d4"
        self.assertEqual(correct_output, generated_output)

    def test_move_is_take_knight(self):
        """
        White king taking knight should update position
        from e1 to d2.
        """
        Knight(position=(1, 3), color='b', chessboard=self.chessboard)
        self.king1.move(new_pos=(1, 3))
        generated_output = self.king1.display()
        correct_output = "w-K-d2"
        self.assertEqual(correct_output, generated_output)


 # ------------------testing illegal moves ------------------------------

    def test_move_is_illegal_2up(self):
        """
        White king moving two fields up
        shouldn't update position from e1.
        """
        self.king1.move(new_pos=(2, 4))
        generated_output = self.king1.display()
        correct_output = "w-K-e1"
        self.assertEqual(correct_output, generated_output)

    def test_move_is_illegal_diagonal_far(self):
        """
        White king moving three fields up and three to the right
        shouldn't update position from b1.
        """
        self.king1.move(new_pos=(3, 7))
        generated_output = self.king1.display()
        correct_output = "w-K-e1"
        self.assertEqual(correct_output, generated_output)

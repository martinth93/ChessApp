import unittest

from chesski.backend.game.board import ChessBoard
from chesski.backend.game.pieces import Pawn


class TestBoardSimple(unittest.TestCase):
    def test_initialize_state(self):
        """
        Initializing the state should yield empty board
        """
        chessboard = ChessBoard() # empty state parameter initializes state
        correct_state = [
                            [None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None]
                        ]
        generated_state = chessboard.state
        errormessage = f"generated state not correct \n {generated_state}"
        self.assertEqual(correct_state, generated_state, errormessage)

    def test_place_piece_on_field(self):
        """
        Placing a piece on the chessboard should modify the state correctly.
        """
        chessboard = ChessBoard()
        p1 = Pawn(position=(1, 3), color="w", chessboard=chessboard)
        correct_state = [
                            [None, None, None, None, None, None, None, None],
                            [None, None, None, p1, None, None, None, None],
                            [None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None]
                        ]
        generated_state = chessboard.state
        errormessage = f"generated state not correct \n {generated_state}"
        self.assertEqual(correct_state, generated_state, errormessage)

    def test_remove_piece_of_state(self):
        """
        Removing a piece of the chessboard by passing in the position.
        """
        chessboard = ChessBoard()
        p1 = Pawn(position=(1, 3), color="w", chessboard=chessboard)
        # pawn placed on (1, 3)
        chessboard.remove_piece_from_state(piece_pos=(1, 3))
        correct_state = [
                            [None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None],
                            [None, None, None, None, None, None, None, None]
                        ]
        generated_state = chessboard.state
        errormessage = f"generated state not correct \n {generated_state}"
        self.assertEqual(correct_state, generated_state, errormessage)

    def test_piece_on_field(self):
        """
        Function should return the corresponding piece on field of specified
        position.
        """
        chessboard = ChessBoard()
        p1 = Pawn(position=(1, 3), color="w", chessboard=chessboard)
        # pawn placed on (1, 3)
        correct_piece = p1
        generated_piece = chessboard.piece_on_field(piece_pos=(1, 3))
        errormessage = f"generated piece not correct \n {generated_piece}"
        self.assertEqual(correct_piece, generated_piece, errormessage)

class TestBoardKomplexPawn(unittest.TestCase):

    def setUp(self):
        self.chessboard = ChessBoard()
        self.p1 = Pawn(position=(1, 0), color="w", chessboard=self.chessboard)
        self.p2 = Pawn(position=(1, 1), color="w", chessboard=self.chessboard)
        self.p3 = Pawn(position=(1, 2), color="w", chessboard=self.chessboard)
        self.p4 = Pawn(position=(1, 3), color="w", chessboard=self.chessboard)
        self.p5 = Pawn(position=(1, 4), color="w", chessboard=self.chessboard)
        self.p6 = Pawn(position=(1, 5), color="w", chessboard=self.chessboard)
        self.p7 = Pawn(position=(1, 6), color="w", chessboard=self.chessboard)
        self.p8 = Pawn(position=(1, 7), color="w", chessboard=self.chessboard)

        self.p9 = Pawn(position=(6, 0), color="b", chessboard=self.chessboard)
        self.p10 = Pawn(position=(6, 1), color="b", chessboard=self.chessboard)
        self.p11 = Pawn(position=(6, 2), color="b", chessboard=self.chessboard)
        self.p12 = Pawn(position=(6, 3), color="b", chessboard=self.chessboard)
        self.p13 = Pawn(position=(6, 4), color="b", chessboard=self.chessboard)
        self.p14 = Pawn(position=(6, 5), color="b", chessboard=self.chessboard)
        self.p15 = Pawn(position=(6, 6), color="b", chessboard=self.chessboard)
        self.p16 = Pawn(position=(6, 7), color="b", chessboard=self.chessboard)


    def test_pawn_placement_big(self):
        """
        All Pawns should be placed at their right position inside state.
        """
        correct_state = [
    [   None,   None,    None,    None,    None,    None,      None,  None],
    [ self.p1, self.p2, self.p3, self.p4, self.p5, self.p6, self.p7, self.p8],
    [   None,   None,    None,    None,    None,    None,      None,   None],
    [   None,   None,    None,    None,    None,    None,      None,   None],
    [   None,   None,    None,    None,    None,    None,      None,   None],
    [   None,   None,    None,    None,    None,    None,      None,   None],
[ self.p9, self.p10, self.p11, self.p12, self.p13, self.p14, self.p15, self.p16 ],
    [   None,   None,    None,    None,    None,    None,      None,   None],
                        ]
        generated_state = self.chessboard.state
        errormessage = f"generated state not correct \n {generated_state}"
        self.assertEqual(correct_state, generated_state, errormessage)

    def test_pawn_movement_result_state_1(self):
        """
        Testing if moving a pawn correctly effects the state.
        """
        self.p4.move(new_pos=(3, 3))
        self.p5.move(new_pos=(2, 4))
        self.p15.move(new_pos=(4, 6))
        self.p16.move(new_pos=(5, 7))

        correct_state = [
    [   None,   None,    None,    None,    None,    None,      None,   None],
    [ self.p1, self.p2, self.p3,  None,    None, self.p6, self.p7,  self.p8],
    [   None,   None,    None,    None,   self.p5,  None,      None,   None],
    [   None,   None,    None,   self.p4,  None,    None,      None,   None],
    [   None,   None,    None,    None,    None,    None,    self.p15, None],
    [   None,   None,    None,    None,    None,    None,      None,  self.p16],
[ self.p9, self.p10, self.p11, self.p12, self.p13, self.p14,   None,   None],
    [   None,   None,    None,    None,    None,    None,      None,   None],
                        ]
        generated_state = self.chessboard.state
        errormessage = f"generated state not correct \n {generated_state}"
        self.assertEqual(correct_state, generated_state, errormessage)

    def test_pawn_movement_result_state_2(self):
        """
        Testing if moving a pawn taking an opponents pawn (p8 taking p16)
        correctly effects the state.
        """
        self.p4.move(new_pos=(3, 3))
        self.p5.move(new_pos=(2, 4))
        self.p15.move(new_pos=(4, 6))
        self.p16.move(new_pos=(5, 7))

        self.p8.move(new_pos=(3, 7))
        self.p8.move(new_pos=(4, 6)) # p8 taking p15!

        correct_state = [
    [   None,   None,    None,    None,    None,    None,      None,   None],
    [ self.p1, self.p2, self.p3,  None,    None, self.p6, self.p7,     None],
    [   None,   None,    None,    None,   self.p5,  None,      None,   None],
    [   None,   None,    None,   self.p4,  None,    None,      None,   None],
    [   None,   None,    None,    None,    None,    None,    self.p8, None],
    [   None,   None,    None,    None,    None,    None,      None,  self.p16],
[ self.p9, self.p10, self.p11, self.p12, self.p13, self.p14,   None,   None],
    [   None,   None,    None,    None,    None,    None,      None,   None],
                        ]
        generated_state = self.chessboard.state
        errormessage = f"generated state not correct \n {generated_state}"
        self.assertEqual(correct_state, generated_state, errormessage)

    def test_pawn_movement_result_state_illegal_1(self):
        """
        Testing if moving a pawn on field of already occupied field by another
        pawn correctly effects the state.
        """
        self.p4.move(new_pos=(3, 3))
        self.p5.move(new_pos=(2, 4))
        self.p15.move(new_pos=(4, 6))
        self.p16.move(new_pos=(5, 7))

        self.p8.move(new_pos=(3, 7))
        self.p8.move(new_pos=(4, 6))
        self.p7.move(new_pos=(3, 6))
        self.p7.move(new_pos=(4, 6)) # illegal move! already occupied by p8

        correct_state = [
    [   None,   None,    None,    None,    None,    None,      None,   None],
    [ self.p1, self.p2, self.p3,  None,    None, self.p6,      None,   None],
    [   None,   None,    None,    None,   self.p5,  None,      None,   None],
    [   None,   None,    None,   self.p4,  None,    None,    self.p7,  None],
    [   None,   None,    None,    None,    None,    None,    self.p8,  None],
    [   None,   None,    None,    None,    None,    None,      None,  self.p16],
[ self.p9, self.p10, self.p11, self.p12, self.p13, self.p14,   None,   None],
    [   None,   None,    None,    None,    None,    None,      None,   None],
                        ]
        generated_state = self.chessboard.state
        errormessage = f"generated state not correct \n {generated_state}"
        self.assertEqual(correct_state, generated_state, errormessage)

    def test_pawn_movement_result_state_illegal_2(self):
        """
        Testing if moving a pawn off the field correctly effects the state.
        """
        self.p4.move(new_pos=(3, 3))
        self.p5.move(new_pos=(2, 4))
        self.p15.move(new_pos=(4, 6))
        self.p16.move(new_pos=(5, 7))

        self.p8.move(new_pos=(3, 7))
        self.p8.move(new_pos=(4, 6))
        self.p7.move(new_pos=(3, 6))
        self.p7.move(new_pos=(4, 6)) # illegal move! already occupied by p8
        self.p8.move(new_pos=(5, 6))
        self.p8.move(new_pos=(6, 6))
        self.p8.move(new_pos=(7, 6))
        self.p8.move(new_pos=(8, 6)) # illegal move! out of board

        correct_state = [
    [   None,   None,    None,    None,    None,    None,      None,   None],
    [ self.p1, self.p2, self.p3,  None,    None, self.p6,      None,   None],
    [   None,   None,    None,    None,   self.p5,  None,      None,   None],
    [   None,   None,    None,   self.p4,  None,    None,    self.p7,  None],
    [   None,   None,    None,    None,    None,    None,      None,   None],
    [   None,   None,    None,    None,    None,    None,      None,  self.p16],
[ self.p9, self.p10, self.p11, self.p12, self.p13, self.p14,   None,    None],
    [   None,   None,    None,    None,    None,    None,    self.p8,   None],
                        ]
        generated_state = self.chessboard.state
        errormessage = f"generated state not correct \n {generated_state}"
        self.assertEqual(correct_state, generated_state, errormessage)

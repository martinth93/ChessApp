import unittest

from chesski.backend.game.board import ChessBoard
from chesski.backend.game.pieces import Pawn
from chesski.backend.game.move import Move


class TestBoardSimple(unittest.TestCase):

    def test_initialize_state(self):
        # Test if Initializing the state yields empty board
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
        # Test of placing a piece from the chessboard
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
        # Test of removing a piece from the chessboard
        chessboard = ChessBoard()
        p1 = Pawn(position=(1, 3), color="w", chessboard=chessboard)
        # pawn placed on (1, 3)
        chessboard.remove_from_board(p1)
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
        chessboard = ChessBoard()
        p1 = Pawn(position=(1, 3), color="w", chessboard=chessboard)
        # pawn placed on (1, 3)
        correct_piece = p1
        generated_piece = chessboard.return_piece_on_field(piece_pos=(1, 3))
        errormessage = f"generated piece not correct \n {generated_piece}"
        self.assertEqual(correct_piece, generated_piece, errormessage)

class TestBoardKomplexPawn(unittest.TestCase):

    def _check_and_move(self, piece, end_pos):
        move = Move(piece.position, end_pos, self.chessboard)
        if piece.move_is_pseudo_legal(move):
            piece.move(move)

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
        self._check_and_move(self.p4, (3, 3))
        self._check_and_move(self.p5, (2, 4))
        self._check_and_move(self.p15, (4, 6))
        self._check_and_move(self.p16, (5, 7))

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
        self._check_and_move(self.p4, (3, 3))
        self._check_and_move(self.p5, (2, 4))
        self._check_and_move(self.p15, (4, 6))
        self._check_and_move(self.p16, (5, 7))

        self._check_and_move(self.p8, (3, 7))
        self._check_and_move(self.p8, (4, 6)) # p8 taking p15!

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
        self._check_and_move(self.p4, (3, 3))
        self._check_and_move(self.p5, (2, 4))
        self._check_and_move(self.p15, (4, 6))
        self._check_and_move(self.p16, (5, 7))

        self._check_and_move(self.p8, (3, 7))
        self._check_and_move(self.p8, (4, 6))
        self._check_and_move(self.p7, (3, 6))

        self._check_and_move(self.p7, (4, 6)) # illegal move! already occupied by p8

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
        self._check_and_move(self.p4, (3, 3))
        self._check_and_move(self.p5, (2, 4))
        self._check_and_move(self.p15, (4, 6))
        self._check_and_move(self.p16, (5, 7))

        self._check_and_move(self.p8, (3, 7))
        self._check_and_move(self.p8, (4, 6))
        self._check_and_move(self.p7, (3, 6))

        self._check_and_move(self.p7, (4, 6)) # illegal move! already occupied by p8

        self._check_and_move(self.p8, (5, 6))
        self._check_and_move(self.p8, (6, 6))
        self._check_and_move(self.p8, (7, 6))

        self._check_and_move(self.p8, (8, 6)) # illegal move! out of board

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

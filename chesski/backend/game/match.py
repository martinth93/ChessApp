import numpy as np

from chesski.backend.game.board import ChessBoard
from chesski.backend.game.pieces import Pawn, Rook, Knight, Bishop, Queen, King


class Match():
    """
    A class setting up Board and Pieces and Managing Moves and displays during
    a match.
    """

    def __init__(self, chessboard=None, which_players_turn = 'w'):

        self.which_players_turn = which_players_turn # white or black has to move
        self.pieces = {'w': [], 'b': []}

        if chessboard is None:
            self.chessboard = ChessBoard()  # create a new chessboard
            self.initialize_pieces()  # create all necessary pieces



    def initialize_pieces(self):
        """
        Creates Instances of all necessary Chesspieces and places them on
        the right starting spot.
        """

        # (PieceClass, [rows], [columns])
        starting_position=[
        (Pawn,   [1, 6], [0, 1, 2, 3, 4, 5, 6, 7]),
        (Rook,   [0, 7], [0, 7]),
        (Knight, [0, 7], [1, 6]),
        (Bishop, [0, 7], [2, 5]),
        (Queen,  [0, 7], [3]),
        (King,   [0, 7], [4])
        ]

        for (PieceClass, rows, cols) in starting_position:
            for row in rows:
                color = 'w'
                if row > 5:
                    color = 'b'

                for col in cols:
                    new_piece = PieceClass(position=(row, col), color=color,
                                                    chessboard=self.chessboard)
                    self.pieces[color].append(new_piece)


    def translate_from_notation(self, move):
        """
        Translates move form common chess notation into usable form for
        this application.
        Returns which piece where to move.
        """
        letters = "abcdefgh"
        piece_to_move = None
        possible_pieces = 0
        start_col = None
        start_row = None
        end_row = None
        end_col = None
        piece_abbrevation = None

        if move[0].islower():  # Pawn move, eg. e4, c4, hxg6
            start_col = letters.index(move[0])
            end_col = letters.index(move[-2])
            end_row = int(move[-1]) - 1
            piece_abbrevation = "P"




        if move[0].isupper():  # Piece move, eg. Ne4, Kg4, Rfe4, Rxe3, Rh4xg6
            end_col = letters.index(move[-2])
            end_row = int(move[-1]) - 1
            piece_abbrevation = move[0]

            if len(move) == 4:
                if 'x' not in move:    # Piece column has to be specified: Rfe4
                    start_col = letters.index(move[1])
            elif len(move) == 5:
                start_col = letters.index(move[1])
                if 'x' not in move:    # Piece column and row has to be specified: Rf4e4
                    start_row = int(move[2]) - 1
            elif len(move) == 6:  # Piece takes and column and row has to be specified: Rf4xe4
                start_col = letters.index(move[1])
                start_row = int(move[2]) - 1

        # search for piece to move
        for piece in self.pieces[self.which_players_turn]:
            if piece.Abbrevation == piece_abbrevation:
                if start_col != None: # if starting column is specified
                    if piece.position[1] != start_col:
                        continue
                if start_row != None: # if starting row is specified
                    if piece.position[0] != start_row:
                        continue

                if piece.move_is_legal(new_pos=(end_row, end_col)):
                    piece_to_move = piece
                    possible_pieces += 1

        if possible_pieces > 1:
            raise ValueError(f"found {possible_pieces} possibilities, check notation!")
        elif piece_to_move == None:
            raise ValueError(f"found no possibilities, check notation!")
        else:
            return piece_to_move, (end_row, end_col)
            # No Issue found

    def make_a_move(self, player, move_in_notation):
        """
        Function handling the moves given as string in common chess notation.
        """
        if player == self.which_players_turn:
            piece, new_pos = self.translate_from_notation(move_in_notation)
            piece.move(new_pos=new_pos)
            if player == "w":                   # change player turn
                self.which_players_turn = "b"
            else:
                self.which_players_turn = "w"

            print(self.display_board())

        else:
            raise ValueError(f"{self.which_players_turn} has to move!")


    def display_board(self):
        """
        Displays the chessboard with pieces on it as numpy array.

        "O" for empty white field
        "X" for empty black field
        "P-w" for white Pawn
        "P-b" for black Pawn
        "R-w" for white Rook
        "R-b" for black Rook
        "N-w" for white Knight
        "N-b" for black Knight
        "B-w" for white Bishop
        "B-b" for black Bishop
        "Q-w" for white Queen
        "Q-b" for black Queen
        "K-w" for white King
        "K-b" for black King
        """
        full_board = []

        for row in range(8):
            displayed_row = []

            for col in range(8):
                displayed_as = ""
                piece = self.chessboard.state[row][col]  # get piece or None

                if piece == None:
                    if (row + col) % 2 == 0:
                        displayed = " X "
                    else:
                        displayed = " O "
                else:
                    displayed = f"{piece.Abbrevation}-{piece.color}"

                displayed_row.append(displayed)

            full_board.append(displayed_row)

        full_board.reverse()

        return(np.array(full_board))

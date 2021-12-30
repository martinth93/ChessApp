import numpy as np

from chesski.backend.game.board import ChessBoard
from chesski.backend.game.pieces import Pawn, Rook, Knight, Bishop, Queen, King


class Match():
    """A class setting up Board and Pieces and Managing Moves."""

    def __init__(self, chessboard=None, which_players_turn = 'w'):

        self.which_players_turn = which_players_turn # white or black has to move
        self.pieces = {'w': [], 'b': []}
        self.removed_pieces = {'w': [], 'b': []}

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
        Translates move form common chess notation into coordinates.
        Returns coordinate of piece to move and coordinate of field to move to.
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

                if piece.move_is_legal(end_pos=(end_row, end_col)):
                    piece_to_move = piece
                    possible_pieces += 1

        if possible_pieces > 1:
            raise ValueError(f"found {possible_pieces} possibilities, check notation!")
        elif piece_to_move == None:
            raise ValueError(f"found no possibilities, check notation!")
        else:
            return piece_to_move.position, (end_row, end_col)
            # No Issue found

    def make_a_move(self, move, in_notation=False):
        """
        Function handling the moves given as string in common chess notation
        or coordinate-tuple.

        If move allowed: return: True,

        If wrong player made turn, ValueError with further specification is raised.
        """
        start_pos, end_pos = None, None
        need_to_remove_piece = False
        checkmating_player = None
        piece_to_remove = None

        # get coordinates of startfield and endfield
        if in_notation:
            start_pos, end_pos = self.translate_from_notation(move)
        else:
            start_pos = move[0]
            end_pos = move[1]

        # get piece on start_position
        piece = self.chessboard.return_piece_on_field(start_pos)

        player = piece.color
        opponent = self.get_opponent(player)

        # check if right player makes turn
        if player != self.which_players_turn:
            raise ValueError(f"Wrong player: {self.which_players_turn} has to move!")

        # make move if succesfull
        if piece.move_is_legal(end_pos=end_pos):

            # change flag if piece on end_field
            piece_to_remove = self.chessboard.return_piece_on_field(end_pos)
            if piece_to_remove != None:
                self.pieces[opponent].remove(piece_to_remove)
            piece.move(end_pos)

            if self.in_check(player):       # if putting yourself in check
                piece.move(start_pos)               # revert move
                if piece_to_remove:
                    piece_to_remove.move(end_pos)   # put removed piece back
                    self.pieces[opponent].append(piece_to_remove)

            else:
                if piece_to_remove != None:
                    need_to_remove_piece = True
                    self.removed_pieces[opponent].append(piece_to_remove)
                self.change_turns(player)
                # print(self.display_board())

                if self.in_check(opponent):
                    print('Putting other player in check')
                    if self.its_checkmate(opponent):
                        checkmating_player = player
                return True, need_to_remove_piece, checkmating_player
                # move worked, piece that needs to be removed
        return False, None, None

    def change_turns(self, current_player):
        """Function switching player that has to move next."""
        if current_player == "w":
            self.which_players_turn = "b"
        else:
            self.which_players_turn = "w"

    @staticmethod
    def get_opponent(player):
        if player == 'w':
            return 'b'
        else:
            return 'w'

    def get_king_position(self, player):
        for piece in self.pieces[player]:
            if piece.Abbrevation == 'K':
                return piece.position

    def in_check(self, player):
        """Function checking if player is in check. (king can be taken)"""
        opponent = self.get_opponent(player)
        king_pos = self.get_king_position(player)

        print('Checking If Move would put player in check:')
        for opponent_piece in self.pieces[opponent]:
            if opponent_piece.move_is_legal(king_pos):
                print('Checking Move was found!')
                return True

        print('No checking Move was found!')
        return False # if no piece can take king

    def its_checkmate(self, losing_player):
        """Function checking if player is in checkmate. (king cant be saved)"""
        king_pos = self.get_king_position(losing_player)
        winning_player = self.get_opponent(losing_player)

        fields = []

        for row in range(8):
            for col in range(8):
                fields.append((row, col))

        for piece in self.pieces[losing_player]:
            for field in fields:                    # check each possible move
                if piece.move_is_legal(field):
                    start_pos = piece.position
                    piece_to_remove = self.chessboard.return_piece_on_field(field)
                    if piece_to_remove != None:
                        self.pieces[winning_player].remove(piece_to_remove)
                    piece.move(field)

                    if not self.in_check(losing_player):    # if moved out of check
                        piece.move(start_pos)               # revert move
                        if piece_to_remove:
                            piece_to_remove.move(field)   # put removed piece back
                            self.pieces[winning_player].append(piece_to_remove)
                        return False
                    else:
                        piece.move(start_pos)               # revert move
                        if piece_to_remove:
                            piece_to_remove.move(field)   # put removed piece back
                            self.pieces[winning_player].append(piece_to_remove)

        print('##################################################\n' \
              + 'Checkmate!\n' \
              + '##################################################')
        return True

    def display_board(self):
        """
        Displays the chessboard with pieces on it as numpy array in terminal.

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

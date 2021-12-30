from chesski.backend.game.board import ChessBoard
from chesski.backend.game.pieces import Pawn, Rook, Knight, Bishop, Queen, King

from chesski.backend.game.helper_functions import translate_from_notation, display_board

class Match():
    """A class setting up Board and Pieces and Managing Moves."""

    def __init__(self, chessboard=None, which_players_turn = 'w'):

        self.which_players_turn = which_players_turn
        self.pieces = {'w': [], 'b': []}
        self.removed_pieces = {'w': [], 'b': []}

        if chessboard is None:
            self.chessboard = ChessBoard()
            self.initialize_pieces()


    def initialize_pieces(self):
        """Creates Instances of all necessary Chesspieces and places them on
        the right starting spot."""

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

    def make_a_move(self, move, in_notation=False):
        """
        Function handling the moves given as string in common chess notation
        or coordinate-tuple. Returning flags to handle the different outcomes.

        Returns:
        ---------
        move_successful: boolean
            True if move was legal and did not end in putting own king in check.
        remove_piece: boolean
            True if move requires to remove another piece.
        checkmate: boolean
            True if move results in checkmate of the opponent.
        castling: str, {'', 'short', 'long'}
            Equals 'short' or 'long' if the move is one of these _castle moves.
            Empty string otherwise.
        """
        start_pos, end_pos = None, None
        move_successful = False
        remove_piece = False
        checkmate = False
        piece_to_remove = None
        castling = ""

        # get coordinates of startfield and endfield
        if in_notation:
            start_pos, end_pos = translate_from_notation(move)
        else:
            start_pos = move[0]
            end_pos = move[1]

        piece = self.chessboard.return_piece_on_field(start_pos)
        player = piece.color
        opponent = self.get_opponent(player)

        if player != self.which_players_turn:
            raise ValueError(f"Wrong player: {self.which_players_turn} has to move!")

        if piece.move_is_legal(end_pos):
            start_pos, castling, piece_to_remove, remove_piece = self._preprocess_move(piece, end_pos)

            self._move_pieces(piece, start_pos, end_pos, castling, piece_to_remove)

            if self.in_check(player):
                self._move_pieces_back(piece, start_pos, end_pos, castling, piece_to_remove)
            else:
                move_successful = True
                piece.moved_once = True
                self.change_turns(player)
                # display_board()

                if self.in_check(opponent):
                    # print('Putting other player in check')
                    if self.its_checkmate(opponent):
                        checkmate = True

        return move_successful, remove_piece, checkmate, castling

    def change_turns(self, current_player):
        """Function switching player that has to move next."""
        if current_player == "w":
            self.which_players_turn = "b"
        else:
            self.which_players_turn = "w"

    def get_king_position(self, player):
        for piece in self.pieces[player]:
            if piece.type_code == 'K':
                return piece.position

    def in_check(self, player):
        """Function checking if player is in check. (king can be taken)"""
        opponent = self.get_opponent(player)
        king_pos = self.get_king_position(player)

        # print('Checking If Move would put player in check:')
        for opponent_piece in self.pieces[opponent]:
            if opponent_piece.move_is_legal(king_pos):
                # print('Checking Move was found!')
                return True

        # print('No checking Move was found!')
        return False # if no piece can take king

    def its_checkmate(self, losing_player):
        """Function checking if player is in checkmate. (king cant be saved).
        Goes through every possible move of the losing player and checks if
        ther is a move to get out of check."""
        still_in_check = True

        king_pos = self.get_king_position(losing_player)
        winning_player = self.get_opponent(losing_player)

        fields = []

        for row in range(8):
            for col in range(8):
                fields.append((row, col))

        for piece in self.pieces[losing_player]:
            for field in fields:                # check each possible move
                castling = ""
                remove_piece = False
                if piece.move_is_legal(field):
                    start_pos, castling, piece_to_remove, remove_piece = self._preprocess_move(piece, field)
                    self._move_pieces(piece, start_pos, field, castling, piece_to_remove)

                    # change flag if move gets loosing player out of check
                    still_in_check = self.in_check(losing_player)

                    self._move_pieces_back(piece, start_pos, field, castling, piece_to_remove)

                    if not still_in_check:
                        return False

        # no way out of check
        return True

    def _add_to_piece_list(self, piece):
        color = piece.color
        if piece in self.removed_pieces[color]:
            self.removed_pieces[color].remove(piece)
        self.pieces[color].append(piece)

    def _remove_from_piece_list(self, piece):
        color = piece.color
        self.pieces[color].remove(piece)
        self.removed_pieces[color].append(piece)

    def _preprocess_move(self, piece, new_pos):
        """Making the"""
        start_pos = piece.position
        castling = ""
        remove_piece = False
        piece_to_remove = self.chessboard.return_piece_on_field(new_pos)

        if piece_to_remove != None:
            if piece_to_remove.color == piece.color:
                castling = piece.check_for_castle(new_pos)
            else:
                remove_piece = True

        return start_pos, castling, piece_to_remove, remove_piece

    def _move_pieces(self, piece, start_pos, new_pos, castling, piece_to_remove):
        """Moving 'piece' from 'start_pos' to 'new_pos' (or castling)
        and removing piece if it ways taken."""
        if castling:
            self._castle(castling, piece, piece_to_remove)
        else:
            if piece_to_remove:
                self._remove_from_piece_list(piece_to_remove)
            piece.move(new_pos)

    def _castle(self, long_short, king, rook):
        """Make move castle long or castle short."""
        new_king_position = None
        new_rook_position = None
        if long_short == 'short':
            new_king_position = (king.position[0], 6)
            new_rook_position = (rook.position[0], 5)
        elif long_short == 'long':
            new_king_position = (king.position[0], 2)
            new_rook_position = (rook.position[0], 3)
        king.move(new_king_position)
        rook.move(new_rook_position)

    def _move_pieces_back(self, piece, start_pos, new_pos, castling, removed_piece):
        """Reverting moving 'piece' from 'start_pos' to 'new_pos' (or castling)
        and placing eventuelly removed piece back to original position."""
        piece.move(start_pos)
        if removed_piece:
            removed_piece.move(new_pos)
            if not castling:
                self._add_to_piece_list(removed_piece)

    @staticmethod
    def get_opponent(player):
        if player == 'w':
            return 'b'
        else:
            return 'w'

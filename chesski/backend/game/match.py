from chesski.backend.game.board import ChessBoard
from chesski.backend.game.pieces import Pawn, Rook, Knight, Bishop, Queen, King
from chesski.backend.game.move import Move

from chesski.backend.game.helper_functions import (translate_from_notation,
                                        display_board, translate_to_notation)

class Match():
    """A class setting up Board and Pieces and Managing Moves."""

    def __init__(self, chessboard=None, current_player = 'w'):

        self.current_player = current_player
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

    def move_is_legal(self, move):
        """Checking a move for check-related rules by simulating the move and
        reverting it after.
        - checking if putting yourself in check
        """

        start_pos = move.start_pos
        new_pos = move.end_pos
        piece = self.chessboard.return_piece_on_field(move.start_pos)
        player = piece.color
        opponent = self.get_opponent(player)
        checking_yourself = False

        if piece.move_is_pseudo_legal(move):
            # make the move
            if move.castling:
                if self._castle(move, piece) == False:
                    checking_yourself = True
            else:
                if move.taking_piece:
                    self._remove_from_piece_list(move.taking_piece)
                piece.move(move)

            #  if player now in check
            if self.in_check(player):
                checking_yourself = True

            # revert move
            piece.move(move, reverse=True)
            if move.taking_piece:
                move.taking_piece.move(move)
                if not move.castling:
                    self._add_to_piece_list(move.taking_piece)

            if not checking_yourself:
                return True

        return False

    def make_a_move(self, move, as_notation=False, promote_to="Q"):
        """
        Function handling the moves given as string in common chess notation
        or coordinate-tuple. Returning Move instance with all flags set
        to handle the different outcomes.
        """
        # get coordinates of startfield and endfield
        if as_notation:
            move = translate_from_notation(move)

        piece = self.chessboard.return_piece_on_field(move.start_pos)

        if piece.color != self.current_player:
            raise ValueError(f"Wrong player: {self.current_player} has to move!")

        if self.move_is_legal(move):
            # make move
            if move.castling:
                self._castle(move, piece)
            else:
                if move.taking_piece:
                    self._remove_from_piece_list(move.taking_piece)
                piece.move(move)

            piece.moved_once = True
            self.change_turns()


            # setting move's promotion and deliver_check/checkmate flags
            if piece.type_code == 'P' and move.end_pos[0] % 7 == 0:
                piece = self.promote_pawn(piece, promote_to)
                move.promotion = promote_to
            if self.in_check(self.current_player):
                move.delivering_check = True
                if self.its_checkmate(self.current_player):
                    move.delivering_checkmate = True

            display_board(self)
            return True
        return False

    def promote_pawn(self, pawn, promote_to):
        """Removes the pawn from the board and replaces it with specified Piece."""
        promotion_options = {"R": Rook, "N": Knight, "B": Bishop, "Q": Queen}
        promotion_type = promotion_options[promote_to]

        position = pawn.position
        color = pawn.color

        self.pieces[color].remove(pawn)
        new_piece = promotion_type(position, color, self.chessboard)
        self.pieces[color].append(new_piece)

        return new_piece

    def change_turns(self):
        """Function switching player that has to move next."""
        if self.current_player == "w":
            self.current_player = "b"
        else:
            self.current_player = "w"

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
            temp_move = Move(opponent_piece.position, king_pos)
            if opponent_piece.move_is_pseudo_legal(temp_move):
                # print('Checking Move was found!')
                return True

        # print('No checking Move was found!')
        return False # if no piece can take king

    def its_checkmate(self, losing_player):
        """Function checking if player is in checkmate. (king cant be saved).
        Goes through every possible move of the losing player and checks if
        ther is a move to get out of check."""
        king_pos = self.get_king_position(losing_player)
        winning_player = self.get_opponent(losing_player)

        fields = []

        for row in range(8):
            for col in range(8):
                fields.append((row, col))

        for piece in self.pieces[losing_player]:
            for field in fields:                # check each possible move
                temp_move = Move(piece.position, field)
                still_in_check = True
                legal_move = True

                if piece.move_is_pseudo_legal(temp_move):

                    # make the move
                    if temp_move.castling:
                        self._castle(temp_move, piece)
                    else:
                        if temp_move.taking_piece:
                            self._remove_from_piece_list(temp_move.taking_piece)
                        piece.move(temp_move)

                    #  if putting self in check
                    if self.in_check(winning_player):
                        legal_move = False

                    # change flag if move gets loosing player out of check
                    if not self.in_check(losing_player):
                        still_in_check = False

                    # revert move
                    piece.move(temp_move, reverse=True)
                    if temp_move.taking_piece:
                        temp_move.taking_piece.move(temp_move)
                        if not temp_move.castling:
                            self._add_to_piece_list(temp_move.taking_piece)

                    if not still_in_check and legal_move:
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

    def _castle(self, move, king):
        """Make move castle long or castle short."""

        if self.in_check(king.color):
            return False # castling starting in check

        rook = move.taking_piece
        new_king_position = None
        new_rook_position = None
        row = king.position[0]
        move_direction = 0
        if move.castling == 'short':
            new_king_position = (row, 6)
            new_rook_position = (row, 5)
            move_direction = 1
        else: # long
            new_king_position = (row, 2)
            new_rook_position = (row, 3)
            move_direction = -1

        king.move(Move(king.position, (row, king.position[1] + move_direction)))
        if self.in_check(king.color):
            return False # castling through check

        king.move(Move(king.position, new_king_position))
        rook.move(Move(rook.position, new_rook_position))

        return True

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

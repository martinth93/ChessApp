from chesski.backend.game.board import ChessBoard
from chesski.backend.game.pieces import Pawn, Rook, Knight, Bishop, Queen, King
from chesski.backend.game.move import Move

from chesski.backend.game.helper_functions import (translate_from_notation,
                                                   translate_to_notation)

import time

class Match():
    """A class setting up Board and Pieces and Managing Moves."""

    def __init__(self, chessboard=None, current_player = 'w'):

        self.current_player = current_player
        self.pieces = {'w': [], 'b': []}
        self.removed_pieces = {'w': [], 'b': []}
        self.occured_positions = [] # list of (chessboard_state, repetitions)
        self.moves_without_capture = 0

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

    def move_is_legal(self, move, set_checkmate_flag, set_draw_flag, revert):
        """Checking a move for check-related rules by simulating the move and
        reverting it after.
        Setting following flags of given move:

        - delivering_check
        - delivering_checkmate
        - delivering_draw
        """

        piece = self.chessboard.return_piece_on_field(move.start_pos)
        player = piece.color
        opponent = self.get_opponent(player)
        legal_move = True

        if piece.move_is_pseudo_legal(move):

            # make the move
            if move.castling:
                if self._castle(move, piece) == False:
                    legal_move = False
            else:
                if move.taking_piece:
                    self._remove_from_piece_list(move.taking_piece)
                piece.move(move)

            if move.promotion:
                # creating promotion piece and placing it on board (in lists)
                new_piece = self._promote_pawn(piece, move.promotion)

            #  if player now in check
            if self._in_check(player):
                legal_move = False

            if legal_move:

                if self._in_check(opponent):
                    move.delivering_check = True
                    if set_checkmate_flag:
                        if self._its_checkmate(opponent):
                            move.delivering_checkmate = True
                if set_draw_flag:
                    if self._check_for_draw(player, move, revert=revert):
                        move.delivering_draw = True

            if revert or not legal_move:
                if move.promotion:
                    # revert promotion, taking new piece of list and board, pawn back on
                    self.pieces[player].remove(new_piece)
                    self.chessboard.place_on_board(piece)
                    self.pieces[player].append(piece)

                # revert move
                piece.move(move, reverse=True)
                if move.taking_piece:
                    move.taking_piece.move(move)
                    if not move.castling:
                        self._add_to_piece_list(move.taking_piece)
            else:
                piece.moved_once = True

            if legal_move:
                return True

        return False

    def make_a_move(self, move, needing_checkmate_flag=True,
                    needing_draw_flag=True, as_notation=False):
        """
        Function handling the moves given as string in common chess notation
        or as instance of the Move class. Returning True if move is legal and
        setting checkmate, check and draw flag of given move instances.
        """
        # get coordinates of startfield and endfield
        if as_notation:
            move = translate_from_notation(move)

        piece = self.chessboard.return_piece_on_field(move.start_pos)

        if piece.color != self.current_player:
            raise ValueError(f"Wrong player: {self.current_player} has to move!")

        if self.move_is_legal(move, set_checkmate_flag=needing_checkmate_flag,
                                    set_draw_flag=needing_draw_flag, revert=False):
            self.change_turns()
            # self.chessboard.display_board()
            return True
        return False

    def get_move_possibilities(self, player, early_stop=False,
                               set_checkmate_flag=False, set_draw_flag=False):
        """Returning all possible moves of a player in the current state.
        Necessary for engine moves or stalemate checks (early stopping).
        Changing delivering_check flag and optionally also delivering_checkmate
        or delivering_draw flag."""
        move_possibilites = []
        fields = []

        for row in range(8):
            for col in range(8):
                fields.append((row, col))

        for piece in self.pieces[player]:
            for field in fields:
                temp_move = Move(piece.position, field)

                if piece.type_code == 'P' and temp_move.end_pos[0] % 7 == 0:
                    for option in ['Q', 'R', 'N', 'B']:
                        promotion_move = Move(temp_move.start_pos,
                                              temp_move.end_pos,
                                              promotion=option)
                        if self.move_is_legal(promotion_move, set_checkmate_flag,
                                              set_draw_flag, revert=True):
                            move_possibilites.append(promotion_move)

                            if early_stop: # to know if at least one move possible
                                return move_possibilites

                else:

                    if self.move_is_legal(temp_move, set_checkmate_flag,
                                          set_draw_flag, revert=True):

                        move_possibilites.append(temp_move)

                        if early_stop: # to know if at least one move possible
                            return move_possibilites

        return move_possibilites

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

    def _pseudo_move(self, move, piece):
        """Private method for code simplification. Moves the piece (changes
        board state, piece position attribute and piece lists) and removes
        pieces that get taken. Does not check for any rulebreaks, gameover events
        or flags"""
        if move.castling:
            self._castle(move, piece)
        else:
            if move.taking_piece:
                self._remove_from_piece_list(move.taking_piece)
            piece.move(move)

    def _add_to_piece_list(self, piece):
        color = piece.color
        if piece in self.removed_pieces[color]:
            self.removed_pieces[color].remove(piece)
        self.pieces[color].append(piece)

    def _remove_from_piece_list(self, piece):
        color = piece.color
        self.pieces[color].remove(piece)
        self.removed_pieces[color].append(piece)

    def _promote_pawn(self, pawn, promote_to):
        """Removes the pawn from the board and replaces it with specified Piece."""
        promotion_options = {"R": Rook, "N": Knight, "B": Bishop, "Q": Queen}
        promotion_type = promotion_options[promote_to]

        position = pawn.position
        color = pawn.color

        self.pieces[color].remove(pawn)
        new_piece = promotion_type(position, color, self.chessboard)
        self.pieces[color].append(new_piece)

        return new_piece

    def _castle(self, move, king):
        """Make move castle long or castle short."""

        if self._in_check(king.color):
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
        if self._in_check(king.color):
            return False # castling through check

        king.move(Move(king.position, new_king_position))
        rook.move(Move(rook.position, new_rook_position))
        return True

    def _in_check(self, player):
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

    def _its_checkmate(self, losing_player):
        """Function checking if losing player is in checkmate..
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
                    self._pseudo_move(temp_move, piece)

                    # change flag if move gets loosing player out of check
                    if not self._in_check(losing_player):
                        still_in_check = False

                    # revert move
                    piece.move(temp_move, reverse=True)
                    if temp_move.taking_piece:
                        temp_move.taking_piece.move(temp_move)
                        if not temp_move.castling:
                            self._add_to_piece_list(temp_move.taking_piece)

                    if not still_in_check:
                        return False

        # no way out of check
        return True

    def _check_for_draw(self, player, move, revert):
        """Checks if a move of player ends in one of the draw scenarios"""
        if (self._check_no_capture_draw(move, revert) or
            self._check_for_repetition_draw(move, revert) or
            self._check_insufficient_material() or
            self._check_stalemating_opponent(move, player)):
            return True
        else:
            return False

    def _check_no_capture_draw(self, move, revert):
        """Checks if there were more than 50 moves (each color) without capture"""
        if move.taking_piece == None or move.castling:
            if self.moves_without_capture > 98:
                return True
            elif not revert:
                self.moves_without_capture += 1
            return False
        elif not revert:
            if move.taking_piece and not move.castling:
                self.moves_without_capture = 0
        return False

    def _check_for_repetition_draw(self, move, revert):
        """Checks if the current repetition already occured two times before
        (threefold repetition)"""

        current_state = self.chessboard.display_board()
        new_position = True

        if move.taking_piece:
            if not revert:
                self.occured_positions = [[current_state, 1]]
            return False

        for i in range(len(self.occured_positions)):
            if (current_state == self.occured_positions[i][0]).all():
                new_position = False
                if self.occured_positions[i][1] == 2:
                    return True
                else:
                    if not revert:
                        self.occured_positions[i][1] += 1
                    return False

        if new_position and not revert:
            self.occured_positions.append([current_state, 1])
        return False

    def _check_stalemating_opponent(self, move, player):
        """Checking if player put opponent in stalemate with last move, has to be
        checked after setting checkmate flags"""
        if move.delivering_check:
            return False

        opponent = self.get_opponent(player)
        if len(self.get_move_possibilities(opponent, early_stop=True)) == 0:
            return True
        else:
            return False

    def _check_insufficient_material(self):
        """Checking if draw through insufficinet material"""
        if len(self.pieces['w']) < 3 and len(self.pieces['b']) < 3:
            white_insufficient = True
            black_insufficient = True

            for own_piece in self.pieces['w']:
                if own_piece.type_code in ['Q', 'P', 'R']:
                    white_insufficient = False
                    break
            if white_insufficient:
                for opponent_piece in self.pieces['b']:
                    if opponent_piece.type_code in ['Q', 'P', 'R']:
                        black_insufficient = False
                        break

            if white_insufficient and black_insufficient:
                return True
            else:
                return False

    @staticmethod
    def get_opponent(player):
        if player == 'w':
            return 'b'
        else:
            return 'w'

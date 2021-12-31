from chesski.backend.game.match import Match
from chesski.backend.game.move import Move

from chesski.backend.game.helper_functions import translate_to_notation

class MatchController:

    def __init__(self):
        self.match = None
        self.main_layout = None
        self.game_over = True
        self.move_count = 0

    def init_match(self):
        """
        Initializing a match in the backend.
        """
        self.game_over = False
        self.match = Match()
        self.move_count = 0

    def get_piece_type_from_state(self, position):
        """
        Returning the piece type as ui type (e.g. b_R for "black Rook") at
        specified position in state.
        """
        row = position[0]
        col = position[1]
        piece = self.match.chessboard.state[row][col]
        if piece == None:
            return None
        color = piece.color
        code = piece.type_code
        position = piece.position

        type = f'{color}_{code}'

        return type

    def get_material_difference(self):
        """Return material score
        Positive: White player has pieces with more combined value.
        Negative: Black player has pieces with more combined value."""
        score_white = 0
        score_black = 0
        for piece in self.match.pieces['w']:
            score_white += piece.value
        for piece in self.match.pieces['b']:
            score_black += piece.value
        return score_white - score_black

    def move_was_possible(self, last_coordinates, next_coordinates):
        """
        Makes a move on the backend board and informs the main_layout
        regarding necessary changes on the ui-board.
        Also handles if a move was made on the ui-board, that is not
        allowed according to the rules implemented in the backend.
        """
        move = Move(last_coordinates, next_coordinates)
        current_player = self.get_current_player()

        try:
            if self.match.make_a_move(move):
                print('1')
                if move.castling:
                    self.main_layout.remove_piece(next_coordinates, to_stack=False)
                    self.main_layout.remove_piece(last_coordinates, to_stack=False)
                    type_king = f'{current_player}_K'
                    type_rook = f'{current_player}_R'
                    row = last_coordinates[0]
                    if move.castling == 'short':
                        new_king_position = (row, 6)
                        new_rook_position = (row, 5)
                    elif move.castling == 'long':
                        new_king_position = (row, 2)
                        new_rook_position = (row, 3)
                    self.main_layout.add_piece(type_rook, new_rook_position)
                    self.main_layout.add_piece(type_king, new_king_position)
                    print("castled")
                elif move.promotion:
                    if move.taking_piece:
                        self.main_layout.remove_piece(next_coordinates)
                    self.main_layout.remove_piece(last_coordinates, to_stack=False)
                    type = self.get_piece_type_from_state(next_coordinates)
                    self.main_layout.add_piece(type, next_coordinates)
                elif move.taking_piece:
                    self.main_layout.remove_piece(next_coordinates)

                if move.delivering_checkmate:
                    self.main_layout.handle_checkmate(current_player)
                    self.game_over = True

                self.move_count += 1
                move_in_notation = translate_to_notation(self.match, move)
                self.main_layout.update_move_text(move_in_notation,
                                                  self.move_count,
                                                  current_player)
                return True
            else:
                return False
        # handling if wrong player made turn
        except ValueError as e:
            print(e)
            return False

    def get_current_player(self):
        return self.match.current_player

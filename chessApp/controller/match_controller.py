from chessApp.backend.game.match import Match
from chessApp.backend.game.move import Move

from chessApp.backend.game.helper_functions import translate_to_notation

from chessApp.backend.engines.random_engine import RandomEngine
from chessApp.backend.engines.minimax import MiniMaxEngine
from chessApp.backend.engines.material_engine import MaterialEngine

import time
import traceback

class MatchController:

    def __init__(self):
        self.match = None
        self.main_layout = None
        self.game_over = True
        self.move_count = 0
        self.engine_option_1 = RandomEngine()
        self.engine_option_2 = MaterialEngine(checkmate_filter=True,
                                      avoiding_draw=True,
                                      auto_queen=True)
        self.engine_option_3 = MiniMaxEngine(max_depth=2)
        self.engine1 = None
        self.engine2 = None
        self.engine1_color = 'w'

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
        return self.match.evaluate_position()

    def move_was_possible(self, last_coordinates, next_coordinates, promote_choice=None):
        """
        Makes a move on the backend board and informs the main_layout
        regarding necessary changes on the ui-board.
        Also handles if a move was made on the ui-board, that is not
        allowed according to the rules implemented in the backend.
        """
        move = Move(last_coordinates, next_coordinates, self.match.chessboard)
        current_player = self.get_current_player()

        if promote_choice:
            move = Move(last_coordinates, next_coordinates, self.match.chessboard, promote_choice)
        current_player = self.get_current_player()

        try:
            if self.match.make_a_move(move):
                self.handle_move_ui_updates(move, current_player)
                self.main_layout.schedule_engine_move()
                return True
            else:
                return False
        # handling if wrong player made turn
        except ValueError as e:
            print(e)
            return False

    def get_current_player(self):
        return self.match.current_player

    def ask_for_promotion(self, piece_widget, player, move):
        self.main_layout.popup_promotion(piece_widget, player, move)

    def make_engine_move(self):
        current_player = self.get_current_player()

        engine_move = None
        if current_player == self.engine1_color:
            engine_move = self.engine1.get_move(self.match, current_player)
        else:
            engine_move = self.engine2.get_move(self.match, current_player)

        self.match.make_a_move(engine_move)
        self.handle_move_ui_updates(engine_move, current_player, engine=True)

    def handle_move_ui_updates(self, move, current_player, engine=False):
        """Creates all necessary changes in the application view and calls
        Handling-Functions for draws or checkmates"""
        if self.main_layout.get_piece_widget(move.start_pos) == None:
            raise ValueError('couldnt find piece on', move.start_pos)

        if move.castling:
            rook_widget = self.main_layout.get_piece_widget(move.end_pos)
            king_widget = self.main_layout.get_piece_widget(move.start_pos)
            row = move.start_pos[0]
            if move.castling == 'short':
                new_king_position = (row, 6)
                new_rook_position = (row, 5)
            elif move.castling == 'long':
                new_king_position = (row, 2)
                new_rook_position = (row, 3)
            rook_widget.move_to_coordinates(new_rook_position)
            king_widget.move_to_coordinates(new_king_position)
            # print("castled")
        elif move.promotion:
            if move.taking_piece:
                self.main_layout.remove_piece(move.end_pos)

            self.main_layout.remove_piece(move.start_pos, to_stack=False)
            type = self.get_piece_type_from_state(move.end_pos)
            p = self.main_layout.add_piece(type, move.end_pos)

            # print(p.last_coordinates)

            if self.main_layout.get_piece_widget(move.end_pos) == None:
                raise ValueError('couldnt place promotion piece')

        elif move.taking_piece:
            self.main_layout.remove_piece(move.taking_piece.position)

        if not move.castling and not move.promotion:
            piece_widget = self.main_layout.get_piece_widget(move.start_pos)
            piece_widget.move_to_coordinates(move.end_pos)


        self.move_count += 1
        move_in_notation = translate_to_notation(self.match, move)
        self.main_layout.update_move_text(move_in_notation,
                                          self.move_count,
                                          current_player)

        if move.delivering_checkmate:
            self.main_layout.handle_checkmate(current_player)
        elif move.delivering_draw:
            self.main_layout.handle_draw(current_player)

        if self.match.current_player == 'w' and self.main_layout.white_engine:
            self.main_layout.schedule_engine_move()
        elif self.match.current_player == 'b' and self.main_layout.black_engine:
            self.main_layout.schedule_engine_move()

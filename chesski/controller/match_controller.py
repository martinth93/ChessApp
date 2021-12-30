from chesski.backend.game.match import Match

class MatchController:

    def __init__(self):
        self.match = None
        self.main_layout = None
        self.game_over = True

    def init_match(self):
        """
        Initializing a match in the backend.
        """
        self.game_over = False
        self.match = Match()

    def _get_board_state(self):
        """
        get the state of the backend-board.
        """
        return self.match.chessboard.state

    def get_pieces_on_board(self):
        """
        Returning all pieces on the backend-board with piece-type,
        position and color.
        Those have to be displayed on the ui-board.
        """
        pieces = []
        for row in self._get_board_state():
            for piece in row:
                if piece != None:
                    color = piece.color
                    abbrev = piece.Abbrevation
                    position = piece.position
                    pieces.append((color, abbrev, position))
        return pieces

    def move_was_possible(self, last_coordinates, next_coordinates):
        """
        Makes a move on the backend board and informs the main_layout
        regarding necessary changes on the ui-board.
        Also handles if a move was made on the ui-board, that is not
        allowed according to the rules implemented in the backend.
        """
        move = (last_coordinates, next_coordinates)

        try:
            move_worked, piece_removal, checkmating_player, castling = self.match.make_a_move(move)

            if piece_removal:
                self.main_layout.remove_piece(next_coordinates)
            elif castling:
                self.main_layout.remove_piece(next_coordinates)
                self.main_layout.remove_piece(last_coordinates)
                current_player = self.get_current_player()
                opponent = self.match.get_opponent(current_player)
                type_king = f'{opponent}_K'
                type_rook = f'{opponent}_R'
                row = last_coordinates[0]
                if castling == 'short':
                    new_king_position = (row, 6)
                    new_rook_position = (row, 5)
                elif castling == 'long':
                    new_king_position = (row, 2)
                    new_rook_position = (row, 3)
                self.main_layout.display_piece(type_rook, new_rook_position)
                self.main_layout.display_piece(type_king, new_king_position)
                print("castled")

            if checkmating_player:
                self.main_layout.handle_checkmate(checkmating_player)
                self.game_over = True

            return move_worked



        # handling if wrong player made turn
        except ValueError as e:
            # print(e)
            pass

    def get_current_player(self):
        return self.match.which_players_turn

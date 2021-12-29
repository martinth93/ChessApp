from chesski.backend.game.match import Match

class MatchController:

    def __init__(self):
        self.match = None
        self.main_layout = None

    def init_match(self):
        self.match = Match()

    def _get_board_state(self):
        return self.match.chessboard.state

    def get_pieces_on_board(self):
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
        move = (last_coordinates, next_coordinates)
        try:
            move_worked, piece_removal = self.match.make_a_move(move)
            print(move_worked, piece_removal)
            if piece_removal and move_worked:
                self.main_layout.remove_piece(next_coordinates)
            return move_worked

        except Exception as e:
            print(e)

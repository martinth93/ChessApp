class Move():
    def __init__(self, start_pos, end_pos):
        self.start_pos = start_pos
        self.end_pos = end_pos

        # gets set in make_a_move
        self.delivering_check = False
        self.delivering_checkmate = False
        self.promotion = ""

        # gets set in in check_for_castle
        self.castling = ""

        # gets set in in check_taking_piece
        self.taking_piece = None

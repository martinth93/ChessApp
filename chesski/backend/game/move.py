class Move():
    def __init__(self, start_pos, end_pos, chessboard, promotion = ''):
        self.start_pos = start_pos
        self.end_pos = end_pos

        self.chessboard = chessboard

        # gets set in make_a_move
        self.delivering_check = False
        self.delivering_checkmate = False
        self.delivering_draw = False
        self.promotion = promotion

        # gets set in in check_for_castle (piece level)
        self.castling = ""

        # gets set in in check_taking_piece
        self.taking_piece = None
        self.piece = self.chessboard.return_piece_on_field(self.start_pos)

        self.en_passant = False

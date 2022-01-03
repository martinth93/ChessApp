import random
import time

class MaterialEngine():
    def __init__(self, checkmate_filter=False, avoiding_draw=False, auto_queen=False):
        self.checkmate_filter = checkmate_filter
        self.avoiding_draw = avoiding_draw

        self.need_checkmate_flag = checkmate_filter
        self.need_draw_flag = avoiding_draw
        self.auto_queen = auto_queen

        # if not set flags before move
        self.move_test_checkmate = checkmate_filter==False
        self.move_test_draw = avoiding_draw==False

    def _get_move_possibilities(self, match, current_player):
        possibilities = match.get_move_possibilities(current_player,
                                            set_checkmate_flag=self.need_checkmate_flag,
                                            set_draw_flag=self.need_draw_flag)
        return possibilities

    def get_move(self, match, current_player):
        """Returning random move out of those that are possible."""
        best_moves = []
        biggest_value = 0

        possible_moves = self._get_move_possibilities(match, current_player)

        for move in possible_moves:
            value = 0

            # Checkmate filter
            if self.checkmate_filter:
                if move.delivering_checkmate:
                    best_moves = []
                    best_moves.append(move)
                    break

            # avoiding draw
            if self.avoiding_draw:
                if move.delivering_draw:
                    continue

            # calculate value
            if move.taking_piece and not move.castling:
                value += move.taking_piece.value

            if self.auto_queen:
                if move.promotion == 'Q':
                    value += 8

            # compare to best moves
            if value > biggest_value:
                best_moves = []
                best_moves.append(move)
                biggest_value = value
                continue
            elif value == biggest_value:
                best_moves.append(move)
                continue

        if self.avoiding_draw and len(best_moves) == 0:
            best_moves = possible_moves
            #print('forced draw')

        best_move = random.choice(best_moves)
        #print(best_move.start_pos, best_move.end_pos, best_move.delivering_draw)
        return best_move

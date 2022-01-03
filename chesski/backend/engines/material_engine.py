import random

class MaterialEngine():
    def __init__(self, checkmate_filter=False, avoiding_draw=False):
        self.checkmate_filter = checkmate_filter
        self.avoiding_draw = avoiding_draw

        if checkmate_filter:
            self.need_checkmate_flag = True
        else:
            self.need_checkmate_flag = False

        if avoiding_draw:
            self.need_draw_flags = True
        else:
            self.need_draw_flags = False

    def _get_move_possibilities(self, match, current_player):
        return match.get_move_possibilities(current_player,
                                            set_checkmate_flag=self.need_checkmate_flag,
                                            set_draw_flags=self.need_draw_flags)

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
            if move.taking_piece:
                value += move.taking_piece.value

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

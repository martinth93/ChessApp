import random

class MaterialEngine():
    def __init__(self, checkmate_filter=False, check_value=0):
        self.checkmate_filter = checkmate_filter
        self.check_value = check_value

    def get_move(self, state, possible_moves):
        """Returning random move out of those that are possible."""
        best_moves = []
        biggest_value = 0

        for move in possible_moves:
            value = 0

            # Checkmate filter
            if self.checkmate_filter:
                if move.delivering_checkmate:
                    best_moves = []
                    best_moves.append(move)
                    break

            # calculate value
            if move.delivering_check:
                value += self.check_value # bad idea
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

        return random.choice(best_moves)

import random
import time

random.seed(3)

class RandomEngine():
    def __init__(self):
        self.need_checkmate_flag = False
        self.need_draw_flag = False

        # if not set flags before move
        self.move_test_checkmate = True
        self.move_test_draw = True

    def _get_move_possibilities(self, match, current_player):
        possibilities = match.get_move_possibilities(current_player,
                                            set_checkmate_flag=self.need_checkmate_flag,
                                            set_draw_flag=self.need_draw_flag)
        return possibilities

    def get_move(self, match, current_player):
        """Returning random move out of those that are possible."""
        possible_moves = self._get_move_possibilities(match, current_player)
        #print(possible_moves)
        return random.choice(possible_moves)

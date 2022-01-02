import random

class RandomEngine():
    def __init__(self):
        pass

    def get_move(self, state, possible_moves):
        """Returning random move out of those that are possible."""
        return random.choice(possible_moves)

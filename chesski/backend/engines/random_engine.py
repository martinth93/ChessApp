import random

class RandomEngine():
    def __init__(self):
        pass

    def get_move(state, possible_moves):
        """Returning next engine move

        Arguments:
            state: state of chessboard in 8x8


        """
        if state == None:
        return random.choice(possible_moves)

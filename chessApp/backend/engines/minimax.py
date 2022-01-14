import random
import time
import copy

from chessApp.backend.game.match import Match
from chessApp.backend.game.move import Move
from math import inf

random.seed(3)

class MiniMaxEngine():
    def __init__(self, max_depth=2):
        # if not set flags before move
        self.move_test_checkmate = True
        self.move_test_draw = True
        self.max_depth = max_depth
        self.checked_combinations = 0

    def _get_move_possibilities(self, match, current_player):
        possibilities = match.get_move_possibilities(current_player)
        random.shuffle(possibilities)
        return possibilities

    def get_move(self, match, current_player):
        """Returning best move out of those that are possible according to
        a minimax algorithm."""
        #print(possible_moves)
        start_time = time.time()
        self.checked_combinations = 0
        move = self._minimax(match, self.max_depth)[1]
        print(f"calculated {self.checked_combinations} moves in {time.time()-start_time:.3f} seconds")
        return move

    def _minimax(self, match, depth, alpha=-inf, beta=inf):
        # if max depth reached
        if depth == 0:
            return match.evaluate_position(), None

        possible_moves = self._get_move_possibilities(match, match.current_player)
        if len(possible_moves) == 0:
            return 0, None
        bestMove = None

        if match.current_player == 'w':
            maxVal = -inf

            for i, move in enumerate(possible_moves):

                match.make_a_move(move, needing_draw_flag=False)
                match.current_player = 'b'
                # print(move.start_pos, move.end_pos)
                # print(match.chessboard.display_board())
                value = -inf

                if move.delivering_checkmate:
                    # reached leaf node through checkmate
                    value = 100
                elif move.delivering_draw:
                    # reached leaf node through draw
                    value = 0
                else:
                    value = self._minimax(match, depth-1, alpha, beta)[0]

                if value > maxVal:
                    maxVal = value
                    if depth == self.max_depth:
                        bestMove = move
                    else:
                        bestMove = copy.deepcopy(move)

                match.revert_move(move)
                match.current_player = 'w'

                alpha = max(alpha, maxVal)
                if beta <= alpha:
                    break

                # print(f'Evaluation of branch {i} at depth {depth}: {value}')
                # print(f'Best outcome vor White: {maxVal} \n')
                self.checked_combinations += 1
            return maxVal, bestMove

        else:
            minVal = inf

            for i, move in enumerate(possible_moves):

                match.make_a_move(move, needing_draw_flag=False)
                match.current_player = 'w'
                # print(move.start_pos, move.end_pos)
                # print(match.chessboard.display_board())
                value = inf

                if move.delivering_checkmate:
                    # reached leaf node through checkmate
                    value = -100
                elif move.delivering_draw:
                    # reached leaf node through draw
                    value = 0
                else:
                    value = self._minimax(match, depth-1, alpha, beta)[0]

                if value < minVal:
                    minVal = min(minVal, value)
                    if depth == self.max_depth:
                        bestMove = move
                    else:
                        bestMove = copy.deepcopy(move)

                match.revert_move(move)
                match.current_player = 'b'

                beta = min(beta, minVal)
                if beta <= alpha:
                    break

                # print(f'Evaluation of branch {i} at depth {depth}: {value}')
                # print(f'Best outcome for black: {minVal} \n')
                self.checked_combinations += 1

            return minVal, bestMove

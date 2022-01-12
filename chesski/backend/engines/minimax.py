import random
import time
import copy

from chesski.backend.game.match import Match
from chesski.backend.game.move import Move
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
        bestMove = None

        if match.current_player == 'w':
            maxVal = -inf

            for i, move in enumerate(possible_moves):
                match_copy = copy.deepcopy(match)
                move_copy = Move(start_pos=move.start_pos, end_pos=move.end_pos, chessboard=match_copy.chessboard)

                match_copy.make_a_move(move_copy)
                # print(move_copy.start_pos, move_copy.end_pos)
                # print(match_copy.chessboard.display_board())
                value = -inf

                if move_copy.delivering_checkmate:
                    # reached leaf node through checkmate
                    value = 100
                elif move_copy.delivering_draw:
                    # reached leaf node through draw
                    value = 0
                else:
                    value = self._minimax(match_copy, depth-1, alpha, beta)[0]

                if value > maxVal:
                    maxVal = value
                    if depth == self.max_depth:
                        bestMove = move
                    else:
                        bestMove = move_copy

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
                match_copy = copy.deepcopy(match)
                move_copy = Move(start_pos=move.start_pos, end_pos=move.end_pos, chessboard=match_copy.chessboard)

                match_copy.make_a_move(move_copy)
                # print(move_copy.start_pos, move_copy.end_pos)
                # print(match_copy.chessboard.display_board())
                value = inf

                if move_copy.delivering_checkmate:
                    # reached leaf node through checkmate
                    value = -100
                elif move_copy.delivering_draw:
                    # reached leaf node through draw
                    value = 0
                else:
                    value = self._minimax(match_copy, depth-1, alpha, beta)[0]

                if value < minVal:
                    minVal = min(minVal, value)
                    if depth == self.max_depth:
                        bestMove = move
                    else:
                        bestMove = move_copy

                beta = min(beta, minVal)
                if beta <= alpha:
                    break

                # print(f'Evaluation of branch {i} at depth {depth}: {value}')
                # print(f'Best outcome for black: {minVal} \n')
                self.checked_combinations += 1

            return minVal, bestMove

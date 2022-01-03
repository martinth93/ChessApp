from chesski.backend.game.match import Match
from chesski.backend.engines.random_engine import RandomEngine
from chesski.backend.engines.material_engine import MaterialEngine

import time

engine1 = MaterialEngine(checkmate_filter=True, avoiding_draw=False)
engine2 = RandomEngine()

engine1_won = 0
engine2_won = 0
draw = 0
move_sum = 0
engine1_color = 'w'

start_time = time.time()


print('Start Testing: \n --------------------------------------------')
for i in range(10000):
    match = Match()
    game_over = False
    move_counter = 0
    no_capture = 0
    while not game_over:
        move_counter += 1
        move = None
        current_player = match.current_player

        if current_player == engine1_color:
            move = engine1.get_move(match, current_player)
        else:
            move = engine2.get_move(match, current_player)
        match.make_a_move(move)
        #print(match.chessboard.display_board())
        # print(move_counter, match.moves_without_capture)
        if move.delivering_checkmate:
            # print('Checkmate by ', current_player)
            if current_player == engine1_color:
                engine1_won += 1
            else:
                engine2_won += 1
            game_over = True
        elif move.delivering_draw:
            # print('Draw by ', current_player)
            draw += 1
            game_over = True

    move_sum += move_counter
    if (i+1) % 25 == 0:
        duration = int(time.time() - start_time)
        minutes = duration // 60
        seconds = duration % 60
        print(f"Games: {i+1} --- {engine1_won} / {draw} / {engine2_won} --- avg: {move_sum//(i+1)} Moves" + \
              f" --- Duration: {minutes}min {seconds}s")

    if i == 500:
        print('###########Switching Colors#############')
        engine_1_color = 'b'

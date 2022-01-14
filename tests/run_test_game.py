from chesski.backend.game.match import Match
from chesski.backend.game.move import Move

def print_state(match):
    print(m.chessboard.display_board())
    print('--------------------White Pieces:-------------------------')
    for piece in match.pieces['w']:
        print(f'{piece.color} {piece.type_code} at {piece.position}', piece==match.chessboard.state[piece.position[0]][piece.position[1]])
    print('--------------------Black Pieces:-------------------------')
    for piece in match.pieces['b']:
        print(f'{piece.color} {piece.type_code} at {piece.position}', piece==match.chessboard.state[piece.position[0]][piece.position[1]])
    print('----------------Removed white Pieces:-------------------------')
    for piece in match.removed_pieces['w']:
        print(f'{piece.color} {piece.type_code} at {piece.position}', piece==match.chessboard.state[piece.position[0]][piece.position[1]])
    print('----------------Removed black Pieces:-------------------------')
    for piece in match.removed_pieces['b']:
        print(f'{piece.color} {piece.type_code} at {piece.position}', piece==match.chessboard.state[piece.position[0]][piece.position[1]])


def print_possibilities(match):
    print('----------------Possible moves:-------------------------')
    for possible_move in match.get_move_possibilities(match.current_player, set_checkmate_flag=True, set_draw_flag=True):
        tp = possible_move.taking_piece
        print(possible_move.start_pos, possible_move.end_pos, tp)

m = Match()

print_state(m)

moves = [((1, 2), (3, 2)),
         ((7, 1), (5, 2)),
         ((1, 0), (2, 0)),
         ((5, 2), (3, 1)),
         ((2, 0), (3, 1)),
         ((6, 4), (5, 4)),
         ((3, 1), (4, 1)),
         ((6, 0), (4, 0)),
         ((4, 1), (5, 0)),
         ((7, 3), (4, 6)),
         ((5, 0), (6, 1)),
         ((4, 6), (1, 6)),
         ((6, 1), (7, 0), 'R'),
         ((7, 6), (5, 5)),
         ((7, 0), (7, 1)),
         ]

for i in range(len(moves)):
    print( f"############# Next Move: {moves[i][0]} -> {moves[i][1]} ##################")
    move = Move(moves[i][0], moves[i][1], m.chessboard)
    if len(moves[i]) > 2:
        move.promotion = moves[i][2]
    print(move.piece.color)
    # print_possibilities(m)
    # print_state(m)
    m.make_a_move(move, needing_checkmate_flag=False,
                            needing_draw_flag=False)
    print_state(m)


# print_possibilities(m)
# print_state(m)

import numpy as np

def translate_from_notation(match, move):
    """Translates move form common chess notation into coordinates.
    Returns tuple of coordinate of starting field and field to move to."""
    letters = "abcdefgh"
    piece_to_move = None
    possible_pieces = 0
    start_col = None
    start_row = None
    end_row = None
    end_col = None
    piece_type_code = None

    if move[0].islower():  # Pawn move, eg. e4, c4, hxg6
        start_col = letters.index(move[0])
        end_col = letters.index(move[-2])
        end_row = int(move[-1]) - 1
        piece_type_code = "P"

    if move[0].isupper():  # Piece move, eg. Ne4, Kg4, Rfe4, Rxe3, Rh4xg6
        end_col = letters.index(move[-2])
        end_row = int(move[-1]) - 1
        piece_type_code = move[0]

        if len(move) == 4:
            if 'x' not in move:    # Piece column has to be specified: Rfe4
                start_col = letters.index(move[1])
        elif len(move) == 5:
            start_col = letters.index(move[1])
            if 'x' not in move:    # Piece column and row has to be specified: Rf4e4
                start_row = int(move[2]) - 1
        elif len(move) == 6:  # Piece takes and column and row has to be specified: Rf4xe4
            start_col = letters.index(move[1])
            start_row = int(move[2]) - 1

    # search for piece to move
    for piece in match.pieces[match.which_players_turn]:
        if piece.type_code == piece_type_code:
            if start_col != None: # if starting column is specified
                if piece.position[1] != start_col:
                    continue
            if start_row != None: # if starting row is specified
                if piece.position[0] != start_row:
                    continue

            if piece.move_is_legal(end_pos=(end_row, end_col)):
                piece_to_move = piece
                possible_pieces += 1

    if possible_pieces > 1:
        raise ValueError(f"found {possible_pieces} possibilities, check notation!")
    elif piece_to_move == None:
        raise ValueError(f"found no possibilities, check notation!")
    else:
        return piece_to_move.position, (end_row, end_col)
        # No Issue found



def display_board(match):
    """
    Displays the chessboard with pieces on it as numpy array in terminal.

    "O" for empty white field
    "X" for empty black field
    "P-w" for white Pawn
    "P-b" for black Pawn
    "R-w" for white Rook
    "R-b" for black Rook
    "N-w" for white Knight
    "N-b" for black Knight
    "B-w" for white Bishop
    "B-b" for black Bishop
    "Q-w" for white Queen
    "Q-b" for black Queen
    "K-w" for white King
    "K-b" for black King
    """
    full_board = []

    for row in range(8):
        displayed_row = []

        for col in range(8):
            displayed_as = ""
            piece = match.chessboard.state[row][col]  # get piece or None

            if piece == None:
                if (row + col) % 2 == 0:
                    displayed = " X "
                else:
                    displayed = " O "
            else:
                displayed = f"{piece.type_code}-{piece.color}"
            displayed_row.append(displayed)
        full_board.append(displayed_row)
    full_board.reverse()

    print(np.array(full_board))

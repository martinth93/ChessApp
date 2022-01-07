import numpy as np
from chesski.backend.game.move import Move

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
    for piece in match.pieces[match.current_player]:
        if piece.type_code == piece_type_code:
            if start_col != None: # if starting column is specified
                if piece.position[1] != start_col:
                    continue
            if start_row != None: # if starting row is specified
                if piece.position[0] != start_row:
                    continue

            temp_move = Move(piece.position, (end_row, end_col))
            if match.move_is_legal(temp_move, set_checkmate_flag=False,
                                   set_draw_flag=False, revert=True):
                piece_to_move = piece
                possible_pieces += 1

    if possible_pieces > 1:
        raise ValueError(f"found {possible_pieces} possibilities, check notation!")
    elif piece_to_move == None:
        raise ValueError(f"found no possibilities, check notation!")
    else:
        return (piece_to_move.position, (end_row, end_col))
        # No Issue found


def translate_to_notation(match, move):
    """Translates move to notation with the help of specified flags inside the
    move class. Therefore can onlcy be called after making a move, since thats
    when some flags are set."""

    notation = ""
    letters = 'abcdefgh'

    if move.castling:  # only possible when castling
        if move.castling == 'short':
            return 'O-O'
        else:
            return 'O-O-O'

    piece = move.piece
    color = piece.color

    type_code = piece.type_code
    if type_code != 'P' and not move.promotion:
        notation += type_code

    if move.promotion:
        notation += letters[move.start_pos[1]]

    # revert move and check if other piece could have moved there
    piece.move(move, reverse=True)
    if move.taking_piece:
        move.taking_piece.move(move)
        match._add_to_piece_list(move.taking_piece)

    for other_piece in match.pieces[color]:
        if other_piece == piece:
            continue
        temp_move = Move(other_piece.position, move.end_pos, match.chessboard)
        if other_piece.type_code == type_code and match.move_is_legal(temp_move,
                    set_checkmate_flag=False, set_draw_flag=False, revert=True):
            notation += letters[move.start_pos[1]]
            if other_piece.position[1] == piece.position[1]:
                notation += str(move.start_pos[0] + 1)

    # make move again
    if move.taking_piece:
        match._remove_from_piece_list(move.taking_piece)
    piece.move(move)

    if move.taking_piece:
        if type_code == 'P' and len(notation)==0:
            notation += letters[move.start_pos[1]]
        notation += 'x'

    notation += letters[move.end_pos[1]]
    notation += str(move.end_pos[0]+1)

    if move.promotion:
        notation += move.promotion

    if move.delivering_checkmate:
        notation += '#'
    elif move.delivering_check:
        notation += '+'

    return notation

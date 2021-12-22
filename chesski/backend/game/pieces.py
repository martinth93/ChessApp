class Piece():
    """
    A parent class of all chesspieces.

    ...

    Parameters:
    ----------
    position: (int:col, int:row)
        Position of the chess Piece on the board.
    color: str
        Player ("w"/"b") which is in control of the chesspiece.

    Methods:
    ---------
    get_position:
        Returns the current position of the chess piece.
    is_white:
        Returns True if Piece belongs to white player.
    """

class GameManager():
    """
    A class handling all gameobjects and mechanics.

    ...

    Parameters:
    -----------
    chessboard: ChessBoard
        Chessboard that is used to play.
    orientation: str
        Player black/white that should be on the bottom of the ChessBoard
    pieces: list(Pieces)
        List of pieces that are on the chessboard.
    layout: numpy.array (shape=(n, m))
        2D-Array, every entry represents the state of a single square on the
        chessboard. If it is occupyied by a piece it corresponds to the id of
        this piece, or 0 if there is no piece on it.

    Methods:
    -----------

    """

    def __init__(self, , orientation='w'
                     , pieces="all", state="initial"):s

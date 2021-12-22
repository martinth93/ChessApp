class ChessBoard():
    """
    A class to represent a chessboard.

    ...

    Attributes:
    -----------
    size: tuple (int:n, int:m)
        Grid-size of the chessboard (height n, width m)

    Methods:
    ----------
    get_layout:
        Returning a list with the color of each square on the chessboard.
    __str__:
        Displaying the chessboard.


    """

    def __init__(self, size=(8, 8)):
        """
        Constructs a chessboard with all necessary information to display it.

        Parameters:
        ------------
        size: tuple (int:n, int:m)
            Grid-size of the chessboard (height n, width m).
            Only accepting even numbers.

        """

        if size[0] % 2 == 0 and size[1] % 2 == 0:
            self.size = size
        else:
            raise Exception("Invalid Size of Chessboard."
                            "Please choose even numbers")

    def get_layout(self):
        """
        Constructs a list for the colors of all grid-squares of the chessboard.

        Parameters:
        ----------
        None

        Returns:
        ---------
        The layout of the chessboard as list of rows, which are lists of
        strings with "w" for white and "b" for black.

        """

        layout = []

        while len(layout) < self.size[0]: # while chessboard not high enough
            row1 = ["b", "w", "b"]

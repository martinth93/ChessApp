from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class BoardGrid(GridLayout):
    fields = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.board_orientation = 'w'
        self.init_board()

    def init_board(self):
        """
        Creating a 8x8 grid of boxlayouts, the size of the displayed
        chessboard graphic.
        Dropping a piece inside one of the grid-fields, snaps the piece
        to the middle of the field.
        """
        for row in range(7 ,-1, -1): # row 0 at bottom
            row_fields = []
            for col in range(8):
                b = BoxLayout()
                # # displaying grid
                # coordinate_text = f"({row}, {col})"
                # but = Button(text=coordinate_text)
                # but.opacity = 0.3
                # b.add_widget(but)
                row_fields.append(b)
                self.add_widget(b)
            self.fields.insert(0, row_fields) # first row at index [0]

    def get_field(self, coordinates):
        """Returning the ui correspoinding to given coordinates"""
        row, col = 0, 0
        if self.board_orientation == 'w':
            row = coordinates[0]
            col = coordinates[1]
        else:
            row = 7 - coordinates[0]
            col = 7 - coordinates[1]
        field = self.fields[row][col]
        return field

    def rotate_boardgrid(self):
        if self.board_orientation == 'w':
            self.board_orientation = 'b'
            # print('rotate')
        else:
            self.board_orientation = 'w'
        return self.board_orientation

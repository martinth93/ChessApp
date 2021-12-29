from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class BoardGrid(GridLayout):
    fields = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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

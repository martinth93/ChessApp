from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.metrics import dp
from kivy.uix.image import Image

class GameLayout(RelativeLayout):

    board_size = ObjectProperty((100, 100)) # binded to the size of the board grid
    board_padding = NumericProperty(0)      # for boards with outside frame
    board_spacing = dp(3)                   # not binded because its fixed
    graphics_path = StringProperty('')

    def on_size(self, *args):
        # adjusting board grid to image of board
        new_size = min(self.size)
        self.board_size = (new_size, new_size)
        # adjusting padding to new size
        self.board_padding = self.board_size[0] * 0.03 + self.board_spacing

    def display_from_state(self):
        for row in range(1):
            for col in range(1):
                #if state[row][col] != None:
                gui_piece = ChessPiece(
                    image_path=self.graphics_path + '/chessboard_and_pieces/white_pawn.png',
                    coordinates=(row, col)
                    )
                self.add_widget(gui_piece)

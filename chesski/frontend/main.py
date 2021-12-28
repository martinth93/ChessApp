import kivy

from kivy.app import App

from kivy.metrics import dp
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout


class ChessGame(BoxLayout):
    pass


class BoardLayout(RelativeLayout):
    board_size = ObjectProperty((100, 100)) # binded to the size of the board grid
    board_padding = NumericProperty(0)      # for boards with outside frame
    board_spacing = dp(3)                   # not binded because its fixed

    def on_size(self, *args):
        # adjusting board grid to image of board that has a fixed
        # width/height ratio of 1 (its a square) and is always in center
        if self.width < self.height:
            self.board_size = (self.width, self.width)
        else:
            self.board_size = (self.height, self.height)
        # adjusting padding to new size
        self.board_padding = self.board_size[0] * 0.03 + self.board_spacing


class BoardWidget(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_board()

    def init_board(self):
        self.cols = 8
        for i in range(64):
            b = Button(text='A')
            b.opacity = .1
            self.add_widget(b)


class ChessApp(App):
    pass

if __name__ == "__main__":
    ChessApp().run()

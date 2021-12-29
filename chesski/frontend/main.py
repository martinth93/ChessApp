import kivy

from kivy.app import App

# importing .py file of UI Elements
from mainlayout import MainLayout
from boardgrid import BoardGrid
from chesspiece import ChessPiece
from gamelayout import GameLayout

from kivy.config import Config
Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '700')

# loading .kv file of UI Elements
from kivy.lang import Builder
Builder.load_file('mainlayout.kv')
Builder.load_file('gamelayout.kv')
Builder.load_file('boardgrid.kv')

class ChessApp(App):
    def build(self):
        return MainLayout()

ChessApp().run()

import kivy
from kivy.app import App

# importing .py files of UI Elements
from chessApp.frontend.chesspiece import ChessPiece
from chessApp.frontend.mainlayout import MainLayout
from chessApp.frontend.boardgrid import BoardGrid
from chessApp.frontend.gamelayout import GameLayout
from chessApp.frontend.buttons import IconButton

# setting default window size of application
from kivy.config import Config
Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '700')

# loading .kv file of UI Elements
from kivy.lang import Builder
Builder.load_file('chessApp/frontend/mainlayout.kv')
Builder.load_file('chessApp/frontend/gamelayout.kv')
Builder.load_file('chessApp/frontend/boardgrid.kv')
Builder.load_file('chessApp/frontend/chesspiece.kv')
Builder.load_file('chessApp/frontend/playerdisplay.kv')

# setting path to graphics
# graphics of board and pieces have to be in a folder called chessboard_and_pieces
# boardname: chessboard.png
# piece_names:  black Knight = b_N.png
#               black Rook = b_R.png
#               white Pawn = w_P.png ...
# for example: black king at 'graphics/chessboard_and_pieces/b_K.png'
graphics_path = "graphics"

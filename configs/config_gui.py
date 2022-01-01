import kivy
from kivy.app import App

# importing .py files of UI Elements
from chesski.frontend.chesspiece import ChessPiece
from chesski.frontend.mainlayout import MainLayout
from chesski.frontend.boardgrid import BoardGrid
from chesski.frontend.gamelayout import GameLayout
from chesski.frontend.buttons import IconButton

# setting default window size of application
from kivy.config import Config
Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '700')

# loading .kv file of UI Elements
from kivy.lang import Builder
Builder.load_file('chesski/frontend/mainlayout.kv')
Builder.load_file('chesski/frontend/gamelayout.kv')
Builder.load_file('chesski/frontend/boardgrid.kv')
Builder.load_file('chesski/frontend/chesspiece.kv')
Builder.load_file('chesski/frontend/playerdisplay.kv')

# setting path to graphics
# graphics of board and pieces have to be in a folder called chessboard_and_pieces
# boardname: chessboard.png
# piece_names:  black Knight = b_N.png
#               black Rook = b_R.png
#               white Pawn = w_P.png ...
# for example: black king at 'graphics/chessboard_and_pieces/b_K.png'
graphics_path = "graphics"

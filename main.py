from configs.config_gui import *
from chessApp.controller.match_controller import MatchController

class ChessApp(App):
    def build(self):
        match_controller = MatchController()
        main = MainLayout(match_controller=match_controller)
        main.graphics_path = graphics_path
        return main

ChessApp().run()

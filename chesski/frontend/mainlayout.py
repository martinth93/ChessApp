from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

from chesski.frontend.chesspiece import ChessPiece

class MainLayout(BoxLayout):
    start_reset_button_text = StringProperty("Start")
    graphics_path = StringProperty('')

    piece_widgets = []

    def __init__(self, match_controller, **kwargs):
        super().__init__(**kwargs)
        self.match_controller = match_controller
        self.match_controller.main_layout = self


    def start_game(self):
        """
        Button Function to start or reset the game.
        """
        # remove all remaining gui-pieces
        if self.piece_widgets:
            self.ids.game_box.clear_widgets(self.piece_widgets)
            self.piece_widgets = []

        # notify the match controller to start backend-match
        self.match_controller.init_match()

        # setup pieces
        for color, abbrevation, position \
        in self.match_controller.get_pieces_on_board():
            type = f'{color}_{abbrevation}'
            self.display_piece(type, position)

        # change start/reset button text
        self.start_reset_button_text = 'Reset'

    def display_piece(self, type, position):
        """
        Instantiates the Chesspiece UI-Element and add id as
        child-widget of the game-box.
        """
        gui_piece = ChessPiece(
            board=self.ids.board_grid,
            type=type,
            coordinates=position,
            graphics_path=self.graphics_path,
            match_controller=self.match_controller
            )
        self.ids.game_box.add_widget(gui_piece)
        self.piece_widgets.append(gui_piece)


    def remove_piece(self, coordinates):
        """
        Removes a piece on a given coordiante.
        """
        # print('removing piece')
        for i in range(len(self.piece_widgets)):
            # print('checking piece ', i)
            piece = self.piece_widgets[i]
            if piece.last_coordinates == coordinates:
                piece_to_remove = self.piece_widgets.pop(i)
                self.ids.game_box.remove_widget(piece_to_remove)
                print('piece removed')
                return
        raise ValueError('Piece to remove couldnt be found.')

    def handle_checkmate(self, checkmating_player):
        for piece_widget in self.piece_widgets:
            piece_widget.disable_drag()
        print(f"{checkmating_player} won.")

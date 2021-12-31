from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.uix.image import Image

from chesski.frontend.chesspiece import ChessPiece

class MainLayout(BoxLayout):
    start_reset_button_text = StringProperty("Start")
    graphics_path = StringProperty('')
    white_material_text = StringProperty('')
    black_material_text = StringProperty('')
    move_notations_text = StringProperty('')

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
        for row in range(8):
            for col in range(8):
                position = (row, col)
                type = self.match_controller.get_piece_type_from_state(position)
                if type != None:
                    self.add_piece(type, position)

        # change start/reset button text
        self.start_reset_button_text = 'Reset'

    def add_piece(self, type, position):
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
        self.update_material_text()


    def remove_piece(self, coordinates, to_stack=True):
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
                self.update_material_text()
                if to_stack:
                    image_path = piece_to_remove.source
                    new_image = Image(source=image_path, size_hint=(.05, 1))
                    if image_path[-7] == 'w':
                        self.ids.player_display.ids.black_stack.add_widget(new_image)
                    else:
                        self.ids.player_display.ids.white_stack.add_widget(new_image)
                return
        raise ValueError('Piece to remove couldnt be found.')

    def handle_checkmate(self, checkmating_player):
        for piece_widget in self.piece_widgets:
            piece_widget.disable_drag()
        print('##################################################\n' \
              + f'Checkmate! {checkmating_player} won.\n' \
              + '##################################################')

    def update_material_text(self):
        score = self.match_controller.get_material_difference()
        self.white_material_text = ''
        self.black_material_text = ''
        if score > 0:
            self.white_material_text = '+' + str(score)
        elif score < 0:
            self.black_material_text = '+' + str(-score)

    def update_move_text(self, move_in_notation, move_count, color):
        color_code = 'ffffff'
        if color == 'b':
            color_code = '000000'
        text = str(move_count) + '.' + move_in_notation + ',  '
        self.move_notations_text += f'[color={color_code}]' + text + '[/color]'

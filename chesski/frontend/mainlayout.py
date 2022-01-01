from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty, Clock
from kivy.uix.image import Image
from kivy.uix.button import Button

import time

from chesski.frontend.chesspiece import ChessPiece
from chesski.frontend.buttons import IconButton

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
        self.black_stack = self.ids.player_display.ids.black_stack
        self.white_stack = self.ids.player_display.ids.white_stack
        self.piece_to_promote = None
        self.move_after_promote = None
        self.popup = self.ids.promotion_popup

    def black_engine_update(self, dt):
        if not self.match_controller.game_over:
            if self.match_controller.get_current_player() == 'b':
                self.match_controller.make_engine_move()

    def white_engine_update(self, dt):
        if not self.match_controller.game_over:
            if self.match_controller.get_current_player() == 'w':
                self.match_controller.make_engine_move()

    def on_toggle_white_engine(self, widget):
        if widget.state != 'normal':
            Clock.schedule_interval(self.white_engine_update, 1/2.0)
        else:
            Clock.unschedule(self.white_engine_update)

    def on_toggle_black_engine(self, widget):
        if widget.state != 'normal':
            Clock.schedule_interval(self.black_engine_update, 1/2.0)
        else:
            Clock.unschedule(self.black_engine_update)

    def start_game(self):
        """
        Button Function to start or reset the game.
        """
        self.remove_all_piece_widgets()

        # notify the match controller to start backend-match
        self.match_controller.init_match()
        self.display_pieces_from_state()

        # change start/reset button text
        self.start_reset_button_text = 'Reset'
        self.move_notations_text = ''
        self.clear_stacks()

    def remove_all_piece_widgets(self):
        """remove all remaining gui-pieces"""
        if self.piece_widgets:
            self.ids.game_box.clear_widgets(self.piece_widgets)
            self.piece_widgets = []

    def display_pieces_from_state(self):
        """displays the current state of the backend match"""
        self.remove_all_piece_widgets()
        for row in range(8):
            for col in range(8):
                coordinates = (row, col)
                type = self.match_controller.get_piece_type_from_state(coordinates)
                if type != None:
                    self.add_piece(type, coordinates)

    def get_piece_widget(self, coordinates):
        for piece in self.piece_widgets:
            if piece.last_coordinates == coordinates:
                return piece
        return None

    def add_piece(self, type, coordinates):
        """
        Instantiates the Chesspiece UI-Element and add id as
        child-widget of the game-box.
        """
        gui_piece = ChessPiece(
            board_grid=self.ids.board_grid,
            type=type,
            coordinates=coordinates,
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
                # print('piece removed')
                self.update_material_text()
                if to_stack:
                    image_path = piece_to_remove.source
                    new_image = Image(source=image_path, size_hint=(.05, 1))
                    if image_path[-7] == 'w':
                        self.black_stack.add_widget(new_image)
                    else:
                        self.white_stack.add_widget(new_image)
                return
        raise ValueError('Piece to remove couldnt be found.')

    def handle_checkmate(self, checkmating_player):
        for piece_widget in self.piece_widgets:
            piece_widget.disable_drag()
        print('##################################################\n' \
              + f'   Checkmate! {checkmating_player} won.\n' \
              + '##################################################')

    def handle_draw(self, checkmating_player):
        for piece_widget in self.piece_widgets:
            piece_widget.disable_drag()
        print('##################################################\n' \
              + f'                   Draw!\n' \
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

    def clear_stacks(self):
        self.white_stack.clear_widgets()
        self.black_stack.clear_widgets()

    def on_rotate_board_buttonpress(self):
        if not self.match_controller.game_over:
            perspective = self.ids.board_grid.rotate_boardgrid()
            self.ids.board_image.source = self.graphics_path + \
                        f'/chessboard_and_pieces/chessboard_{perspective}.png'
            self.remove_all_piece_widgets()
            self.display_pieces_from_state()

    def popup_promotion(self, piece_widget, player, move):
        """Shows the Promotion options, fills it with colored piece images and
        stores information (which piece to promote and what move to make)
        that is needed when choice was made (IconButton clicked)"""
        for widget, choice in zip(self.popup.children, ['R', 'N', 'B', 'Q']):
            widget.source = self.graphics_path + f'/chessboard_and_pieces/{player}_{choice}.png'
        self.popup.pos = piece_widget.pos
        self.popup.opacity = 1
        self.popup.disabled = False
        self.piece_to_promote = piece_widget
        self.move_after_promote = move

    def on_promotion_choice(self, choice):
        """when promotion-iconbutton clicked, inform piece widget, which will
        inform the match-controller to make the correct move (if legal)"""
        self.piece_to_promote.make_promotion_move(self.move_after_promote, choice)
        self.popup.opacity = 0
        self.popup.disabled = True
        self.popup.x = 3*self.width

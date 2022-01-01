from kivy.uix.behaviors import DragBehavior
from kivy.uix.image import Image
from kivy.properties import ObjectProperty, NumericProperty, Clock
from kivy.metrics import dp

class ChessPiece(DragBehavior, Image):

    def __init__(self, board_grid, type, graphics_path, coordinates,
                 match_controller, **kwargs):
        super().__init__(**kwargs)

        self.board_grid = board_grid
        self.match_controller = match_controller

        self.drag_rectangle = (self.board_grid.x, self.board_grid.y,
                               self.board_grid.width, self.board_grid.height)
        self.type = type

        self.source = graphics_path + f'/chessboard_and_pieces/{type}.png'

        self.starting_coordinates = coordinates
        self.last_coordinates = coordinates
        self.getting_dragged = False

        self.enable_drag()

        Clock.schedule_once(self.turn_visible, .1)

    def enable_drag(self):
        self.drag_distance = dp(1)

    def disable_drag(self):
        self.drag_distance = dp(100000)

    def update_while_dragging(self, dt):
        self.stay_on_board_grid()

    def turn_visible(self, dt):
        """
        workaround for image appearing at 0,0 when first instantiated
        """
        self.move_to_coordinates(self.starting_coordinates)
        self.opacity=1

    def on_size(self, *args):
        self.move_to_coordinates(self.last_coordinates)
        self.drag_rectangle = (self.board_grid.x, self.board_grid.y,
                               self.board_grid.width, self.board_grid.height)

    def on_touch_down(self, touch):
        """
        if start dragging start function schedule to keep piece on board.
        """
        if not self.match_controller.game_over:
            if self.collide_point(*touch.pos): # start only for clicked piece
                Clock.schedule_interval(self.update_while_dragging, 1/60.0)
                self.getting_dragged = True

        super(ChessPiece, self).on_touch_down(touch)


    def stay_on_board_grid(self):
        """
        Function adjusting Position of piece if dragged off board.
        """
        if self.x < self.board_grid.x:
            self.x = self.board_grid.x
        elif self.right > self.board_grid.x + self.board_grid.width:
            self.right = self.board_grid.x + self.board_grid.width
        elif self.y < self.board_grid.y:
            self.y = self.board_grid.y
        elif self.top > self.board_grid.y + self.board_grid.height:
            self.top = self.board_grid.y + self.board_grid.height

    def get_nearest_coordinates(self):
        piece_x = self.center_x
        piece_y = self.center_y
        for row in range(8):
            for col in range(8):
                field = self.board_grid.get_field((row, col))
                field_left_x = field.x
                field_right_x = field.right
                field_bottom_y = field.y
                field_top_y = field.top
                if (field_left_x < piece_x < field_right_x and
                   field_bottom_y < piece_y < field_top_y):
                   return (row, col)
        return None

    def on_touch_up(self, touch):
        """
        if stop dragging stop function schedule to keep piece on board.
        """
        if not self.match_controller.game_over:
            if self.getting_dragged: # only for clicked piece
                next_coordinates = self.get_nearest_coordinates()
                if next_coordinates == None:
                    self.move_to_coordinates(self.last_coordinates)
                else:
                    move = (self.last_coordinates, next_coordinates)
                    if (self.type == 'w_P' and next_coordinates[0] == 7 or
                        self.type == 'b_P' and next_coordinates[0] == 0):
                        self.match_controller.ask_for_promotion(self,
                                                                self.type[0],
                                                                move)
                    elif (self.match_controller.move_was_possible(*move)):
                            self.move_to_coordinates(next_coordinates)
                            # print('move made!', next_coordinates)

                    else: # move back
                        self.move_to_coordinates(self.last_coordinates)
                        # print('could not make move')

                # stop function schedule to keep piece on board
                Clock.unschedule(self.update_while_dragging)

                self.getting_dragged = False
        super(ChessPiece,self).on_touch_up(touch)

    def make_promotion_move(self, move, promotion_choice):
        if (self.match_controller.move_was_possible(*move, promotion_choice)):
            self.move_to_coordinates(move[1])
            # print('move made!', next_coordinates)

        else: # move back
            self.move_to_coordinates(self.last_coordinates)
            # print('could not make move')

    def move_to_coordinates(self, coordinates):
        """
        Move this Piece (Gui-Element) to given coordinates.
        Update coordinates attribute.
        """
        field = self.board_grid.get_field(coordinates)
        self.center_x = field.center_x
        self.center_y = field.center_y
        self.last_coordinates = coordinates
        # print('moved to coordinates: ', coordinates)
